# from trab import load_conf_file, Messenger
import trab

# mensagens = []


def on_receive(message: trab.Message) -> None:
    _, data, _ = message
    print(f'message received!: {data}')
    # mensagens.append(data)


configs = trab.load_conf_file("conf1.toml")
clocks = trab.initialize_clocks(configs.process_quantity)
messenger = trab.Messenger(configs,clocks)
# print('configs done!')
# messenger.send(1,"hi!")
# print('message send!')

# _, data, _ = messenger.receive()
trab.listen(messenger, on_receive)


# lib.send(2,"opa")



