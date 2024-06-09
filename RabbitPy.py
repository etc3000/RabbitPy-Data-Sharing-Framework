import argparse

from message.MagicWormhole import Wormhole
from message.Message import Message
from user.User import User
from message import *
from my_logging.Log import Log
import shell_application.File_Function as ff
from constants import Constants
from shell_application.user_list import user_credentials
from rmq.RabbitMQConnection import RabbitMQConnection
import pika
from urllib.parse import urlparse

rmq_connection = None


# def handle_user_registration(args):
#     user_id, password = args.register
#     user = User(user_id)
#     user_credentials[user_id] = password
#     print(f"User {user_id} registered successfully.")
#
#     # Registered user added to user_list.py
#     with open("user_list.py", "w") as user_base:
#         user_base.write(f"user_credentials = {user_credentials}")
#
#     return user
#
#
# def handle_user_login(args):
#     global rmq_connection
#     user_id, password = args.login
#     if user_id in user_credentials and password == user_credentials[user_id]:
#         print(f"User {user_id} logged in successfully.")
#         url = 'amqps://crnulcjb:jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x@shark.rmq.cloudamqp.com/crnulcjb'
#         try:
#             rmq_connection = pika.BlockingConnection(pika.URLParameters(url))
#             print("Successfully connected to the RabbitMQ server.")
#         except pika.exceptions.AMQPConnectionError:
#             print("Failed to connect to the RabbitMQ server.")
#             return None
#         return user_id
#     else:
#         print("Invalid username or password.")
#         return None
#
#
# def handle_file_conversion(args):
#     source_file, target_file, conversion_type = args.convert
#     if conversion_type == 'csv_to_pdf':
#         ff.csv_to_pdf(source_file, target_file)
#     elif conversion_type == 'pdf_to_csv':
#         ff.pdf_to_csv(source_file, target_file)
#     # Add the other file conversions and list to user when called!
#     # CSV to JSON
#     elif conversion_type == 'csv_to_json':
#         ff.csv_to_json(source_file, target_file)
#     elif conversion_type == 'text_to_csv':
#         ff.text_to_csv(source_file, target_file)
#     elif conversion_type == 'json_to_csv':
#         ff.json_to_csv(source_file, target_file)
#     elif conversion_type == 'csv_to_text':
#         ff.csv_to_text(source_file, target_file)
#     elif conversion_type == 'pdf_to_text':
#         ff.pdf_to_text(source_file, target_file)
#     elif conversion_type == 'text_to_pdf':
#         ff.text_to_pdf(source_file, target_file)
#     else:
#         print("Invalid conversion type.")
#         return
#
#
# def handle_add_want_format(username, format):
#     user = User(username)  # Assuming User class has been imported and user exists
#     user.add_want_format(format)
#     print(f"Format {format} has been added for user {username}.")
#
#
# def handle_add_convert_format(username, source_format, target_format):
#     user = User(username)  # Assuming User class has been imported and user exists
#     user.convert[source_format] = target_format.split()
#     print(f"Conversion format {source_format}:{target_format} has been added for user {username}.")
#
#
# def handle_upload(args):
#     if args.upload:
#         file_path = args.upload[0]
#         # Assuming a function to upload files exists
#         upload_file(file_path)
#
#
# def handle_download(args):
#     if args.download:
#         file_path = args.download[0]
#         # Assuming a function to download files exists
#         download_file(file_path)
#
#
# def handle_receive_file(args):
#     if args.receive_file:
#         command, filename = args.receive_file
#         Wormhole.receive(rmq_connection, Message(args.user, "Receiving file"), command, filename, args.user)
#
#
# def handle_send_message(args, rmq_connection):
#     if args.send_message:
#         message_text, user_id = args.send_message
#         message = Message(args.user, message_text)
#         rmq_connection.direct(message, user_id)
#
#
# def handle_magic_wormhole(args):
#     if args.magicwormhole:
#         file_path, user_id = args.magicwormhole
#         Wormhole.send(rmq_connection, user_id, Message(user_id, "Sending file"), file_path)
#
#
# def handle_close_connection(args):
#     global rmq_connection
#     if args.close_connection and rmq_connection:
#         rmq_connection.close()
#         rmq_connection = None
#         print("Connection to the RabbitMQ server has been closed.")
# -------------------------------------------------------------
'''Operation Handling Functions'''


def handle_user_registration(user_id, password):
    user = User(user_id)
    user_credentials[user_id] = password
    print(f"User {user_id} registered successfully.")

    # Registered user added to user_list.py
    with open("user_list.py", "w") as user_base:
        user_base.write(f"user_credentials = {user_credentials}")

    return user


def handle_user_login(user_id, password):
    global rmq_connection
    if user_id in user_credentials and password == user_credentials[user_id]:
        print(f"User {user_id} logged in successfully.")
        url = 'amqps://crnulcjb:jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x@shark.rmq.cloudamqp.com/crnulcjb'
        try:
            rmq_connection = pika.BlockingConnection(pika.URLParameters(url))
            print("Successfully connected to the RabbitMQ server.")
        except pika.exceptions.AMQPConnectionError:
            print("Failed to connect to the RabbitMQ server.")
            return None
        return user_id
    else:
        print("Invalid username or password.")
        return None


def handle_file_conversion(source_file, target_file, conversion_type):
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


def handle_add_want_format(username, format):
    user = User(username)  # Assuming User class has been imported and user exists
    user.add_want_format(format)
    print(f"Format {format} has been added for user {username}.")


def handle_add_convert_format(username, source_format, target_format):
    user = User(username)  # Assuming User class has been imported and user exists
    # user.convert[source_format] = target_format.split()
    # print(f"Conversion format {source_format}:{target_format} has been added for user {username}.")
    user.add_convert_format(source_format, target_format)
    print(f"Conversion format {source_format}:{target_format} has been added for user {username}.")


def handle_upload(file_path):
    # Assuming a function to upload files exists
    upload_file(file_path)


def handle_download(file_path):
    # Assuming a function to download files exists
    download_file(file_path)


# def handle_receive_file():
#     command, filename = input("Enter command and filename (separated by space): ").split()
#     Wormhole.receive(rmq_connection, Message(args.user, "Receiving file"), command, filename, args.user)
#
#
# def handle_send_message(message_text, user_id):
#     message = Message(args.user, message_text)
#     rmq_connection.direct(message, user_id)
#
#
# def handle_magic_wormhole(file_path, user_id):
#     Wormhole.send(rmq_connection, user_id, Message(user_id, "Sending file"), file_path)

def handle_receive_file():
    command, filename = input("Enter command and filename (separated by space): ").split()
    user = input("Enter user: ")
    Wormhole.receive(rmq_connection, Message(user, "Receiving file"), command, filename, user)


def handle_send_message(message_text, user_id):
    user = input("Enter user: ")
    message = Message(user, message_text)
    rmq_connection.direct(message, user_id)


def handle_magic_wormhole(file_path, user_id):
    user = input("Enter user: ")
    Wormhole.send(rmq_connection, user_id, Message(user, "Sending file"), file_path)


def handle_close_connection():
    global rmq_connection
    if rmq_connection:
        rmq_connection.close()
        rmq_connection = None
        print("Connection to the RabbitMQ server has been closed.")


# -------------------------------------------------------------
''' Data Operation Functions '''


def check_user_formats(username):
    user = User(username)  # Assuming User class has been imported and user exists
    print(f"User {username} wants these formats: {user.want_formats}")
    print(f"User {username} can convert these formats: {user.convert_formats}")


def upload_file(channel, routing_key, file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    channel.basic_publish(
        exchange='',
        routing_key=routing_key,
        body=file_data,
        properties=pika.BasicProperties(
            content_type='application/octet-stream',
            delivery_mode=2
        )
    )


def download_file(channel, queue_name, file_path):
    method_frame, properties, body = channel.basic_get(queue_name)
    if method_frame:
        with open(file_path, 'wb') as file:
            file.write(body)
        channel.basic_ack(method_frame.delivery_tag)


# -------------------------------------------------------------
# TODO: Construct a persistent connection that allows for multiple commands without KeyboardInterrupt
# TODO: Ask user for command line, console, or GUI version upon script launch?
'''Main Function'''


def main():
    global rmq_connection
    # parser = argparse.ArgumentParser(description='Interact with the Research API.')
    # parser.add_argument('--register', nargs=2, help='Register a new user.')
    # parser.add_argument('--login', nargs=2, help='Login as an existing user.')
    # # parser.add_argument('--add-want-format', type=str, help='Add a file format the user wants.')
    # parser.add_argument('--add-want-format', nargs=2, metavar=('username', 'format'),
    #                     help='Add a file format the user wants.')
    #
    # # parser.add_argument('--add-convert-format', type=str, help='Add a file format the user can convert to.')
    # parser.add_argument('--add-convert-format', nargs=3, metavar=('username', 'source_format', 'target_format'),
    #                     help='Add a file format the user can convert to.')
    #
    # # might be a good idea to be able to remove formats as well
    #
    # parser.add_argument('--receive_messages', action='store_true', help='Receive any messages from the user\'s queue.')
    # parser.add_argument('--send_message', nargs=2, help='Send a message to another user.')
    # parser.add_argument('--convert', nargs=3, help='Convert a file from one format to another.')
    # parser.add_argument('--upload', nargs=1, help='Upload a file.')
    # parser.add_argument('--download', nargs=1, help='Download a file.')
    # parser.add_argument('--magicwormhole', nargs=2, help='Choose file to send to another user')
    # parser.add_argument('--close_connection', action='store_true', help='Close the connection to the RabbitMQ server.')
    #
    # args = parser.parse_args()
    #
    # user = None
    # if args.register:
    #     user = handle_user_registration(args)

    # try:
    #     if args.login:
    #         user_id = handle_user_login(args)
    #         if user_id is None:
    #             return
    #
    #     while True:
    #         # user_command = input("Enter a command: ")
    #         if args.convert:
    #             # user_command = 'convert'
    #             handle_file_conversion(args)
    #
    #         elif args.add_want_format:
    #             # user_command = 'add_want_format'
    #             username, format = args.add_want_format
    #             handle_add_want_format(username, format)
    #
    #         elif args.add_convert_format:
    #             username, source_format, target_format = args.add_convert_format
    #             handle_add_convert_format(username, source_format, target_format)
    #
    #         elif args.upload:
    #             handle_upload(args)
    #
    #         elif args.download:
    #             handle_download(args)
    #
    #         elif args.receive_messages:
    #             handle_receive_file(args)
    #
    #         elif args.send_message:
    #             handle_send_message(args, rmq_connection)
    #
    #         elif args.magicwormhole:
    #             handle_magic_wormhole(args)
    #
    #         elif args.close_connection:
    #             handle_close_connection(args, rmq_connection)
    #
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    try:
        while True:
            command = input("Enter command:\n"
                            "\tregister\n"
                            "\tlogin\n"
                            "\tconvert\n"
                            "\tadd-want-format\n"
                            "\tadd-convert-format\n"
                            "\tupload\n"
                            "\tdownload\n"
                            "\treceive_messages\n"
                            "\tsend_message\n"
                            "\tmagicwormhole\n"
                            "\tclose_connection\n")

            if command == 'register':
                user_id, password = (
                    input("Enter user_id and password (separated by space): ").split())
                user = handle_user_registration(user_id, password)

            elif command == 'login':
                user_id, password = input("Enter user_id and password (separated by space): ").split()
                user_id = handle_user_login(user_id, password)
                if user_id is None:
                    return

            elif command == 'convert':
                source_file, target_file, conversion_type = (
                    input("Enter source_file, target_file, conversion_type (separated by space): ").split())
                handle_file_conversion(source_file, target_file, conversion_type)

            elif command == 'add-want-format':
                username, format = (
                    input("Enter username and format (separated by space): ").split())
                handle_add_want_format(username, format)

            elif command == 'add-convert-format':
                username, source_format, target_format = (
                    input("Enter username, source_format, target_format (separated by space): ").split())
                handle_add_convert_format(username, source_format, target_format)

            elif command == 'upload':
                file_path = input("Enter file_path: ")
                handle_upload(file_path)

            elif command == 'download':
                file_path = input("Enter file_path: ")
                handle_download(file_path)

            elif command == 'receive_messages':
                handle_receive_file()

            elif command == 'send_message':
                message_text, user_id = (
                    input("Enter message_text and user_id (separated by space): ").split())
                handle_send_message(message_text, user_id, rmq_connection)

            elif command == 'magicwormhole':
                file_path, user_id = (
                    input("Enter file_path and user_id (separated by space): ").split())
                handle_magic_wormhole(file_path, user_id)

            elif command == 'close_connection':
                handle_close_connection()

            elif command == 'check_formats':
                username = input("Enter username: ")
                check_user_formats(username)

            else:
                print("Invalid command.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()

'''
# final demo should have multiple clients connecting
# Can use fake data, one person uploads, one person converts, one person downloads etc.

# Successful registration
# Successful login
# Successful add-want
# Not successful add-conversion

# Test file upload
# Test file download
# Test file conversion
# Test message sending
# Test message receiving
# Test magic wormhole
# Test close connection
'''
