import time
import trab

configs = trab.load_conf_file("conf0.toml")
clocks = trab.initialize_clocks(configs.process_quantity)
messenger = trab.Messenger(config=configs, clocks=clocks)
print('configs done!')

while True:
    sent = messenger.broadcast("hi!".encode())
    print("Sent" if sent else "Not sent")
    time.sleep(1)
    pid_sender, msg, seqnum = messenger.deliver()
    if pid_sender != None:
        print(f'Message received: {msg}')
        print(f'PID sender: {pid_sender}')
        print(f'Sequence number: {seqnum}')
    else:
        print("No message received")
    time.sleep(1)