import tkinter as tk
from tkinter import Text, filedialog, messagebox
import pika
import hashlib

import run_jar
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
        result_label.config("No matching username found")


def rmq_connect():
    global rmq_connection
    cloudamqp_uri = "amqps://crnulcjb:jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x@shark.rmq.cloudamqp.com/crnulcjb"
    try:
        rmq_connection = pika.BlockingConnection(pika.URLParameters(cloudamqp_uri))
        channel = rmq_connection.channel()
        channel.queue_declare(queue='My Queue')
        print("Connected to RMQ_APP_Testing")
        # rmq_connect_button.pack_forget()
        disconnect_button = tk.Button(root, text="Disconnect from RabbitMQ", command=disconnect_rmq)
        disconnect_button.pack()

        user_id = username_entry.get()
        message = f"User: {user_id} has connected."
        channel.basic_publish(exchange='', routing_key='My Queue', body=message)

        # Create a text box for entering messages
        message_label = tk.Label(root, text="Enter your message:")
        # Drop-down for message type
        # Select recipient of message
        # List of queues
        message_label.pack()
        message_text = Text(root, height=5, width=20)
        message_text.pack()

        send_button = tk.Button(root, text="Send text to RabbitMQ", command=send_data)
        send_button.pack()

        queue_select = tk.Button(root, text="Please select your queue", command=queue_menu)

        # Create a file upload button, supports csv and pdf
        upload_button = tk.Button(root, text="Upload File", command=upload_file)
        upload_button.pack()

        # Once file is uploaded, display name and size
        # upload_label = tk.Label(root, text = "File Name: " + file_name)
        # upload_label.pack()
    except Exception as e:
        print(f"Could not connect to RabbitMQ, Error: {e}")


def queue_menu():
    # Pings RMQ for queues: My Queue, General, direct user message, etc.
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
    username_label.pack_forget()
    username_entry.pack_forget()
    password_label.pack_forget()
    password_entry.pack_forget()
    login_button.pack_forget()
    result_label.pack_forget()

    # Display metadata on right hand side
    rmq_connect_button = tk.Button(root, text="Connect to RabbitMQ", command=rmq_connect)
    rmq_connect_button.pack()


# Create the main window
root = tk.Tk()
root.title("RabbitMQ Messenger")
root.geometry("600x600")
# Need to resize

rmq_img = tk.PhotoImage(file="C:/Users/Tedio/PycharmProjects/RabbitMG_GUI/rabbitmq_logo-1105942957.png")

# Create and configure widgets
rmq_img_label = tk.Label(root, image=rmq_img)
username_label = tk.Label(root, text="Username:")
username_entry = tk.Entry(root)
password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, show="*")  # Hide the password as asterisks
login_button = tk.Button(root, text="Login", command=login)
result_label = tk.Label(root, text="")

add_user_button = tk.Button(root, text="Register a New User", command=user_management.user_register)
add_user_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Place widgets in the window
rmq_img_label.pack()

username_label.pack()
username_entry.pack()

password_label.pack()
password_entry.pack()

login_button.pack()
result_label.pack()

# Start the main event loop
root.mainloop()

"""
- Connect/Disconnect on the top left
- File Formats on bottom left
- Messaging and file upload in Center
- Queue Selection on top right
- Server info and meta data on bottom right

- Incoming message feed for user?
- Sent messages?
"""