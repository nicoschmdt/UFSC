import socket
import toml
from dataclasses import dataclass
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

    def send(self, id, msg):
        if id >= self.config.process_quantity:
            return "Error" # melhorar a msg

        port, port_number = self.config.process_ports[str(id)].split(':')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print('socket created!')
            s.bind((port, int(port_number)))
            print('binded!')
            s.listen(1)
            # conn, addr = s.accept()
            # s.accept()
            conn.send(msg.encode())
            # conn.close()
            # do jeito que tá, a conexão n é feita, que outra forma é legal de fazer?
            print('message sended!')


    def receive(self): #ond que vai o msg?
        port, port_number = self.config.process_ports[str(config.process_id)].split(':')


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((port, int(port_number)))
            s.listen()
            s.accept()
            data = s.recv(1024).decode()
            print(data)
        return data
        #     s.connect((TCP_IP, TCP_PORT))
        #     data = s.recv(BUFFER_SIZE)


def load_conf_file(file_path):
    with open(file_path, "r") as f:
        data = toml.load(f)
    return Configs(
        process_quantity=data["node"]["processos"],
        process_id=data["node"]["id"],
        process_ports=data["all_processes"]
    )



if __name__ == "__main__":
    # send(id,"Hello, World!")
    config = load_conf_file("conf0.toml")
    msg = Messenger(config)
    msg.send(1,"hi")
    # print(config)