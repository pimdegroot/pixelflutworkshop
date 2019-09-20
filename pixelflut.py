import socket               # Import the library needed to create socket connections

HOST='127.0.0.1'            # Fill in the ip of the server, or an address like pixelflut.event.thereality.nl
PORT=1234                   # Fill in the port, this is usually 1234

x = 1                       # The X coordinate of the pixel
y = 1                       # The Y coordinate
r = 255                     # The Red color value
g = 255                     # The Green color value
b = 255                     # the Blue color value

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket
sock.connect((HOST, PORT))                               # Connect to the server

message = "PX {} {} {:02X}{:02X}{:02X}\n".format(x,y,r,g,b) # This is the message to be sent. 
# {} are placeholders for the variables. {:02x} converts a number into a hexadecimal value with two characters

print(message) # A print statement to show the message to be sent

sock.send(message) # This command sends the message to the server

sock.close() # Closes the connection to the server