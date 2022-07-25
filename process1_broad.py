import time
import messenger

configs = messenger.load_conf_file("conf1.toml")
clocks = messenger.initialize_clocks(configs.process_quantity)
msgr = messenger.Messenger(configs,clocks)
msgr.activate_broadcast()

while True:
    messages = msgr.collect_messages()
    for msg in messages:
        if msg.pid is not None:
            print(f'Message received: {msg.message}')
            print(f'PID sender: {msg.pid}')
            print(f'Sequence number: {msg.seqnum}')
            sent = False
            while not sent:
                sent = msgr.broadcast("Hello!".encode())
                print("Sent" if sent else "Not sent")
                time.sleep(1)