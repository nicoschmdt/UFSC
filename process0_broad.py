import time
import messenger

configs = messenger.load_conf_file("conf0.toml")
clocks = messenger.initialize_clocks(configs.process_quantity)
msgr = messenger.Messenger(config=configs, clocks=clocks)
msgr.activate_broadcast()
print('configs done!')

while True:
    sent = False
    while not sent:
        sent = msgr.broadcast("hi!".encode())
        print("Sent" if sent else "Not sent")
        time.sleep(1)
    messages = msgr.collect_messages()
    for msg in messages:
        if msg.pid is not None:
            print(f'Message received: {msg.message}')
            print(f'PID sender: {msg.pid}')
            print(f'Sequence number: {msg.seqnum}')
    time.sleep(1)