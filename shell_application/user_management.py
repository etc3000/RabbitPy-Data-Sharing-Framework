from tkinter import simpledialog
import hashlib

from shell_application import user_list


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

# forgot password
# verify user exists, then allow to reset, update in user_list.py
# redo for command line version, allow user to register with user name and password
# want to connect with regular password, not the hashed one stored in user_list
