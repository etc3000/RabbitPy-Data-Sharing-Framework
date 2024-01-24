import pika
import logging
from api import ResearchAPI
from constants import Constants
from message import Message
from user import User

class RabbitMQConnection:
    """
    The RabbitMQConnection class is responsible for establishing and managing a connection to a RabbitMQ server.

    Attributes:
        user (User): The user who is using the connection.
        connection (pika.BlockingConnection): The connection to the RabbitMQ server.
        channel (pika.Channel): The channel for the connection.
        queue_name (str): The name of the queue for the connection.
    """

    CLASS_NAME = RabbitMQConnection.__name__
    RESEARCH_API_CONNECT = ResearchAPI.__name__ + ":connect"
    EXCHANGE_NAME = "research"
    EXCHANGE_TYPE = "direct"
    ANNOUNCE_ROUTING_KEY = "announce"
    SENT = " [x] Sent "

    def __init__(self, user: User, uri: str) -> None:
        """
        Initializes the RabbitMQConnection class with the user and URI.

        Args:
            user (User): The user who is using the connection.
            uri (str): The URI of the RabbitMQ server.
        """
        self.user = user
        self.connection = None
        self.channel = None
        self.queue_name = None

        factory = None

        if uri:
            try:
                factory = self.get_connection_factory(uri)
            except (KeyError, ValueError):
                logging.error(f"Failed to connect to RabbitMQ server: {uri}", self.RESEARCH_API_CONNECT)
                logging.info("Connecting to the default RabbitMQ server")

                # Attempt to connect to the default server
                factory = self.get_default_connection_factory()
                if factory is None:
                    return

        try:
            self.connection = factory.new_connection()
            if self.connection is None:
                factory = self.get_default_connection_factory()
                self.connection = factory.new_connection()
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=self.EXCHANGE_NAME, exchange_type=self.EXCHANGE_TYPE)
            result = self.channel.queue_declare(queue="", exclusive=True)
            self.queue_name = result.method.queue

            self.channel.queue_bind(exchange=self.EXCHANGE_NAME, queue=self.queue_name, routing_key=self.ANNOUNCE_ROUTING_KEY)
            self.channel.queue_bind(exchange=self.EXCHANGE_NAME, queue=self.queue_name, routing_key=self.user.get_user_id())
        except Exception as e:
            logging.error("Failed establishing connection and queues to RabbitMQ server, please double-check input URI",
                          self.RESEARCH_API_CONNECT)

    def get_connection_factory(self, uri: str) -> pika.URLParameters:
        """
        Gets a connection factory for the given URI.

        Args:
            uri (str): The URI of the RabbitMQ server.

        Returns:
            pika.URLParameters: The connection factory for the given URI.
        """
        factory = pika.URLParameters(uri)
        return factory

    def get_default_connection_factory(self) -> pika.ConnectionParameters:
        """
        Gets the default connection factory.

        Returns:
            pika.ConnectionParameters: The default connection factory.
        """
        factory = pika.ConnectionParameters(host=Constants.RABBITMQ_HOST,
                                            port=Constants.RABBITMQ_PORT,
                                            virtual_host=Constants.RABBITMQ_VHOST,
                                            credentials=pika.PlainCredentials(Constants.RABBITMQ_USER,
                                                                              Constants.RABBITMQ_PASSWORD))
        return factory

    def announce(self, message: Message) -> None:
        """
        Announces a message to the RabbitMQ server.

        Args:
            message (Message): The message to announce.
        """
        try:
            self.channel.basic_publish(exchange=self.EXCHANGE_NAME, routing_key=self.ANNOUNCE_ROUTING_KEY,
                                       body=message.to_json())
            sent = self.SENT + str(message)
            logging.info(sent)
        except Exception as e:
            logging.error(str(e), f"{self.CLASS_NAME}:{self.ANNOUNCE_ROUTING_KEY}")

    def direct(self, message: Message, user_id: str) -> None:
        """
        Sends a message directly to a user on the RabbitMQ server.

        Args:
            message (Message): The message to send.
            user_id (str): The ID of the user to send the message to.
        """
        try:
            self.channel.basic_publish(exchange=self.EXCHANGE_NAME, routing_key=user_id, body=message.to_json())
            sent = self.SENT + str(message)
            logging.info(sent)
        except Exception as e:
            logging.error(str(e), f"{self.CLASS_NAME}:{self.EXCHANGE_TYPE}")

    def get_channel(self) -> pika.Channel:
        """
        Gets the channel for the connection.

        Returns:
            pika.Channel: The channel for the connection.
        """
        return self.channel

    def get_queue_name(self) -> str:
        """
        Gets the name of the queue for the connection.

        Returns:
            str: The name of the queue for the connection.
        """
        return self.queue_name