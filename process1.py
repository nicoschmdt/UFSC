# from trab import load_conf_file, Messenger
import messenger

# mensagens = []


def on_receive(message: messenger.Message) -> None:
    _, data, _ = message
    print(f'message received!: {data}')
    # mensagens.append(data)


configs = messenger.load_conf_file("conf1.toml")
clocks = messenger.initialize_clocks(configs.process_quantity)
msgr = messenger.Messenger(configs,clocks)
# print('configs done!')
# messenger.send(1,"hi!")
# print('message send!')

# _, data, _ = messenger.receive()
messenger.listen(msgr, on_receive)


# lib.send(2,"opa")



