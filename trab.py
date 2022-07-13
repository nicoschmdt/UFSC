import socket
import toml
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


@dataclass
class Configs:
    """Classe para armazenar as informações de um processo."""
    process_quantity: int
    process_id: int
    process_ports: dict[int, str]


@dataclass
class Messenger:
    config: Configs
    clocks: dict[int,int] = field(default_factory=defaultdict(lambda: 0))

    def send(self, id: int, msg: bytes) -> None:
        pid = self.config.process_id
        self.clocks[pid] += 1
        if id >= self.config.process_quantity:
            return "Error" # melhorar a msg

        # pid.to_bytes(2,'big'),
        message = b";".join([
            f'{pid}'.encode(),
            str(self.clocks).encode(),
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
            print(data)

        # get info from msg
        pid_sender, clocks_sender, msg = data.decode().split(';')
        clocks_sender = eval(clocks_sender)

        for clock in clocks_sender:
            # s = sender
            pid_s, ticks_s = clock
            if pid_s != pid:
                self.clocks[pid_s] = max(ticks,self.clocks[pid_s])

        return msg


def load_conf_file(file_path):
    with open(file_path, "r") as f:
        data = toml.load(f)
    return Configs(
        process_quantity=data["node"]["processos"],
        process_id=data["node"]["id"],
        process_ports=data["all_processes"]
    )


def initialize_clocks(num_process):
    clocks = {}
    for num in range(num_process):
        clocks[num] = 0
    return clocks
