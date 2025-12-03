#!/usr/bin/env python

import pika
import sys
import time

def handle_message(channel, method, props, body):
    print('(i) Received a message!')
    print(body.decode())
    time.sleep(5)
    print('(i) Done')
    channel.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()
    channel.queue_declare(queue='tasks')
    channel.basic_consume(queue='tasks', on_message_callback=handle_message)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
