import trab

configs = trab.load_conf_file("conf_seq.toml")
clocks = trab.initialize_clocks(configs.process_quantity)
messenger = trab.Messenger(config=configs, clocks=clocks)
sequencer = trab.Sequencer(config=configs, messenger=messenger)
sequencer.wait_messages()