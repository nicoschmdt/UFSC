# from trab import load_conf_file, Messenger
import trab

configs = trab.load_conf_file("conf0.toml")
clocks = trab.initialize_clocks(configs.process_quantity)
messenger = trab.Messenger(config=configs, clocks=clocks)
print('configs done!')
messenger.send(1,"hi!".encode()) # envia msg pro processo 1

# data = messenger.receive()
# print(f'message received!: {data}')
# lib.send(2,"opa")



