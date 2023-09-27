import tkinter as tk
import subprocess
from tkinter import simpledialog
import pika
import hashlib

import user_list


# Optimize later
# Might want to separate functions into files

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in user_list.user_credentials:  # password hash can be stored on host server?
        stored_password_hash = user_list.user_credentials[username]
        computed_password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        if stored_password_hash == computed_password_hash:
            result_label.config(text="User successfully validated")
            jar_func()
            update_gui_after_login()
        else:
            result_label.config(text="Invalid credentials, please try again")
    else:
        result_label.config("No matching username found")


def jar_func():
    """
    Run API upon button press?
    """
    # Replace with actual JAR file
    jar_file_path = "C:/Users/Tedio/eclipse-workspace/Thesis-Research-API/research.jar"

    try:
        # Use the 'java' command to run the JAR file
        subprocess.run(['java', '-jar', jar_file_path], check=True)
    except subprocess.CalledProcessError as e:
        result_label.config(text=f"Error running JAR file: {e}")
        rmq_connect()


def rmq_connect():
    """
    Button that handles connecting to RabbitMQ server
    - Need to add option to close connection
    """
    cloudamqp_uri = "amqps://crnulcjb:jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x@shark.rmq.cloudamqp.com/crnulcjb"
    try:
        rmq_connection = pika.BlockingConnection(pika.URLParameters(cloudamqp_uri))
        channel = rmq_connection.channel()

        channel.queue_declare(queue='My Queue')
        # "ping" RabbitMQ to confirm a connection

        # publish a test message

        # Entry box for message, select format boxes, etc.

        print("Connected to RMQ_APP_Testing")

        rmq_connection.close()
    except Exception as e:
        print(f"Could not connect to RabbitMQ, Error: {e}")


def settings_toolbar():
    """
    Contains an about section, possible settings, etc.
    """
    return


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


def user_register():
    """
    - Registers a new username and hashed password
    - Need to make sure to check for duplicates
    - Possible password rules?
    """
    new_user = simpledialog.askstring("Add New User", "Please enter a username")
    new_user_pass = simpledialog.askstring("Add New User", "Please enter a password")
    new_password_hash = hashlib.sha256(new_user_pass.encode('utf-8')).hexdigest()
    user_list.user_credentials[new_user] = new_password_hash
    with open("user_list.py", "w") as user_base:
        user_base.write(f"user_credentials = {user_list.user_credentials}")


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

add_user_button = tk.Button(root, text="Register a New User", command=user_register)
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
