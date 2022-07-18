import trab

configs = trab.load_conf_file("conf0.toml")
clocks = trab.initialize_clocks(configs.process_quantity)
messenger = trab.Messenger(config=configs, clocks=clocks)
print('configs done!')
messenger.broadcast("hi!".encode())