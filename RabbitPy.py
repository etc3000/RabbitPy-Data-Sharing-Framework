# -------------------------------------------------------------
# 1. Import Statements
import argparse
import json
import os
from message.MagicWormhole import Wormhole
from message.Message import Message
from user.User import User
from message import *
from my_logging.Log import Log
import shell_application.File_Function as ff
from constants import Constants
from user_list import user_credentials
from rmq.RabbitMQConnection import RabbitMQConnection
import pika
from urllib.parse import urlparse

# -------------------------------------------------------------
# 2. Global Variables
rmq_connection = None
ALLOWED_FORMATS = ['.pdf', '.csv', '.txt', '.json', '.jpg', '.png', '.jpeg', '.gif', '.bmp', '.tiff', '.svg']
FORMAT_CONVERSIONS = ['csv_to_pdf', 'pdf_to_csv', 'csv_to_json', 'text_to_csv', 'json_to_csv', 'csv_to_text',
                      'pdf_to_text', 'text_to_pdf']
user_formats = {}


# -------------------------------------------------------------
# 3. User Registration and Login Functions
def publish_login_message(user_id, action):
    global rmq_connection
    channel = rmq_connection.channel()
    channel.queue_declare(queue='login')
    message = f"User {user_id} has {action} the system."
    channel.basic_publish(exchange='', routing_key='login', body=message)
    print(f"Message sent: {message}")


def handle_user_registration(user_id, password):
    user = User(user_id)
    user_formats[user_id] = user  # Add the user to the user_formats dictionary

    # Add new user
    user_credentials[user_id] = password
    print(f"User {user_id} registered successfully.")
    publish_login_message(user_id, "registered")

    create_user_queue(user_id)
    # Save updated user list
    with open("user_credentials.json", "w") as user_base:
        json.dump(user_credentials, user_base)
        # JSON here will save our user info over multiple sessions
    return user


def handle_user_login(user_id, password):
    with open("user_credentials.json", "r") as user_base:
        user_credentials = json.load(user_base)

    if user_id in user_credentials and password == user_credentials[user_id]:
        url = 'amqps://crnulcjb:jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x@shark.rmq.cloudamqp.com/crnulcjb'
        try:
            rmq_connection = pika.BlockingConnection(pika.URLParameters(url))
            print("Successfully connected to the RabbitMQ server.")
            publish_login_message(user_id, "has logged in")

        except pika.exceptions.AMQPConnectionError:
            print("Failed to connect to the RabbitMQ server.")
            return None

        user = User(user_id)
        user_formats[user_id] = user

        # Load the user's want formats from a JSON file if it exists
        want_formats_file = f"{user_id}_want_formats.json"
        if os.path.exists(want_formats_file):
            with open(want_formats_file, "r") as file:
                user.want_formats = json.load(file)

        # Load the user's convert formats from a JSON file if it exists
        convert_formats_file = f"{user_id}_convert_formats.json"
        if os.path.exists(convert_formats_file):
            with open(convert_formats_file, "r") as file:
                user.convert_formats = json.load(file)

        return user_id

    else:
        print("Invalid username or password.")
        return None


# -------------------------------------------------------------
# 4. File Conversion Functions
def handle_file_conversion(source_file, target_file, conversion_type):
    source_file = 'example/' + source_file
    target_file = 'example/' + target_file
    # example is where we want all of our files to go (for now)
    if conversion_type == 'csv_to_pdf':
        ff.csv_to_pdf(source_file, target_file)
    elif conversion_type == 'pdf_to_csv':
        ff.pdf_to_csv(source_file, target_file)
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
        if conversion_type == 'text_to_pdf':
            with open(source_file, 'r', encoding='utf-8') as file:
                text = file.read()
            ff.text_to_pdf(text, target_file)
    else:
        print("Invalid conversion type.")
        return


# -------------------------------------------------------------
# 5. Format Handling Functions
def handle_add_want_format(username, format):
    # print('Supported formats: ', Constants.ALLOWED_FORMATS)
    if username not in user_formats:
        print(f"User {username} does not exist.")
        return

    if format in ALLOWED_FORMATS:
        user = user_formats[username]  # Assuming User class has been imported and user exists
        user.add_want_format(format)
        print(f"Format {format} has been added for user {username}.")

        # Save the user's want formats to a JSON file
        with open(f"{username}_want_formats.json", "w") as file:
            json.dump(user.want_formats, file)

    else:
        print(f"Invalid format. Please choose from the following: {ALLOWED_FORMATS}")


def handle_add_convert_format(username):
    if username not in user_formats:
        print(f"User {username} does not exist.")
        return

    user = user_formats[username]  # Fetch the user from the user_formats dictionary
    # if username not in user_credentials:
    #     print(f"User {username} does not exist.")
    #     return

    print("Select a conversion format:")
    for i, format in enumerate(FORMAT_CONVERSIONS, start=1):
        print(f"{i}. {format}")

    format_index = int(input("Enter the number of your choice: ")) - 1
    format_choice = FORMAT_CONVERSIONS[format_index]

    source_format, target_format = format_choice.split('_to_')
    user.add_convert_format("." + source_format, "." + target_format)

    # Save the user's convert formats to a JSON file
    with open(f"{username}_convert_formats.json", "w") as file:
        json.dump(user.convert_formats, file)


# -------------------------------------------------------------
# 6. Upload and Download Functions
def handle_upload(user_id, file_path):
    # Extract the file extension
    file_extension = os.path.splitext(file_path)[1]

    # Check against the want_formats of all users
    for user in user_formats.values():
        if file_extension in user.want_formats:
            # Send a notification to the user
            notification = f"User {user_id} has uploaded a file with a format you want: {file_path}"
            rmq_connection.direct(notification, user.user_id)

    # Upload the file
    upload_file(file_path, user_id)


def handle_download(queue_name):
    # Download a message from the queue
    message = download_message(queue_name)
    print(f"Downloaded message: {message}")


# -------------------------------------------------------------
# 7. Message Handling Functions
def handle_receive_file():
    command, filename = input("Enter command and filename (separated by space): ").split()
    user = input("Enter user: ")
    Wormhole.receive(rmq_connection, Message(user, "Receiving file"), command, filename, user)


def handle_send_message(message_text, user_id):
    channel = rmq_connection.channel()  # Assuming rmq_connection is your RabbitMQ connection
    channel.queue_declare(queue=user_id)  # Declare a queue
    channel.basic_publish(exchange='', routing_key=user_id, body=message_text)  # Publish a message to the queue


def handle_magic_wormhole(file_path, user_id):
    recipient_user_id = input("Enter recipient user ID: ")
    Wormhole.send(rmq_connection, user_id, Message(user_id, "Sending file"), file_path, recipient_user_id)


def handle_close_connection():
    global rmq_connection
    if rmq_connection:
        rmq_connection.close()
        rmq_connection = None
        print("Connection to the RabbitMQ server has been closed.")
        return


# -------------------------------------------------------------
# 8. Data Operation Functions
def check_user_formats(username):
    with open("user_credentials.json", "r") as user_base:
        user_credentials = json.load(user_base)

        if username not in user_credentials:
            print(f"User {username} does not exist.")
            return

        user = User(username)
        user_formats[username] = user

        # Load the user's want formats from a JSON file
        want_formats_file = f"{username}_want_formats.json"
        if os.path.exists(want_formats_file):
            with open(want_formats_file, "r") as file:
                user.want_formats = json.load(file)
                print(f"User {username} wants these formats: {user.want_formats}")

        # Load the user's convert formats from a JSON file
        convert_formats_file = f"{username}_convert_formats.json"
        if os.path.exists(convert_formats_file):
            with open(convert_formats_file, "r") as file:
                user.convert_formats = json.load(file)
                print(f"User {username} can convert these formats: {user.convert_formats}")


def upload_file(file_path, user_id):
    queue_name = f'{user_id}'  # The queue name is based on the user_id
    exchange_name = ''  # Using the default exchange
    channel = rmq_connection.channel()  # Assuming rmq_connection is your RabbitMQ connection
    with open(file_path, 'rb') as file:
        file_data = file.read()
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=queue_name,
        body=file_data,
        properties=pika.BasicProperties(
            content_type='application/octet-stream',
            delivery_mode=2,
            headers={'filename': os.path.basename(file_path)}
        )
    )


def download_message(queue_name):
    # This method should retrieve a message from the specified queue
    channel = rmq_connection.channel()  # Assuming rmq_connection is your RabbitMQ connection
    method_frame, properties, body = channel.basic_get(queue_name)
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        filename= properties.headers['filename']
        with open(filename, 'wb') as file:
            file.write(body)
        print(f"Downloaded message and saved to file: {filename}")
        # return body.decode('utf-8')
    else:
        print("No messages in the queue.")
        return None


def create_user_queue(user_id):
    global rmq_connection
    channel = rmq_connection.channel()
    channel.queue_declare(queue=user_id)
    message = "Queue {" + user_id + "} has been created"
    channel.basic_publish(exchange='', routing_key='user_id', body=message)


# -------------------------------------------------------------
# 9. Main Function
# TODO: Ask user for command line, console, or GUI version upon script launch?

def main():
    global rmq_connection
    url = 'amqps://crnulcjb:jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x@shark.rmq.cloudamqp.com/crnulcjb'
    try:
        rmq_connection = pika.BlockingConnection(pika.URLParameters(url))
        print("Successfully connected to the RabbitMQ server.")
    except pika.exceptions.AMQPConnectionError:
        print("Failed to connect to the RabbitMQ server.")
        return

    print("Welcome to the RabbitPy Data-Sharing Framework! \n"
          "Please select an interface to begin.\n")

    user_id = None
    while user_id is None:
        command = input("Enter command:\n"
                        "register \t login \t close_connection\n")

        if command == 'register':
            user_id = input("Please create a user_id: ")
            password = input("Please create a password: ")
            handle_user_registration(user_id, password)

        elif command == 'login':
            user_id = input("Enter user_id: ")
            password = input("Enter password: ")
            user_id = handle_user_login(user_id, password)
            if user_id is None:
                print("Invalid username or password.")

        elif command == 'close_connection':
            return

        else:
            print("Invalid command.")

    try:
        while True:
            command = input("Enter command:\n\tconvert | add-want-format | add-convert-format | check_formats\n"
                            "\tupload | download | receive_messages | send_message | magicwormhole\n"
                            "\tclose_connection\n")

            if command == 'convert':
                source_file = input("Enter source_file: ")
                target_file = input("Enter target_file: ")
                conversion_type = input("Enter conversion_type: ")
                handle_file_conversion(source_file, target_file, conversion_type)

            elif command == 'add-want-format':
                want_format = input("Enter format: ")
                handle_add_want_format(user_id, want_format)

            elif command == 'add-convert-format':
                handle_add_convert_format(user_id)

            elif command == 'upload':
                # Upload a file to RabbitMQ
                print("RABBITMQ HAS A STRICT 2GB SIZE LIMIT, USE MAGICWORMHOLE FOR LARGER FILES!\n")
                file_path = input("Enter file_path: ")
                if os.path.getsize(file_path) > 2 * 1024 * 1024 * 1024:
                    print("The file is too large for RabbitMQ. Please use MagicWormhole.")

                else:
                    file_path = file_path.replace('"', '')
                    handle_upload(user_id, file_path)

            elif command == 'download':
                download_queue = input("Enter queue name to download from: ")
                # select queue to download from
                handle_download(download_queue)

            elif command == 'receive_messages':
                handle_receive_file()

            elif command == 'send_message':
                user_id_to_send = input("Enter recipient's user_id: ")
                message_text = input("Enter message_text: ")
                handle_send_message(message_text, user_id_to_send)

            elif command == 'magicwormhole':
                file_path = input("Enter file_path: ")
                user_id_to_send = input("Enter user_id to send file to: ")
                handle_magic_wormhole(file_path, user_id_to_send)

            elif command == 'close_connection':
                handle_close_connection()
                user_id = None
                break

            elif command == 'check_formats':
                username_to_check = input("Enter username to check formats for: ")
                check_user_formats(username_to_check)

            else:
                print("Invalid command.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
'''
# final demo should have multiple clients connecting
# Can use fake data, one person uploads, one person converts, one person downloads etc.


# Test file upload
# Test file download
# Test file conversion
# Test message sending 
# Test message receiving
# Test magic wormhole

# Send message in RMQ to other user
Check formats might want to specify which user to check formats for other than yourself
'''
