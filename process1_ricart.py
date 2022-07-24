import time
import messenger

configs = messenger.load_conf_file("conf1.toml")
clocks = messenger.initialize_clocks(configs.process_quantity)
state = "RELEASED"
clocks = messenger.initialize_clocks(configs.process_quantity)
msgr = messenger.Messenger(config=configs, clocks=clocks)
msgr.activate_broadcast()

while True:
    messages = msgr.collect_messages()
    for msg in messages:
        if msg.pid is not None:
            if "OK" not in msg.message:
                print("Received timestamp from process", msg.pid)
                print("Sending OK to process", msg.pid)
                sent = False
                while not sent:
                    sent = msgr.broadcast(f'OK,{msg.pid}'.encode())
                    time.sleep(1)
            else:
                print("Received OK from process", msg.pid)
            