import time
import messenger

configs = messenger.load_conf_file("conf0.toml")
clocks = messenger.initialize_clocks(configs.process_quantity)
state = "RELEASED"
clocks = messenger.initialize_clocks(configs.process_quantity)
msgr = messenger.Messenger(config=configs, clocks=clocks)
pid = configs.process_id
msgr.activate_broadcast()
queue = []
print('configs done!')

## Process 0 wants to enter the region
state = "WANTED"
sent = False
# def on_receive(message: messenger.Message) -> None:
#     _, data, _ = message
#     print(f'message received!: {data}')
#     # mensagens.append(data)

# messenger.listen(msgr, on_receive)
while not sent:
    # Tries to send message
    msg=str(msgr.clocks[pid]).encode()
    sent = msgr.broadcast(msg)
    print("Sent" if sent else "Not sent")
    print(msg.decode())
    time.sleep(1)
# Get responses from other processes
num_oks = 0
while num_oks < configs.process_quantity-2:
    messages = msgr.collect_messages()
    for msg in messages:
        if msg.pid is not None:
            print(f'Message received: {msg.message}')
            print(f'PID sender: {msg.pid}')
            print(f'Sequence number: {msg.seqnum}')
        if "OK" not in msg.message:
            if int(msg.message) < msgr.clocks[pid]:
                print("Sending ok to lower timestamp")
                sent = False
                while not sent:
                    sent = msgr.broadcast(f'OK,{msg.pid}'.encode())
            else:
                queue.append(msg.pid)
        elif "0" in msg.message:
            num_oks += 1

## Enter critical region
print("Entering critical region")
state = "HELD"
time.sleep(2)
for process in queue:
    print(f"Sending ok to {process}")
    sent = False
    while not sent:
        sent = msgr.broadcast(f'OK,{process}'.encode())
print("Exiting critical region")
state = "RELEASED"