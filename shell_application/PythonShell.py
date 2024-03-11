import subprocess
import tkinter as tk
from tkinter import Text, filedialog, messagebox
import pika
import hashlib

import user_management

import user_list

# Optimize later
# Might want to separate functions into files
rmq_connection = None
disconnect_button = None
rmq_connect_button = None


def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in user_list.user_credentials:  # password hash can be stored on host server?
        stored_password_hash = user_list.user_credentials[username]
        computed_password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        if stored_password_hash == computed_password_hash:
            result_label.config(text="User successfully validated")
            # run_jar.jar_func()
            # need to better define jar funcs first, for now just login
            update_gui_after_login()
        else:
            result_label.config(text="Invalid credentials, please try again")
    else:
        result_label.config(text="No matching username found")


def rmq_connect():
    global rmq_connection
    cloudamqp_uri = "amqps://crnulcjb:jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x@shark.rmq.cloudamqp.com/crnulcjb"
    try:
        rmq_connection = pika.BlockingConnection(pika.URLParameters(cloudamqp_uri))
        channel = rmq_connection.channel()
        channel.queue_declare(queue='My Queue')
        print("Connected to RMQ_APP_Testing")
        # rmq_connect_button.pack_forget()

        user_id = username_entry.get()
        message = f"User: {user_id} has connected."
        channel.basic_publish(exchange='', routing_key='My Queue', body=message)

        # Create a text box for entering messages
        message_label = tk.Label(root, text="Enter your message:")
        message_label.grid(row=1, column=2, padx=10, pady=10)
        message_text = Text(root, height=5, width=20)
        message_text.grid(row=2, column=2, padx=10, pady=10)

        # Send button
        send_button = tk.Button(root, text="Send text to RabbitMQ", command=send_data)
        send_button.grid(row=3, column=2, padx=10, pady=10)

        # Queue selection and file format menus
        queue_select_button = tk.Button(root, text="Select Queue", command=queue_menu)
        queue_select_button.grid(row=0, column=3, padx=10, pady=10)

        file_format_menu = tk.OptionMenu(root, "File Format", "CSV", "PDF")  # Add more options as needed
        file_format_menu.grid(row=1, column=1, padx=10, sticky="ne")

        request_format_menu = tk.OptionMenu(root, "Request Format", "CSV", "PDF")  # Add more options as needed
        request_format_menu.grid(row=1, column=3, padx=10, pady=10)

        disconnect_button = tk.Button(root, text="Disconnect from RabbitMQ", command=disconnect_rmq)
        disconnect_button.grid(row=4, column=3, padx=10, pady=10)

    except Exception as e:
        print(f"Could not connect to RabbitMQ, Error: {e}")


def queue_menu():
    # Pings RMQ for queues: My Queue, General, direct user message, etc.
    proc = subprocess.Popen("/usr/sbin/rabbitmqctl list_queues", shell=True, stdout=subprocess.PIPE)
    stdout_value = proc.communicate()[0]
    print(stdout_value)
    return


def send_data():
    # this function gathers meta_data and sends a formatted message to RabbitMQ
    # send to specified queue
    return


def magic_wormhole():
    # perform file transfer
    return


def disconnect_rmq():
    global rmq_connection
    try:
        if rmq_connection:
            channel = rmq_connection.channel()
            username = username_entry.get()
            message = f"User {username} disconnected"
            channel.basic_publish(exchange='', routing_key='My Queue', body=message)
            rmq_connection.close()
            rmq_connection = None
            # kill app or return to login screen
    except Exception as e:
        print(f"Could not disconnect from RabbitMQ, Error: {e}")


def settings_toolbar():
    """
    Contains an about section, possible settings, etc.
    """
    return


def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("PDF Files", "*.pdf")])
    if file_path:
        messagebox.showinfo("File Uploaded", f"File {file_path} has been uploaded.")
        # Upload button, remember the size limit
        # MagicWormhole transfer


def update_gui_after_login():
    """
    Screen after a successful login
    """
    username_label.grid_forget()
    username_entry.grid_forget()
    password_label.grid_forget()
    password_entry.grid_forget()
    login_button.grid_forget()
    result_label.grid_forget()

    # CloudAMQP information (top left)
    cloudamqp_info_label = tk.Label(root, text="CloudAMQP Info")
    cloudamqp_info_label.grid(row=0, column=0, sticky="nw")

    # Text message input (center)
    message_label = tk.Label(root, text="Enter your message:")
    message_label.grid(row=1, column=0, padx=10)
    message_text = Text(root, height=5, width=20)
    message_text.grid(row=2, column=0, padx=10)

    # Send button
    send_button = tk.Button(root, text="Send text to RabbitMQ", command=send_data)
    send_button.grid(row=3, column=0, padx=10)

    # Queue selection and file format menus
    queue_select_button = tk.Button(root, text="Select Queue", command=queue_menu)
    queue_select_button.grid(row=0, column=1, padx=10, sticky="ne")

    file_format_menu = tk.OptionMenu(root, "File Format", "CSV", "PDF")  # Add more options as needed
    file_format_menu.grid(row=1, column=1, padx=10, sticky="ne")

    request_format_menu = tk.OptionMenu(root, "Request Format", "CSV", "PDF")  # Add more options as needed
    request_format_menu.grid(row=2, column=1, padx=10, sticky="ne")

    disconnect_button = tk.Button(root, text="Disconnect from RabbitMQ", command=disconnect_rmq)
    disconnect_button.grid(row=0, column=0, sticky="nw", padx=10)


# Create the main window
root = tk.Tk()
root.title("RabbitMQ Messenger")
root.geometry("600x600")

rmq_img = tk.PhotoImage(file="rabbitmq_logo-1105942957.png")

# Create and configure widgets
rmq_img_label = tk.Label(root, image=rmq_img)
username_label = tk.Label(root, text="Username:")
username_entry = tk.Entry(root)
password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, show="*")
login_button = tk.Button(root, text="Login", command=login)
result_label = tk.Label(root, text="")

add_user_button = tk.Button(root, text="Register a New User", command=user_management.user_register)

# Place widgets in the window using grid
rmq_img_label.grid(row=0, column=0, padx=10, pady=10)

username_label.grid(row=1, column=0, padx=10, pady=10)
username_entry.grid(row=1, column=1, padx=10, pady=10)

password_label.grid(row=2, column=0, padx=10, pady=10)
password_entry.grid(row=2, column=1, padx=10, pady=10)

login_button.grid(row=3, column=0, padx=10, pady=10)
result_label.grid(row=3, column=1, padx=10, pady=10)

add_user_button.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

# Start the main event loop
root.mainloop()

"""
- Connect/Disconnect on the top left
- File Formats on bottom left
- Messaging and file upload in Center
- Queue Selection on top right
- Server info and meta data on bottom right
- Meta data will be converted into JSON and sent to RMQ

- Incoming message feed for user?
- Sent messages?
- Start listening once connected to RMQ


From Nguyen -
User ID - The ID of the user sending the message.
Message ID - The ID of the message.
Message Type - The type relevant to the message.
Data - The name(s) and size(s) of the data file(s).
Data Convert Formats - The formats the user can convert to and from.
Data Request Formats - The formats the user can read.
Timestamp - The time the message was sent in UTC format.
Origin Message ID - The message ID this message relates to or is in response to.
Source User ID - The user ID this message relates to or is in response to.
These fields are automatically filled from the information the user supplied when
implementing the API and by relevant messages the user receives. The only fields that
exist with every message sent are user id, message id, message type, and timestamp,
the others are only needed for announcing the generated data and data requests.
"""
