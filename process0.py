# from trab import load_conf_file, Messenger
import trab

configs = trab.load_conf_file("conf0.toml")
messenger = trab.Messenger(configs)
print('configs done!')
messenger.send(0,"hi!")
print('message send!')

data = messenger.receive()
print(f'message received!: {data}')
# lib.send(2,"opa")



