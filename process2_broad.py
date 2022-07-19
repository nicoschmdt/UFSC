import time
import trab

configs = trab.load_conf_file("conf2.toml")
clocks = trab.initialize_clocks(configs.process_quantity)
messenger = trab.Messenger(configs,clocks)
messenger = trab.Messenger(configs,clocks)

while True:
    pid_sender, msg, seqnum = messenger.deliver()
    if pid_sender != None:
        print(f'Message received: {msg}')
        print(f'PID sender: {pid_sender}')
        print(f'Sequence number: {seqnum}')
    else:
        print("No message received")
    time.sleep(1)