import trab

def ricart_agrawala() -> None:
    process0_configs = trab.load_conf_file("conf0.toml")
    process1_configs = trab.load_conf_file("conf1.toml")
    process2_configs = trab.load_conf_file("conf2.toml")
    sequencer = trab.load_conf_file("conf_seq.toml")
    process0 = trab.Messenger(process0_configs)
    process1 = trab.Messenger(process1_configs)
    process2 = trab.Messenger(process2_configs)

    # Process P0 and P2 want to enter the region
    want_region(process0)
    want_region(process2)

def want_region(messenger: trab.Messenger) -> None:
    pid = messenger.config.process_id
    messenger.state = "wanted"
    messenger.broadcast(messenger.clocks[pid])

def enter_region() -> None:
    # state Held
    return None

def exit_region() -> None:
    #state released
    # awnser ok to all
    return None

ricart_agrawala()