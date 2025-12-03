#!/usr/bin/env python

import sys
import pika

message = ' '.join(sys.argv[1:]) or 'Just a default message'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='tasks')
channel.basic_publish(exchange='', routing_key='tasks', body=message)
print('(!) Message sent')
connection.close()
