#!usr/bin/env python

from sys import stderr
from socket import socket, AF_INET, SOCK_STREAM
from pickle import load, dump
from tkinter import Tk, Button, Label, Entry, Scrollbar, Listbox, Frame, StringVar
from tkinter import N, S, E, W, HORIZONTAL, END, ACTIVE, messagebox

class Gui(object):

    # initialize the gui
    def __init__(self):

        # create gui
        self._root = Tk()
        self._root.title('Nuclear source verification interface')
        screenWidth = self._root.winfo_screenwidth()
        screenHeight = self._root.winfo_screenheight()
        self._root.geometry('%sx%s'% (screenWidth//2, screenHeight//2))
        # layout grid
        self._root.grid_rowconfigure(0, weight=0)
        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_columnconfigure(0, weight=1)
        self._root.grid_columnconfigure(1, weight=1)
        self._root.grid_columnconfigure(2, weight=1)


        # buttons
        buttonsFrame = Frame(self._root, height=0)

        buttonsFrame.grid(row=0, column=0, columnspan=3,sticky=E+W,pady=10)
        buttonsFrame.grid_rowconfigure(0, weight=0)
        buttonsFrame.grid_columnconfigure(0, weight=1)
        buttonsFrame.grid_columnconfigure(1, weight=1)
        buttonsFrame.grid_columnconfigure(2, weight=1)


        shieldbutton = Button(buttonsFrame, text='Shielding Check')
        shieldbutton.bind('<Button-1>', self.shieldListener)
        calibratebutton = Button(buttonsFrame, text='Calibrate')
        calibratebutton.bind('<Button-1>', self.calibrateListener)
        verifybutton = Button(buttonsFrame, text='Verify')
        verifybutton.bind('<Button-1>', self.verifyListener)


        # grid elements in buttonsFrame
        shieldbutton.grid(row=0, column=0)
        calibratebutton.grid(row=0, column=1)
        verifybutton.grid(row=0, column=2)


        # scrolling listbox for text display
        listboxFrame = Frame(self._root, height=0)
        listboxFrame.grid_columnconfigure(0, weight=1)
        listboxFrame.grid_columnconfigure(1, weight=0)
        listboxFrame.grid_rowconfigure(0, weight=1)
        listboxFrame.grid_rowconfigure(1, weight=0)
        self._scrollingListbox = Listbox(listboxFrame, height=5)
        scrollbarV = Scrollbar(listboxFrame, command=self._scrollingListbox.yview)
        scrollbarH = Scrollbar(listboxFrame, command=self._scrollingListbox.xview,
            orient=HORIZONTAL)
        self._scrollingListbox['yscrollcommand'] = scrollbarV.set
        self._scrollingListbox['xscrollcommand'] = scrollbarH.set
        self._scrollingListbox.grid(row=0, column=0, sticky=N+S+E+W)
        scrollbarH.grid(row=1, column=0, sticky=E+W)
        scrollbarV.grid(row=0, column=1, sticky=N+S)
        listboxFrame.grid(row=1, column=0, sticky=N+S+E+W, columnspan=3, padx=10)
        self._scrollingListbox.insert(END, ' Welcome to the nuclear source verification interface. To begin, press shielding check.')

    def shieldListener(self, event):
        shielding_check()

    def calibrateListener(self, event):
        calibrate()

    def verifyListener(self, event):
        verify()

    # start the gui
    def start(self):
        self._root.mainloop()

if __name__ == '__main__':
    Gui().start()
