import argparse
from api.ResearchAPI import ResearchAPI
from user.User import User
from rabbitmq.RabbitMQConnection import RabbitMQConnection
from message.Message import Message
from message.ProcessMessage import ProcessMessage
from message.MagicWormhole import Wormhole
from logging.Log import Log
from shell_application.File_Function import csv_to_pdf


def main():
    """
    Upon running this script, user signs into RabbitMQ or connects after specifying their username, verify with logged credentials on server
    User uploads or types out their message, can also choose to convert a file to a different format
    User can also choose to listen for messages, receive a file, send a file, or convert a file
    User can specify intended recipient/channel of message or file
    :return:
    """
    parser = argparse.ArgumentParser(description='Interact with the Research API.')
    parser.add_argument('--connect', action='store_true', help='Connect to the RabbitMQ server.')
    parser.add_argument('--user', type=str, help='Specify the user ID.')
    parser.add_argument('--message', type=str, help='Specify a message to send.')
    parser.add_argument('--add-file', type=str, help='Add a file to the user profile and announce it.')
    parser.add_argument('--add-convert-format', nargs=2, help='Add a conversion format to the user profile.')
    parser.add_argument('--start-listening', action='store_true', help='Start listening for messages.')
    parser.add_argument('--get-received-file', action='store_true', help='Get the received file.')
    parser.add_argument('--send-direct', nargs=2, help='Send a direct message to a specific user.')
    parser.add_argument('--get-channel', action='store_true', help='Get the channel for the connection.')
    parser.add_argument('--get-queue-name', action='store_true', help='Get the name of the queue for the connection.')
    parser.add_argument('--convert-file', nargs=2, help='Convert a file from one format to another.')
    parser.add_argument('--send-file', type=str, help='Send a file using the Magic Wormhole protocol.')
    parser.add_argument('--receive-file', nargs=2, help='Receive a file using the Magic Wormhole protocol.')
    # Add more arguments as necessary...

    args = parser.parse_args()

    if args.connect:
        # Create a ResearchAPI instance and connect to the server
        api = ResearchAPI(Log.TYPE, Log.LEVEL)
        api.connect()

    if args.user:
        # Create a User instance with the specified ID
        user = User(args.user)

    if args.message:
        # Create a Message instance and send it
        message = Message(args.user, args.message)
        api.connection.announce(message)

    if args.add_file:
        # Add a file to the user's profile and announce it
        api.add_file(args.add_file)

    if args.add_convert_format:
        # Add a conversion format to the user's profile
        original_format, destination_format = args.add_convert_format
        api.add_convert_format(original_format, destination_format)

    if args.start_listening:
        # Start listening for messages
        api.start_listening()

    if args.get_received_file:
        # Get the received file
        received_file = api.get_received_file()
        print(f'Received file: {received_file}')

    if args.send_direct:
        # Send a direct message to a specific user
        message_text, user_id = args.send_direct
        message = Message(args.user, message_text)
        api.connection.direct(message, user_id)

    if args.get_channel:
        # Get the channel for the connection
        channel = api.connection.get_channel()
        print(f'Channel: {channel}')

    if args.get_queue_name:
        # Get the name of the queue for the connection
        queue_name = api.connection.get_queue_name()
        print(f'Queue name: {queue_name}')

    if args.convert_file:
        # Convert a file from one format to another
        source_file, target_file = args.convert_file
        csv_to_pdf(source_file, target_file)

    if args.send_file:
        # Send a file using the Magic Wormhole protocol
        Wormhole.send(api.connection, args.user, Message(args.user, "Sending file"), args.send_file)

    if args.receive_file:
        # Receive a file using the Magic Wormhole protocol
        command, filename = args.receive_file
        Wormhole.receive(api.connection, Message(args.user, "Receiving file"), command, filename, args.user)

    # Add more operations as necessary...


if __name__ == '__main__':
    main()
