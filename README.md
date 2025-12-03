# Using RabbitMQ

## Requirements

### RabbitMQ

RabbitMQ is an open-source message-broker software that originally implemented
the Advanced Message Queuing Protocol (AMQP).

Written in Erlang, the RabbitMQ server is built on the Open Telecom Platform
framework for clustering and failover.

Follow the instruction for your favourite Operating System (e.g., [Arch](https://wiki.archlinux.org/title/RabbitMQ)).

### Python

No need of presentation, it's just used to run scripts in this folder.
You will need the `pika` library.

## Starting RabbitMQ

It's really simple, as it comes with a SystemD service.

```bash
sudo systemctl start rabbitmq
```

If you want to enable the HTTP admin page:

```bash
sudo rabbitmq-plugins enable rabbitmq_management
```

And you can reach the page at `localhost:15672` with user `guest` and password `guest`.
