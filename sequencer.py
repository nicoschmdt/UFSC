import messenger

configs = messenger.load_conf_file("conf_seq.toml")
clocks = messenger.initialize_clocks(configs.process_quantity)
msgr = messenger.Messenger(config=configs, clocks=clocks)
sequencer = messenger.Sequencer(config=configs, messenger=msgr)
sequencer.wait_messages()