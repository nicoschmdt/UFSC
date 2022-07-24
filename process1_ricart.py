import time
import messenger

configs = messenger.load_conf_file("conf1.toml")
clocks = messenger.initialize_clocks(configs.process_quantity)
state = "RELEASED"
clocks = messenger.initialize_clocks(configs.process_quantity)
msgr = messenger.Messenger(config=configs, clocks=clocks)
msgr.activate_broadcast()

# def on_receive(message: messenger.Message) -> None:
#     _, data, _ = message
#     print(f'message received!: {data}')
#     # mensagens.append(data)

# messenger.listen(msgr, on_receive)
# P1 not interested
while True:
    messages = msgr.collect_messages()
    for msg in messages:
        print("Received Message")
        if msg.pid is not None:
            print(messages)
            print(f'Message received: {msg.message}')
            print(f'PID sender: {msg.pid}')
            print(f'Sequence number: {msg.seqnum}')
            sent = False
            while not sent:
                sent = msgr.broadcast(f'OK,{msg.pid}'.encode())