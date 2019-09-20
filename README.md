# Pixelflut Client Workshop

## 1. Introduction
This readme is the text part of the workshop building a pixelflut client in python. The assumption is that you have python installed (https://www.python.org/), but no real programming experience. In terms of network connection the client works over wifi, but a gigabit ethernet is recommended. If you are doing this workshop on an event and have questions, feel free to ask them at the hackzone area or on the hackzone discord channel.

## 2. Initial client

`pixelflut.py` contains an initial client which puts a pixel on the screen. It can be run with `python pixelflut.py`, though this will result in an error like this:

``` bash
Traceback (most recent call last):
  File "pixelflut.py", line 13, in <module>
    sock.connect((HOST, PORT)) # Connect to the server
  File "/usr/lib/python2.7/socket.py", line 228, in meth
    return getattr(self._sock,name)(*args)
socket.error: [Errno 111] Connection refused
```

To figure out why this happens let's go through the code line by line.

``` python
import socket
```

Import imports a library of code into your program. In this case functions to set up network connections to other servers, like the pixelflut server. These type of connections are called sockets. The documentation for the library can be found here: https://docs.python.org/3/library/socket.html

``` python
HOST='127.0.0.1'
```

Here a piece of text is put into a variable. The text is the IP address of the server you want to connect to. In the example this is the loopback IP of your own computer. This also explains why the client doesn't connect, there is no server running on your pc. 
The text can be changed to another IP address, or an address like 'pixelflut.event.thereality.nl'.

``` python
PORT=1234
```

In addition to an address or IP address, the connection also needs a port. This line puts the port number for pixelflut into a variable.

``` python
x = 1                       # The X coordinate of the pixel
y = 1                       # The Y coordinate
r = 255                     # The Red color value
g = 255                     # The Green color value
b = 255                     # the Blue color value
```

The pixel to be put on the screen needs a x and y coordinate and color information and these lines create the required variables. X and Y coordinates are positive numbers within the size of the screen (common are 640x480 and 1920x1080). Colors should be within 0 to 255.

``` python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

A TCP stream socket is defined here and the resulting object is put into a variable. An object is a combination of variables which can store data and functions to manipulate data.

``` python
sock.connect((HOST, PORT))
```

The `.connect()` part of this line is one of these functions. It connects to the server using the HOST and PORT variables defined earlier.

``` python
message = "PX {} {} {:02X}{:02X}{:02X}\n".format(x,y,r,g,b)
```

The pixel command is assembled here and put into another variable. The command has the form `PX X Y RRGGBB\n` with the color code in hexadecimal numbers. To put the variables into the text, format() is used. {} is a placeholder for a variable. This placeholder can be customized, {:02X} converts a number into a two digit hexadecimal number with leading zeroes. This means that 10 is converted into "0A" and not "10" or "A". The `.format()` function replaces all the placeholders with actual numbers. More information about format can be found here: https://pyformat.info/

``` python
print(message)
```

The `print()` function puts text onto the command line.

``` python
sock.send(message)`
```

`.send()` is the function that sends the message to the server.

``` python
sock.close()
```

This command closes the connection to the server.

Things to try:
* Set the correct HOST, does the script connect?
* What happens if you change the X and Y coordinates? The Colors?

## 3. Changing the script

If the server is busy the script will run without errors, but you won't see any pixels appear. To fix that, it is time to learn about recursion.

Using `while` or `for` it is possible to repeat a set of commands. First lets use for.

To fill the entire screen, a message has to be sent for each pixel coordinate.

``` python
for x in range(640):
    for y in range(480):
        message = "PX {} {} {:02X}{:02X}{:02X}\n".format(x,y,r,g,b) 
        sock.send(message)
```

Add both for loops in front of message and sock.send. `for x in range(640):` means that `for` every `x in` the `range` [0, ..., 639] do the following command. Range creates a list of numbers from zero to the number you specify minus 1. The range command has more settings, `range(100,200,2)` will generate a list from 100, 102, 104 to 198 skipping each odd number. 

All the code you want to run in the for loop has to be indented using a `TAB`. Loops can also be nested, as you see above. The `sock.close()` command should not be idented, as this should only run once at the end of the program.

Information about `range()` can be found here: https://docs.python.org/3/library/stdtypes.html#typesseq-range

Running the modified script will now result in a white screen, which will dissapear quickly when other people are sending data to the screen.

To fix that a while loop can be used. The goal is to have the script run for 60 seconds.

First import the time library, adding this under the line importing the socket library:

``` python
import time
```

more about time: https://docs.python.org/3.7/library/time.html

Next store the starting time

``` python
endtime = time.time() + 60
```

This will store the current time in seconds plus 60s.

Now the while loop:

``` python
while time.time() < endtime:
```

Add this in front of the for loops and ident the rest of the code. The while loop executes until the condition after while is False. In this case the loop executes while the current time is smaller than the end time. 

Things to try:
* what happens if you modify the range?
* What can you do with color?

## 4 Images

Sending colors to the screen can be fun, but more fun is subjecting others to your favorite cat pictures.

Step one is installing the image library. In the command line enter:
``` bash
pip install pillow
```
The documentation for pillow can be found here: https://pillow.readthedocs.io/en/stable/

Add another import:
``` python
from PIL import Image
```
This imports a specific set of functions from a library.

To open an image use:
``` python
img = Image.open("cat.jpg")
```

To know how many pixels to send, the size of the image can be requested using:
``` python
w,h = img.size
```

`img.size` returns multiple variables. These are split in the w and h variable.

the width and height can be used in the for loops.

``` python
for x in range(w):
    for y in range(h):
```

Retrieving the color:

``` python
r,g,b = img.getpixel((x,y))
```

Adding this before the generation of the message will retrieve the color of the specific pixel.

And now you can send pictures

Further ideas:

* Can you add an offset to the image?
* Your image might be too big. Is there something in the documentation of the pillow library to scale it?
* For each pixel a seperate message is sent. Is there a clever way to add those messages together and sent them in one go?
* How could you send more images after each other?