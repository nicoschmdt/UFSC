import json
import toml
import time
import socket
from threading import RLock, Thread
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, NamedTuple, Protocol
# 1:1 deve respeitar a ordem causal
# Ordem Causal: Se o envio de uma mensagem m precede
# causalmente o envio de uma mensagem m’, então
# nenhum processo correto entrega m’ a menos que m
# já tenha sido entregue

class InvalidPID(Exception):
    pass


class Connection(Protocol):
    def send(self, address: str, port: int, message: bytes) -> None:
        ...

    def receive(self) -> bytes:
        ...


@dataclass
class TCPConnection:
    address: str
    port: int

    def send(self, address: str, port: int, message: bytes) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((address, port))
            sock_out = s.makefile('wb')
            sock_out.write(message)
            sock_out.flush()


    def receive(self) -> bytes:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
            # s.settimeout(10) # Valor arbitrário. Idealmente, baseado no atraso de rede.
            s.listen(1)
            connection, _ = s.accept()

            sock_in = connection.makefile('rb')
            f = sock_in.read(4)
            msg_size = int.from_bytes(f, 'big')
            message = sock_in.read(msg_size)
            return message


@dataclass
class Configs:
    """Classe para armazenar as informações de um processo."""
    process_quantity: int
    process_id: int
    process_ports: dict[int, str]
    sequencer_id: int


class Message(NamedTuple):
    pid: int
    message: str
    seqnum: int


@dataclass
class Messenger:
    config: Configs
    clocks: dict[int,int] = field(default_factory=lambda: defaultdict(lambda: 0))

    next_deliver: int = 1
    pending_messages = []
    connector_factory: Callable[[str, int], Connection] = TCPConnection
    connector: Connection = field(init=False)
    lock: RLock = field(default_factory=RLock)

    def __post_init__(self) -> None:
        full_address = self.config.process_ports[self.config.process_id]
        address, port_text = full_address.split(':', maxsplit=1)
        self.connector = self.connector_factory(address, int(port_text))

    def send(self, id: int, msg: bytes, seqnum: int = 0, pid_sender: int | None = None) -> None:
        with self.lock:
            pid = self.config.process_id
            if pid_sender is not None:
                pid = pid_sender

            self.lock.acquire()
            self.clocks[pid] += 1
            self.lock.release()

            if id >= self.config.process_quantity:
                raise InvalidPID("PID is higher than the number of processes.")

            message = b";".join([
                f'{pid}'.encode(),
                json.dumps(self.clocks).encode(),
                f'{seqnum}'.encode(),
                msg,
            ])
            message = b"".join([len(message).to_bytes(4,'big'), message])

            target_pid, port = self.config.process_ports[id].split(':')
            self.connector.send(target_pid, int(port), message)

    def increment_clock(self) -> None:
        self.clocks[self.config.process_id] += 1

    def receive(self) -> Message:
        with self.lock:
            pid = self.config.process_id

            self.lock.acquire()
            self.increment_clock()
            self.lock.release()

            data = self.connector.receive()

            # get info from msg
            pid_sender, clocks_sender, seqnum, msg = data.split(b';')
            clocks = {int(pid): clock for pid, clock in json.loads(clocks_sender.decode()).items()}

            self.lock.acquire()
            for pid_s in clocks:
                # s = senderticks_s
                ticks_s = clocks[pid_s]
                if pid_s != pid:
                    self.clocks[pid_s] = max(ticks_s,self.clocks[pid_s])
            self.lock.release()



        return Message(int.from_bytes(pid_sender, 'big'), msg.decode(), int.from_bytes(seqnum, 'big'))

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

MessageReceivedCallback = Callable[[Message], None]

def listen(messenger: Messenger, callback: MessageReceivedCallback) -> Thread:
    def receive_messages():
        while True:
            message = messenger.receive()
            callback(message)
    thread = Thread(target=receive_messages)
    thread.start()
    return thread