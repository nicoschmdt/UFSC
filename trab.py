import json
import toml
import time
import socket
from collections import defaultdict
from dataclasses import dataclass, field
# 1:1 deve respeitar a ordem causal
# Ordem Causal: Se o envio de uma mensagem m precede
# causalmente o envio de uma mensagem m’, então
# nenhum processo correto entrega m’ a menos que m
# já tenha sido entregue

# ---------------------------------------------------
# Observe que a ordem causal implementa, internamente,
# um vetor de relógios lógicos de n posições, onde n
# representa o número de processos.
class InvalidPID(Exception):
    pass

class MessageProtocol:
    def send(self, target_pid: str, port: int, message: bytes) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((target_pid, port))
            s.settimeout(3) # Valor arbitrário. Idealmente, baseado no atraso de rede.
            s.listen(1)
            conn, addr = s.accept()
            conn.send(message)

    def receive(self, target_pid: str, port: int) -> bytes:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_pid, port))
            return s.recv(1024)

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
    clocks: dict[int,int] = field(default_factory=lambda: defaultdict(lambda: 0))
    next_deliver: int = 1
    pending_messages = []
    protocol: MessageProtocol = field(default_factory=MessageProtocol)

    def send(self, id: int, msg: bytes, seqnum: int = 0, pid_sender: int | None = None) -> None:
        pid = self.config.process_id
        if pid_sender is not None:
            pid = pid_sender
        self.clocks[pid] += 1
        if id >= self.config.process_quantity:
            raise InvalidPID("PID is higher than the number of processes.")

        message = b";".join([
            f'{pid}'.encode(),
            json.dumps(self.clocks).encode(),
            f'{seqnum}'.encode(),
            msg
        ])

        target_pid, port = self.config.process_ports[id].split(':')
        self.protocol.send(target_pid, int(port), message)


    def receive(self) -> tuple[int,str,int]:
        pid = self.config.process_id
        self.clocks[pid] += 1

        target_pid, port = self.config.process_ports[self.config.process_id].split(':')
        data = self.protocol.receive(target_pid, int(port))

        # get info from msg
        pid_sender, clocks_sender, seqnum, msg = data.decode().split(';')
        clocks = {int(pid): clock for pid, clock in json.loads(clocks).items()}

        for pid_s in clocks:
            # s = sender
            ticks_s = clocks[pid_s]
            if pid_s != pid:
                self.clocks[pid_s] = max(ticks_s,self.clocks[pid_s])

        return ((int)(pid_sender), msg, (int)(seqnum))

    def broadcast(self, msg: bytes) -> bool:
        try:
            self.send(self.config.sequencer_id, msg)
            return True
        except:
            return False

    def deliver(self) -> bytes:
        try:
            pid_sender, msg, seqnum = self.receive()
            self.pending_messages.append((pid_sender, msg, seqnum))
            return self.get_from_pending_messages()
        except:
            return self.get_from_pending_messages()

    def get_from_pending_messages(self):
        # print(self.pending_messages)
        # print(self.next_deliver)
        for i in range(len(self.pending_messages)):
            if self.next_deliver == (int)(self.pending_messages[i][2]):
                pid_sender_deliver, msg_deliver, seqnum_deliver = self.pending_messages.pop(i)
                self.next_deliver += 1
                if pid_sender_deliver != self.config.process_id:
                    return (pid_sender_deliver, msg_deliver, seqnum_deliver)
                else:
                    return (None, None, None)
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
                    if pid != self.config.process_id:
                        # print(f"Sent to {pid}")
                        # print(f"seqnum: {seqnum}")
                        # Sequencer só envia a próxima mensagem se a anterior já foi enviada para TODOS os processos.
                        while True:
                            try:
                                self.messenger.send(pid, msg.encode(), seqnum, pid_sender)
                                break
                            except:
                                continue

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
        process_ports={int(pid): port for pid, port in data["all_processes"].items()},
        sequencer_id=data["sequencer"]["id"]
    )


def initialize_clocks(num_process):
    clocks = {}
    for num in range(num_process):
        clocks[num] = 0
    return clocks
