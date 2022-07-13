# from trab import load_conf_file, Messenger
import trab

configs = trab.load_conf_file("conf1.toml")
clocks = trab.initialize_clocks(configs.process_quantity)
messenger = trab.Messenger(configs,clocks)
# print('configs done!')
# messenger.send(1,"hi!")
# print('message send!')

data = messenger.receive().decode()
print(f'message received!: {data}')
# lib.send(2,"opa")



