__author__ = 'ludwig'
#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
host = "192.168.1.66:12345"
#port = 12345                # Reserve a port for your service.

s.connect((host))
print "Response from server; " + s.recv(1024)
s.send("here's some data!")


s.close                     # Close the socket when done

