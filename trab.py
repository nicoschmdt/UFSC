import socket
import toml
from collections import defaultdict
from dataclasses import dataclass, field
import time
from threading import Lock
# 1:1 deve respeitar a ordem causal
# Ordem Causal: Se o envio de uma mensagem m precede
# causalmente o envio de uma mensagem m’, então
# nenhum processo correto entrega m’ a menos que m
# já tenha sido entregue

# ---------------------------------------------------
# Observe que a ordem causal implementa, internamente,
# um vetor de relógios lógicos de n posições, onde n
# representa o número de processos.


@dataclass
class Configs:
    """Classe para armazenar as informações de um processo."""
    process_quantity: int
    process_id: int
    process_ports: dict[int, str]
    sequencer_id: int

@dataclass
class Messenger:
    config: Configs
    clocks: dict[int,int] = field(default_factory=defaultdict(lambda: 0))
    next_deliver = 1
    pending_messages = []

    def send(self, id: int, msg: bytes, seqnum: int = 0) -> None:
        pid = self.config.process_id
        self.clocks[pid] += 1
        if id >= self.config.process_quantity:
            return "Error" # melhorar a msg

        # pid.to_bytes(2,'big'),
        message = b";".join([
            f'{pid}'.encode(),
            str(self.clocks).encode(),
            f'{seqnum}'.encode(),
            msg
        ])        

        port, port_number = self.config.process_ports[str(id)].split(':')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((port, int(port_number)))
            s.listen(1)
            conn, addr = s.accept()
            conn.send(message)


    def receive(self) -> bytes:
        pid = self.config.process_id
        self.clocks[pid] += 1

        port, port_number = self.config.process_ports[str(self.config.process_id)].split(':')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((port, int(port_number)))
            data = s.recv(1024)
            # print(data)

        # get info from msg
        pid_sender, clocks_sender, seqnum, msg = data.decode().split(';')
        clocks_sender = eval(clocks_sender)

        for pid_s in clocks_sender:
            # s = sender
            ticks_s = clocks_sender[pid_s]
            if pid_s != pid:
                self.clocks[pid_s] = max(ticks_s,self.clocks[pid_s])

        return ((int)(pid_sender), msg, (int)(seqnum))

    def broadcast(self, msg: bytes) -> None:
        self.send(self.config.sequencer_id, msg)

    def deliver(self) -> bytes:
        try:
            pid_sender, msg, seqnum = self.receive()
            self.pending_messages.append((pid_sender, msg, seqnum))
            # print(self.pending_messages)
            # print(self.next_deliver)
            for i in range(len(self.pending_messages)):
                if self.next_deliver == (int)(self.pending_messages[i][2]):
                    pid_sender_deliver, msg_deliver, seqnum_deliver = self.pending_messages.pop(i)
                    self.next_deliver += 1
                    return (pid_sender_deliver, msg_deliver, seqnum_deliver)
            return (None, None, None)
        except:
            # print(self.pending_messages)
            # print(self.next_deliver)
            for i in range(len(self.pending_messages)):
                if self.next_deliver == (int)(self.pending_messages[i][2]):
                    pid_sender_deliver, msg_deliver, seqnum_deliver = self.pending_messages.pop(i)
                    self.next_deliver += 1
                    return (pid_sender_deliver, msg_deliver, seqnum_deliver)
            return (None, None, None)

@dataclass
class Sequencer:
    config: Configs
    messenger: Messenger

    def wait_messages(self) -> None:
        seqnum: int = 2
        while(True):
            try:
                pid_sender, msg, _ = self.messenger.receive()
                # print(f'pid sender: {pid_sender}')
                # print(f'message received!: {msg}')

                for pid in range(0, self.config.process_quantity):
                    # print(f"Trying to send to {pid}")
                    if pid != (int)(pid_sender) and pid != self.config.process_id:
                        # print(f"Sent to {pid}")
                        # print(f"seqnum: {seqnum}")
                        self.messenger.send(pid, msg.encode(), seqnum)

                # Ordem do primeiro e do segundo seqnum invertida.
                if seqnum == 2:
                    seqnum = 1
                elif seqnum == 1:
                    seqnum = 3
                else:
                    seqnum += 1
            except:
                # print("Nothing received")
                # time.sleep(2)
                continue

def load_conf_file(file_path):
    with open(file_path, "r") as f:
        data = toml.load(f)
    return Configs(
        process_quantity=data["node"]["processos"],
        process_id=data["node"]["id"],
        process_ports=data["all_processes"],
        sequencer_id=data["sequencer"]["id"]
    )


def initialize_clocks(num_process):
    clocks = {}
    for num in range(num_process):
        clocks[num] = 0
    return clocks
