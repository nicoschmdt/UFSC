# from trab import load_conf_file, Messenger
import messenger

configs = messenger.load_conf_file("conf0.toml")
clocks = messenger.initialize_clocks(configs.process_quantity)
msgr = messenger.Messenger(config=configs, clocks=clocks)
print('configs done!')
msgr.send(1,"hi!".encode()) # envia msg pro processo 1

# data = messenger.receive()
# print(f'message received!: {data}')
# lib.send(2,"opa")



