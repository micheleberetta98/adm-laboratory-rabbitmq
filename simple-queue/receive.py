#!/usr/bin/env python

import pika
import sys

def handle_message(channel, method, props, body):
    print('(i) Received a message!')
    print(body)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()
    channel.queue_declare(queue='tasks')
    channel.basic_consume(queue='tasks', on_message_callback=handle_message, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
