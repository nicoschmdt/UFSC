import time
import trab

configs = trab.load_conf_file("conf1.toml")
clocks = trab.initialize_clocks(configs.process_quantity)
messenger = trab.Messenger(configs,clocks)

while True:
    pid_sender, msg, seqnum = messenger.deliver()
    if pid_sender != None:
        print(f'Message received: {msg}')
        print(f'PID sender: {pid_sender}')
        print(f'Sequence number: {seqnum}')
        sent = messenger.broadcast("Hello!".encode())
        print("Sent" if sent else "Not sent")
    else:
        print("No message received")
    time.sleep(1)