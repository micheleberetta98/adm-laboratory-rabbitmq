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

    # TODO: Fill code
    
    w.content = FormattedTextControl('\n'.join(output))


def message_listener():
    # TODO: Fill code
    pass


# ----------- Setup sending messages

def send_on_rabbitmq(msg):
    # TODO: Fill code

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
