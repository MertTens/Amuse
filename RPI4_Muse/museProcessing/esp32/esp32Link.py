
from tkinter import *
import sys
import socket
import serial
import glob

# Initialize socket and serial connections
UDP_IP = "192.168.2.251"
UDP_PORT = 8888

SER_ESP32 = None
try:
    SER_ESP32 = serial.Serial("/dev/ttyACM0", 115200, timeout=10)
    print("Connected to USB:")
    print(SER_ESP32.name)
    SERIAL_CONNECTED = True;
except serial.serialutil.SerialException as ex:
    print (ex)
    print ('Serial USB not connected')
    SERIAL_CONNECTED = False;

# Sends command on UDP, via USB cable
def send_command(message):
    msg_as_bytes = str.encode(message)
    print ("UDP target IP:", UDP_IP, ":" ,UDP_PORT, " ",  msg_as_bytes)
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.sendto(msg_as_bytes, (UDP_IP, UDP_PORT))
    if(SERIAL_CONNECTED & (SER_ESP32 is not None)):
        print("USB port:", SER_ESP32.name)
        SER_ESP32.write(msg_as_bytes)

def send_serial(message):
    msg_as_bytes = str.encode(message)
    print("USB port:", SER_ESP32.name)
    SER_ESP32.write(msg_as_bytes)



# Wrappers for send_command
def send_command_forward():
    send_command("f")
def send_command_backward():
    send_command("b")
def send_command_left():
    send_command("l")
def send_command_right():
    send_command("r")
def send_command_stop():
    send_command("s")
def increase_speed():
    send_commond(">")
def decrease_speed():
    send_command("<")
def reset():
    send_command("s")
    send_command("0")




# ===================== Main Execution =====================
if __name__ =="__main__":
# Set up Tkinter window UI
    window = Tk()
    window.title("MindTEAL")
    window.geometry('350x200')

# Configure rows and columns to have equal size
    for i in range(3):
        Grid.rowconfigure(window, i, weight=1)
        Grid.columnconfigure(window, i, weight=1)

# Add buttons
    btnInc = Button(window, text="Speed+", command=lambda:send_command(">"))
    btnInc.grid(column=0, row=0, sticky=N+S+E+W)
    btnDec = Button(window, text="Speed-", command=lambda:send_command("<"))
    btnDec.grid(column=2, row=0, sticky=N+S+E+W)

    btnRst = Button(window, text="Reset", command=lambda:reset())
    btnRst.grid(column=0, row=2, sticky=N+S+E+W)

    btnHome = Button(window, text="Home", command=lambda:send_command("h"))
    btnHome.grid(column=2, row=2, sticky=N+S+E+W)

    btnFwd = Button(window, text="Forward", command=lambda:send_command("f"))
    btnFwd.grid(column=1, row=0, sticky=N+S+E+W)
    btnLeft = Button(window, text="Left", command=lambda:send_command("l"))
    btnLeft.grid(column=0, row=1, sticky=N+S+E+W)
    btnStop = Button(window, text="Stop", command=lambda:send_command("s"))
    btnStop.grid(column=1, row=1, sticky=N+S+E+W)
    btnRight = Button(window, text="Right", command=lambda:send_command("r"))
    btnRight.grid(column=2, row=1, sticky=N+S+E+W)
    btnRev = Button(window, text="Reverse", command=lambda:send_command("b"))
    btnRev.grid(column=1, row=2, sticky=N+S+E+W)

# Begin GUI loop
    window.mainloop()
