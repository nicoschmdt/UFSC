from email import message
from email.policy import default
import json
import threading
import toml
import time
import socket
import copy
import sys
from threading import RLock, Lock, Thread
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
            s.settimeout(3) # Valor arbitrário. Idealmente, baseado no atraso de rede.)
            s.connect((address, port))
            sock_out = s.makefile('wb')
            sock_out.write(message)
            sock_out.flush()


    def receive(self) -> bytes:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
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
    pending_messages: list[Message] = field(default_factory=list)
    delivered_messages: list[Message] = field(default_factory=list)
    lock_delivered: Lock = field(default_factory=Lock)

    thread_broadcast: Thread = field(default_factory=Thread)
    stop_broadcast: bool = False
    
    connector_factory: Callable[[str, int], Connection] = TCPConnection
    connector: Connection = field(init=False)
    lock: RLock = field(default_factory=RLock)

    def __post_init__(self) -> None:
        full_address = self.config.process_ports[self.config.process_id]
        address, port_text = full_address.split(':', maxsplit=1)
        self.connector = self.connector_factory(address, int(port_text))

    def send(self, id: int, msg: bytes, seqnum: int = 0, pid_sender: int | None = None) -> None:
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

        return Message((int)(pid_sender), msg.decode(), (int)(seqnum))

    def broadcast(self, msg: bytes) -> bool:
        try:
            self.send(self.config.sequencer_id, msg)
            return True
        except:
            return False

    def deliver(self) -> None:
        msg = self.receive()
        self.pending_messages.append(msg)
        self.get_from_pending_messages()

    def get_from_pending_messages(self) -> None:
        # print("pending_messsages: ", self.pending_messages)
        # print("next_deliver: ", self.next_deliver)
        index = 0
        while index < len(self.pending_messages):
            if self.next_deliver == self.pending_messages[index].seqnum:
                msg = self.pending_messages.pop(index)
                self.next_deliver += 1
                if msg.pid != self.config.process_id:
                    with self.lock_delivered:
                        self.delivered_messages.append(msg)
            else:
                index += 1

    def collect_messages(self) -> list[Message]:
        delivered = []
        with self.lock_delivered:
            delivered = copy.deepcopy(self.delivered_messages)
            self.delivered_messages.clear()
        return delivered

    def activate_broadcast(self) -> None:
        self.stop_broadcast = False
        self.thread_broadcast = threading.Thread(target=self.thread_run_deliver)
        self.thread_broadcast.start()
    
    def thread_run_deliver(self) -> None:
        while True:
            self.deliver()
            if self.stop_broadcast:
                print("Turning broadcast service off")
                break

    def deactivate_bradcast(self) -> None:
        self.stop_broadcast = True
        self.thread_broadcast.join()

@dataclass
class Sequencer:
    config: Configs
    messenger: Messenger

    def wait_messages(self) -> None:
        seqnum: int = 2
        while(True):
            msg = self.messenger.receive()
            # print(f'pid sender: {msg.pid}')
            # print(f'message received!: {msg.message}')

            for target_pid in range(0, self.config.process_quantity):
                # print(f"Trying to send to {target_pid}")
                if target_pid != self.config.process_id:
                    # Sequencer só envia a próxima mensagem se a anterior já foi enviada para TODOS os processos.
                    while True:
                        try:
                            self.messenger.send(target_pid, msg.message.encode(), seqnum, msg.pid)
                            # print(f"Sent to {msg.pid}")
                            # print(f"seqnum: {msg.seqnum}")
                            break
                        except:
                            time.sleep(2)
                            continue

            # Ordem do primeiro e do segundo seqnum invertida.
            if seqnum == 2:
                seqnum = 1
            elif seqnum == 1:
                seqnum = 3
            else:
                seqnum += 1

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