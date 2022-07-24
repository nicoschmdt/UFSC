import time
import messenger

configs = messenger.load_conf_file("conf2.toml")
clocks = messenger.initialize_clocks(configs.process_quantity)
state = "RELEASED"
clocks = messenger.initialize_clocks(configs.process_quantity)
msgr = messenger.Messenger(config=configs, clocks=clocks)
pid = configs.process_id
msgr.activate_broadcast()
queue = []


## Process 2 wants to enter the region
state = "WANTED"
sent = False

print("Sending timestamp")
while not sent:
    # Tries to send message
    msg=str(msgr.clocks[pid]).encode()
    sent = msgr.broadcast(msg)
    time.sleep(1)
# Get responses from other processes
num_oks = 0
while num_oks < configs.process_quantity-2:
    messages = msgr.collect_messages()
    for msg in messages:
        if "OK" not in msg.message:
            print("Received timestamp from process", msg.pid)
            if int(msg.message) < msgr.clocks[pid]:
                print("Sending OK to lower timestamp")
                sent = False
                while not sent:
                    sent = msgr.broadcast(f'OK,{msg.pid}'.encode())
                    time.sleep(1)
            else:
                queue.append(msg.pid)
        elif "2" in msg.message:
            num_oks += 1

## Enter critical region
print("Entering critical region")
state = "HELD"
time.sleep(2)
for process in queue:
    print(f"Sending OK to {process}")
    send = False
    while not send:
        send = msgr.broadcast(f'OK,{process}'.encode())
        time.sleep(1)
print("Exiting critical region")
state = "RELEASED"

