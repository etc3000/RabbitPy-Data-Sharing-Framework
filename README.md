# Thesis-PythonShell
Python Shell Application

This project is thesis research extending previous work on a RabbitMQ messaging system for science users to exchange data with one another


Original project can be found at: https://github.com/Andrew-Nguyen-2/Thesis-Research-API

Iterative Development on Java Portions: https://github.com/etc3000/Thesis-Research-API/blob/main/README.md

Python App Structure
------
Opening App

Login Button
	Enter Username/Password
	Register
		Create Username/Password, stored in users.py or remote host
-----
After Login

Connect Button
-----
Connected to RMQ		

Choose Message Format / Type

	Queue Selection
		My Queue, General Queue, other user's queue
			Find user?
	Upload Message Button

	Send Message Box
		Sends to RMQ / Performs file transfer if file is uploaded

	Metadata / Server Info
		Displayed on side as text / JSON

	Convert Data Formats
		Run conversion methods, produce a new file for download?

	Disconnect
		Confirm Disconnect
-----
Server-Side
	Receive messages upon connect/disconnect
	Receive messages in 
