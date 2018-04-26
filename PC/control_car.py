import bluetooth
import time
import numpy as np


class Controller:
    def __init__(self, time_sleep):
        self.time = time_sleep
    def connectBluetooth(self,macAddress,port):
        try:
            self.socket = None
            print("Connecting...")
            s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            s.connect((macAddress, port))
            print("Connect Successful!")
            self.socket = s
        except:
            ##reconnect
            print("No conection!")
            print("Wait for 5 seconds to reconnect!")
            time.sleep(5)
            self.connectBluetooth(macAddress, port)

    def forward(self):
        print("forward")
        self.socket.send("1")
        time.sleep(self.time)
        self.socket.send("0")
        
    def backward(self):
        print("backward")
        self.socket.send("2")
        time.sleep(self.time)
        self.socket.send("0")
        
    def turnLeft(self):
        print("turn left")
        self.socket.send("3")
        time.sleep(self.time)
        self.socket.send("0")

    def turnRight(self):
        print("turn_right")
        self.socket.send("4")
        time.sleep(self.time)
        self.socket.send("0")

    def stop(self):
        self.socket.send("0")

    def runByLabel(self,label):
        if(np.array_equal(label, [1,0,0])):
            self.forward()
        elif(np.array_equal(label, [0,1,0])):
            self.turn_left()
        elif(np.array_equal(label, [0,0,1])):
            self.turn_right()
        else:
            print("Nothing")

    def showLabel(self,label):
        if(np.array_equal(label, [1,0,0])):
            print("forward")
        elif(np.array_equal(label, [0,1,0])):
            print("turn left")
        elif(np.array_equal(label, [0,0,1])):
            print("turn right")
        else:
            print("Nothing")


