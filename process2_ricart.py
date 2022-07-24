import time
import trab

configs = trab.load_conf_file("conf2.toml")
clocks = trab.initialize_clocks(configs.process_quantity)
state = configs["node"]["state"]
clocks = messenger.initialize_clocks(configs.process_quantity)
msgr = messenger.Messenger(config=configs, clocks=clocks)
pid = messenger.config.process_id
msgr.activate_broadcast()
queue = []
print('configs done!')

## Process 2 wants to enter the region
state = "WANTED"
sent = False
while not sent:
    # Tries to send message
    sent = msgr.broadcast(msg=msgr.clocks[pid])
    print("Sent" if sent else "Not sent")
    time.sleep(1)
# Get responses from other processes
receivedMessages = []
while (len(receivedMessages) < 2):
    # Wait until all respond (N -1)
    messages = msgr.collect_messages();
    for m in messages:
        receivedMessages.append(m)
for msg in receivedMessages:
    if msg.pid is not None:
        print(f'Message received: {msg.message}')
        print(f'PID sender: {msg.pid}')
        print(f'Sequence number: {msg.seqnum}')
    if msg.message != "OK":
        if int(msg.message) < msgr.clocks[pid]:
            msgr.send(msg.pid, "OK".encode())
        else:
            queue.append(msg.pid)

## Enter critical region
state = "HELD"
time.sleep(2)
for process in queue:
    msgr.send(process, "OK".encode())
        

