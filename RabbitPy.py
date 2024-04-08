import argparse
from user import User
from message import *
from my_logging.Log import Log
import shell_application.File_Function as ff
from constants import Constants
from shell_application.user_list import user_credentials
from rmq.RabbitMQConnection import RabbitMQConnection
import pika
from urllib.parse import urlparse

rmq_connection = None


def handle_user_registration(args):
    user_id, password = args.register
    user = User(user_id)
    user_credentials[user_id] = password
    print(f"User {user_id} registered successfully.")
    return user


def handle_user_login(args):
    user_id, password = args.login
    if user_id in user_credentials and password == user_credentials[user_id]:
        print(f"User {user_id} logged in successfully.")
        return user_id
    else:
        print("Invalid username or password.")
        return None

    # user_id, password = args.login
    # if user_id in user_credentials and password == user_credentials[user_id]:
    #     print(f"User {user_id} logged in successfully.")
    #     channel = connection.channel()
    #     channel.queue_declare(queue='test_queue')
    #     channel.basic_publish(exchange='', routing_key='test_queue', body=f'User {user_id} has connected.')
    #     print(f"User {user_id} connected to the RabbitMQ server.")
    #     channel.basic_publish(exchange='', routing_key='test_queue', body=f'User {user_id} has logged in.')
    #     print(f"Published message: 'User {user_id} has logged in.'")
    # else:
    #     print("Invalid username or password.")
    #     return


def handle_file_conversion(args):
    source_file, target_file, conversion_type = args.convert
    if conversion_type == 'csv_to_pdf':
        ff.csv_to_pdf(source_file, target_file)
    elif conversion_type == 'pdf_to_csv':
        ff.pdf_to_csv(source_file, target_file)
    # Add the other file conversions and list to user when called!
    # CSV to JSON
    elif conversion_type == 'csv_to_json':
        ff.csv_to_json(source_file, target_file)
    elif conversion_type == 'text_to_csv':
        ff.text_to_csv(source_file, target_file)
    elif conversion_type == 'json_to_csv':
        ff.json_to_csv(source_file, target_file)
    elif conversion_type == 'csv_to_text':
        ff.csv_to_text(source_file, target_file)
    elif conversion_type == 'pdf_to_text':
        ff.pdf_to_text(source_file, target_file)
    elif conversion_type == 'text_to_pdf':
        ff.text_to_pdf(source_file, target_file)
    else:
        print("Invalid conversion type.")
        return


def handle_add_want_format(args, user):
    if args.add_want_format:
        user.add_want_format(args.add_want_format)


def handle_add_convert_format(args, user):
    if args.add_convert_format:
        original_format, destination_formats = args.add_convert_format.split(',')
        destination_formats = destination_formats.split()
        user.add_convert_format(original_format, destination_formats)


# TODO: Reformat code below into new functions above, better readability and modularity

def main():
    parser = argparse.ArgumentParser(description='Interact with the Research API.')
    parser.add_argument('--register', nargs=2, help='Register a new user.')
    parser.add_argument('--login', nargs=2, help='Login as an existing user.')
    # parser.add_argument('--connect', action='store_true', help='Connect to the RabbitMQ server.')

    # New arguments...
    parser.add_argument('--add-want-format', type=str, help='Add a file format the user wants.')
    parser.add_argument('--add-convert-format', type=str, help='Add a file format the user can convert to.')
    parser.add_argument('--receive_messages', action='store_true', help='Receive any messages from the user\'s queue.')
    parser.add_argument('--send_message', nargs=2, help='Send a message to another user.')
    parser.add_argument('--convert', nargs=3, help='Convert a file from one format to another.')
    parser.add_argument('--upload', nargs=1, help='Upload a file.')
    parser.add_argument('--download', nargs=1, help='Download a file.')

    args = parser.parse_args()

    user = None
    if args.register:
        user = handle_user_registration(args)

    # Always attempt to connect to the RabbitMQ server when the script is run
    url = 'amqps://crnulcjb:jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x@shark.rmq.cloudamqp.com/crnulcjb'
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    try:
        connection = pika.BlockingConnection(pika.URLParameters(url))
        print("Successfully connected to the RabbitMQ server.")
    except pika.exceptions.AMQPConnectionError:
        print("Failed to connect to the RabbitMQ server.")
        return

    if args.login:
        user_id = handle_user_login(args)
        if user_id is None:
            return

    if args.convert:
        handle_file_conversion(args)


if __name__ == '__main__':
    main()

# final demo should have multiple clients connecting
# Can use fake data, one person uploads, one person converts, one person downloads etc.

# TODO: Previous stuff is below here, might be useful

#     parser.add_argument('--message', type=str, help='Specify a message to send.')
#     parser.add_argument('--add-file', type=str, help='Add a file to the user profile and announce it.')
#     parser.add_argument('--add-convert-format', nargs=2, help='Add a conversion format to the user profile.')
#     parser.add_argument('--start-listening', action='store_true', help='Start listening for messages.')
#     parser.add_argument('--get-received-file', action='store_true', help='Get the received file.')
#     parser.add_argument('--send-direct', nargs=2, help='Send a direct message to a specific user.')
#     parser.add_argument('--get-channel', action='store_true', help='Get the channel for the connection.')
#     parser.add_argument('--get-queue-name', action='store_true', help='Get the name of the queue for the connection.')
#     parser.add_argument('--convert-file', nargs=2, help='Convert a file from one format to another.')
#     parser.add_argument('--send-file', type=str, help='Send a file using the Magic Wormhole protocol.')
#     parser.add_argument('--receive-file', nargs=2, help='Receive a file using the Magic Wormhole protocol.')
#     # Add more arguments as necessary...

#     if args.user:
#         # Create a User instance with the specified ID
#         user = User(args.user)
#
#     if args.message:
#         # Create a Message instance and send it
#         message = Message(args.user, args.message)
#         api.connection.announce(message)
#
#     if args.add_file:
#         # Add a file to the user's profile and announce it
#         api.add_file(args.add_file)
#
#     if args.add_convert_format:
#         # Add a conversion format to the user's profile
#         original_format, destination_format = args.add_convert_format
#         api.add_convert_format(original_format, destination_format)
#
#     if args.start_listening:
#         # Start listening for messages
#         api.start_listening()
#
#     if args.get_received_file:
#         # Get the received file
#         received_file = api.get_received_file()
#         print(f'Received file: {received_file}')
#
#     if args.send_direct:
#         # Send a direct message to a specific user
#         message_text, user_id = args.send_direct
#         message = Message(args.user, message_text)
#         api.connection.direct(message, user_id)
#
#     if args.get_channel:
#         # Get the channel for the connection
#         channel = api.connection.get_channel()
#         print(f'Channel: {channel}')
#
#     if args.get_queue_name:
#         # Get the name of the queue for the connection
#         queue_name = api.connection.get_queue_name()
#         print(f'Queue name: {queue_name}')
#
#     if args.convert_file:
#         # Convert a file from one format to another
#         source_file, target_file = args.convert_file
#         csv_to_pdf(source_file, target_file)
#
#     if args.send_file:
#         # Send a file using the Magic Wormhole protocol
#         Wormhole.send(api.connection, args.user, Message(args.user, "Sending file"), args.send_file)
#
#     if args.receive_file:
#         # Receive a file using the Magic Wormhole protocol
#         command, filename = args.receive_file
#         Wormhole.receive(api.connection, Message(args.user, "Receiving file"), command, filename, args.user)
#
#     # Add more operations as necessary...
#     # args = parser.parse_args()
#     #
#     # if args.register:
#     #     user_id, password = args.register
#     #     api.register(user_id, password)
#     #
#     # if args.login:
#     #     user_id, password = args.login
#     #     api.login(user_id, password)
#     #
#     # if args.publish:
#     #     message_text, channel_or_queue = args.publish
#     #     api.publish(message_text, channel_or_queue)
#     #
#     # if args.add_format:
#     #     original_format, destination_format = args.add_format
#     #     api.add_format(original_format, destination_format)
