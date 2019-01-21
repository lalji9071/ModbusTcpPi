from pyModbusTCP.client import ModbusClient
from tkinter import *
import pyautogui
import random
import time
import os

width1, height1 = pyautogui.size()
height2 = height1/3
width2 = (width1/2) - 50
height3 = height2/2
root = Tk()


red = Canvas(width=width1, height=height2, bg="black")
red.pack()
yellow = Canvas(width=width1, height=height2, bg="black")
yellow.pack()
green = Canvas(width=width1, height=height2, bg="black")
green.pack()


class Ball:
    def __init__(self):
        self.shape = red.create_oval(10, 10, 60, 60, fill="green")
        self.xspeed = random.randrange(-2, 10)
        self.yspeed = random.randrange(-2, 10)

    def move(self):
        red.move(self.shape, self.xspeed, self.yspeed)
        pos = red.coords(self.shape)
        if pos[3] >= height2 or pos[1] <= 0:
            self.yspeed = -self.yspeed
        if pos[2] >= width1 or pos[0] <= 0:
            self.xspeed = -self.xspeed

c = ModbusClient()
c.host("192.168.58.10")
c.port(502)
# managing TCP sessions with call to c.open()/c.close()
c.open()

ball = Ball()

color1 = StringVar()


#green_box = canvas.create_rectangle(25, 25, 130, 60, fill=color1)
fehler = Label(root, fg="black", background="red", textvariable=color1, font=("Helvetica", 40,"bold"))
fehler.place(x=width2, y=height3)
root.attributes("-fullscreen", True)
root.bind("<1>", exit)


def state_change():
    root.after(20, state_change)
    regs = c.read_discrete_inputs(512, 16)
    if regs[13] == 1:
        x = regs[13]
        print(x)
        red.configure(bg="red")
        color1.set("Störung")
        ball.move()
    if regs[13] == 0:
        x = regs[13]
        print(x)
        color1.set('black')

root.after(20, state_change)

root.mainloop()
