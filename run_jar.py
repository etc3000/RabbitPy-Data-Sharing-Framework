import tkinter as tk
from tkinter import Text, filedialog, messagebox
import pika
import hashlib
import subprocess

from PythonShell import rmq_connect, result_label


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
