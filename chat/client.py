#!/usr/bin/env python

import pika
import sys
import json
import threading
from datetime import datetime
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout

CHAT_NAME = 'chat'
if len(sys.argv) < 2:
    print('Usage: client.py [USERNAME]')
    sys.exit(1)
    
USERNAME = sys.argv[1]
input = Buffer()
output = []

# ----------- Setup receiving messages

def handle_message(channel, method, props, body):
    data = json.loads(body)
    sender = data['sender']

    if data['type'] == 'joined':
        output.append(f'(i) {sender} just joined')
    elif data['type'] == 'left':
        output.append(f'(i) {sender} just left')
    elif data['type'] == 'msg':
        timestamp = data['timestamp']
        content = data['content']
        output.append(f'({timestamp}) {sender}> {content}')
    
    w.content = FormattedTextControl('\n'.join(output))
    app.invalidate()


def message_listener():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=CHAT_NAME, exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=CHAT_NAME, queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=handle_message, auto_ack=True)
    channel.start_consuming()


# ----------- Setup sending messages

def send_on_rabbitmq(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=CHAT_NAME, exchange_type='fanout')
    channel.basic_publish(exchange=CHAT_NAME, routing_key='', body=json.dumps(msg))
    connection.close()

def send_message(content):
    send_on_rabbitmq({
        'type': 'msg',
        'sender': USERNAME,
        'timestamp': datetime.now().strftime('%H:%M'),
        'content': content,
    })

def send_joined(sender):
    send_on_rabbitmq({
        'type': 'joined',
        'sender': USERNAME,
    })

def send_left(sender):
    send_on_rabbitmq({
        'type': 'left',
        'sender': USERNAME,
    })

# ----------- Keybindings

kb = KeyBindings()
@kb.add('enter')
def on_enter(event):
    send_message(input.text)
    input.text = ''

@kb.add('c-c')
def exit_(event):
    event.app.exit()

# ----------- Setup graphical application

w = Window(content=FormattedTextControl(text=''))
root_container = HSplit([
    w,
    Window(height=1, char='—'),
    Window(height=2, content=BufferControl(input)),
])
layout = Layout(root_container)
app = Application(layout=layout, key_bindings=kb, full_screen=True)

# ----------- Start

listener = threading.Thread(target=message_listener, daemon=True)
listener.start()
send_joined(USERNAME)
app.run()
send_left(USERNAME)
