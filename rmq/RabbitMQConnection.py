# import pika
# from ..constants import Constants
# from ..message import Message
# from ..user import User
#
# class RabbitMQConnection:
#     EXCHANGE_NAME = "research"
#     EXCHANGE_TYPE = "direct"
#     ANNOUNCE_ROUTING_KEY = "announce"
#
#     def __init__(self, user: User, uri: str) -> None:
#         self.user = user
#         self.connection = pika.BlockingConnection(pika.URLParameters(uri))
#         self.channel = self.connection.channel()
#         self.queue_name = self.channel.queue_declare(queue="", exclusive=True).method.queue
#
#         self.channel.exchange_declare(exchange=self.EXCHANGE_NAME, exchange_type=self.EXCHANGE_TYPE)
#         self.channel.queue_bind(exchange=self.EXCHANGE_NAME, queue=self.queue_name,
#                                 routing_key=self.ANNOUNCE_ROUTING_KEY)
#         self.channel.queue_bind(exchange=self.EXCHANGE_NAME, queue=self.queue_name,
#                                 routing_key=self.user.get_user_id())
#
#     def announce(self, message: Message) -> None:
#         self.channel.basic_publish(exchange=self.EXCHANGE_NAME, routing_key=self.ANNOUNCE_ROUTING_KEY,
#                                    body=message.to_json())
#
#     def direct(self, message: Message, user_id: str) -> None:
#         self.channel.basic_publish(exchange=self.EXCHANGE_NAME, routing_key=user_id, body=message.to_json())
#
#     def get_channel(self) -> pika.Channel:
#         return self.channel
#
#     def get_queue_name(self) -> str:
#         return self.queue_name

import pika
from constants import Constants
from message import Message
from user import User


class RabbitMQConnection:
    EXCHANGE_NAME = "research"
    EXCHANGE_TYPE = "direct"
    ANNOUNCE_ROUTING_KEY = "announce"

    def __init__(self, user: User, uri: str) -> None:
        self.user = user
        self.connection = pika.BlockingConnection(pika.URLParameters(uri))
        self.channel = self.connection.channel()
        self.queue_name = self.channel.queue_declare(queue="", exclusive=True).method.queue

        self.channel.exchange_declare(exchange=self.EXCHANGE_NAME, exchange_type=self.EXCHANGE_TYPE)
        self.channel.queue_bind(exchange=self.EXCHANGE_NAME, queue=self.queue_name,
                                routing_key=self.ANNOUNCE_ROUTING_KEY)
        self.channel.queue_bind(exchange=self.EXCHANGE_NAME, queue=self.queue_name,
                                routing_key=self.user.get_user_id())

    def announce(self, message: Message) -> None:
        self.channel.basic_publish(exchange=self.EXCHANGE_NAME, routing_key=self.ANNOUNCE_ROUTING_KEY,
                                   body=message.to_json())

    def direct(self, message: Message, user_id: str) -> None:
        self.channel.basic_publish(exchange=self.EXCHANGE_NAME, routing_key=user_id, body=message.to_json())

    def get_channel(self) -> pika.channel:
        return self.channel

    def get_queue_name(self) -> str:
        return self.queue_name
