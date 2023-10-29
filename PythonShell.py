import tkinter as tk
import subprocess
from tkinter import simpledialog, Text, filedialog, messagebox
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
            run_jar.jar_func()
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
        message_label.pack()
        message_text = Text(root, height=5, width=40)
        message_text.pack()

        # Create a file upload button
        upload_button = tk.Button(root, text="Upload File", command=upload_file)
        upload_button.pack()
    except Exception as e:
        print(f"Could not connect to RabbitMQ, Error: {e}")


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
        # Upload button
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
root.geometry("400x400")
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
