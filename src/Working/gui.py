#!usr/bin/env python

import sys
from threading import Thread
from tkinter import Tk, Button, Label, Entry, Scrollbar, Listbox, Frame, StringVar
from tkinter import N, S, E, W, HORIZONTAL, END, ACTIVE, DISABLED, NORMAL
from simple_osprey_2020 import *
from weapon_signatures_ultra import *
from shielding_check import *

MIN_NA = 481
MAX_NA = 576

class Gui(object):

    # initialize the gui
    def __init__(self):

        self._hvon = False
        self._gatheringdata = False
        self._counter = 0
        self._backgrounds = []
        self._shielddata = []
        self._verifydata = []
        self.

        # create gui
        self._root = Tk()
        self._root.title('Nuclear Source Verification Interface')
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


        self._shieldbutton = Button(buttonsFrame, text='Shielding Check', state=DISABLED)
        self._shieldbutton.bind('<Button-1>', self.shieldListener)
        self._calibratebutton = Button(buttonsFrame, text='Calibrate', state=DISABLED)
        self._calibratebutton.bind('<Button-1>', self.calibrateListener)
        self._verifybutton = Button(buttonsFrame, text='Verify', state=DISABLED)
        self._verifybutton.bind('<Button-1>', self.verifyListener)


        # grid elements in buttonsFrame
        self._shieldbutton.grid(row=0, column=1)
        self._calibratebutton.grid(row=0, column=0)
        self._verifybutton.grid(row=0, column=2)


        # scrolling listbox for text display
        listboxFrame = Frame(self._root, height=0)
        listboxFrame.grid_columnconfigure(0, weight=1)
        listboxFrame.grid_columnconfigure(1, weight=0)
        listboxFrame.grid_columnconfigure(2, weight=0)
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
        self._scrollingListbox.insert(END, ' Welcome to the nuclear source verification interface. To begin, press connect.')

        self._sideFrame = Frame(listboxFrame,height=0)
        self._sideFrame.grid_rowconfigure(0, weight=1)
        self._sideFrame.grid_rowconfigure(1, weight=1)
        self._sideFrame.grid_rowconfigure(2, weight=1)
        self._sideFrame.grid_rowconfigure(3, weight=1)
        self._sideFrame.grid(row=0, column=2, sticky=E+W, padx=(22,15))
        self._ipText = StringVar()
        self._ipText.set('128.112.35.172')
        ipEntry = Entry(self._sideFrame, textvariable=self._ipText)
        ipEntry.grid(row=0, sticky=E+W, padx=(22,15))
        self._connectbutton = Button(self._sideFrame, text='Connect')
        self._connectbutton.bind('<Button-1>', self.connectListener)
        self._connectbutton.grid(row=1, sticky=E+W, padx=(22,15))
        self._databutton = Button(self._sideFrame, text='Gather Data', state=DISABLED)
        self._databutton.bind('<Button-1>', self.dataListener)
        self._databutton.grid(row=2, sticky=E+W, padx=(22,15), pady=10)

    def connectListener(self, event):
        self._scrollingListbox.insert(END, 'Connecting to detector...')
        connect2osprey(self._ipText.get())
        self._scrollingListbox.insert(END, 'Connected')
        self._scrollingListbox.insert(END, 'Ramping up HV to 910 V...')
        HVon(910)
        self._hvon = True
        self._scrollingListbox.insert(END, 'HV on at 910 V')
        self._connectbutton.destroy()
        self._disconnectbutton = Button(self._sideFrame, text='Disconnect')
        self._disconnectbutton.bind('<Button-1>', self.disconnectListener)
        self._disconnectbutton.grid(row=1, sticky=E+W, padx=(22,15))
        self._calibratebutton['state'] = NORMAL
        self._scrollingListbox.insert(END, 'Click Calibrate to begin calibration process.')

    def disconnectListener(self, event):
        self._scrollingListbox.insert(END, 'Turning off HV...')
        HVoff()
        self._scrollingListbox.insert(END, 'HV off')
        self._hvon = False

    def calibrateListener(self, event):
        self._scrollingListbox.insert(END, 'Please point the sensor towards the background.')
        self._scrollingListbox.insert(END, 'When ready, click the gather data button.')
        self._databutton['state'] = NORMAL
        calib = []
        for i in range(2):
            self._scrollingListbox.insert(END, 'When ready, click the gather data button.')
            self._databutton['state'] = NORMAL
            while(not self._gatheringdata):
                pass
            self._databutton['state'] = DISABLED
            self._scrollingListbox.insert(END, 'Running calibration collection '+str(i+1))
            calib[i] = collect_data() - self._avg_bkgd
            self._scrollingListbox.insert(END,  'Calibration collection '+str(i+1)+' complete.')


        (self._a,b) = sodium_calibration(self._avg_bkgd, calib[0], calib[1])
        self._naCalibration = calib[0]-self._avg_bkgd

        self._scrollingListbox.insert(END,  'Calibration completed. When ready, click Shielding Check to continue.')
        self._calibratebutton['state'] = DISABLED
        self._shieldbutton['state'] = NORMAL


    def shieldListener(self, event):
        dists = [50,75,100]
        shielddata = []
        for i in range(len(dists)):
            self._scrollingListbox.insert(END, 'Please point the sensor to the material and place it '+str(dists[i])+' cm away from the material. When ready, click gather data.')
            self._databutton['state'] = NORMAL
            while(not self._gatheringdata):
                pass
            self._databutton['state'] = DISABLED
            self._scrollingListbox.insert(END, 'Running data collection at '+str(dists[i])+' cm.')
            shielddata[i] = collect_data() - self._avg_bkgd
            self._scrollingListbox.insert(END,  'Data collection at '+str(dists[i])+'cm complete.')
        excessive_shielding = check_shielding_run(dists, self._na_Calibration, MIN_NA, MAX_NA, shielddata[0], shielddata[1], shielddata[2], self._a)
        if excessive_shielding:
            self._scrollingListbox.insert(END,  'Shielding within acceptable range. When ready, click Verify button for nuclear material verification.')
            self._shieldbutton['state'] = DISABLED
            self._verifybutton['state'] = NORMAL
        else:
            self._scrollingListbox.insert(END,  'Too much shielding detected. Please start over, or quit.')
            self._calibratebutton['state'] = NORMAL
            self._shieldbutton['state'] = DISABLED



    def verifyListener(self, event):
        verifydata = []
        for i in range(3):
            self._scrollingListbox.insert(END, 'Please point the sensor at the material for reading '+str(i)+'. When ready, click gather data.')
            self._databutton['state'] = NORMAL
            while(not self._gatheringdata):
                pass
            self._databutton['state'] = DISABLED
            self._scrollingListbox.insert(END, 'Running data collection '+str(i)+'.')
            verifydata[i] = collect_data() - self._avg_bkgd
            self._scrollingListbox.insert(END,  'Data collection '+str(i)+' complete.')

        self._scrollingListbox.insert(END,  'Data collection complete. Verifying data...')

        (bmatch1, cmatch1) = verify(verifydata[0], self._a)
        (bmatch2, cmatch2) = verify(verifydata[1], self._a)
        (bmatch3, cmatch3) = verify(verifydata[2], self._a)
        barium = False
        cobalt = False
        if (bmatch1 and bmatch2) or (bmatch1 and bmatch3) or (bmatch2 and bmatch3):
            barium = True

        if (cmatch1 and cmatch2) or (cmatch1 and cmatch3) or (cmatch2 and cmatch3):
            cobalt = True

        print(barium, cobalt)
        if barium and cobalt:
            self._scrollingListbox.insert(END,  'Absense of weapon unconfirmed. ')
        else:
            self._scrollingListbox.insert(END,  'Absense of weapon confirmed.')


    def dataListener(self, event):
        thread = WorkerThread(self._sideFrame)
        thread.start()
        self._databutton['state'] = DISABLED
        if self._counter == 0:
            self._scrollingListbox.insert(END, 'Running background collection 1')
            self.backgrounds[0] = collect_data()
            self._scrollingListbox.insert(END,  'Background collection 1 complete. Please change location of background detector.')
        elif self._counter == 1:
            self._scrollingListbox.insert(END, 'Running background collection 2')
            self._backgrounds[1] = collect_data()
            self._scrollingListbox.insert(END,  'Background collection 2 complete. Please change location of background detector.')
        elif self._counter == 2:
            self._scrollingListbox.insert(END, 'Running background collection 3')
            self._backgrounds[2] = collect_data()
            self._scrollingListbox.insert(END,  'Background collection 3 complete.')
            self._avg_bkgd = avg_background(self._backgrounds[0],self._backgrounds[1],self._backgrounds[2])
            self._scrollingListbox.insert(END, 'Now, please point the sensor towards the calibration source for two calibration data collections.')
            self._scrollingListbox.insert(END, 'When ready, click the gather data button.')
        elif self._counter == 3:
            self._scrollingListbox.insert(END, 'Running background collection 3')
            self._backgrounds[2] = collect_data()
            self._scrollingListbox.insert(END,  'Background collection 3 complete.')
            self._avg_bkgd = avg_background(self._backgrounds[0],self._backgrounds[1],self._backgrounds[2])
            self._scrollingListbox.insert(END, 'Now, please point the sensor towards the calibration source for two calibration data collections.')

        self._databutton['state'] = ENABLED
        self._counter = self._counter+1




    def on_quit(self):
        if self._hvon:
            self.disconnectListener(None)

        self._root.destroy()

    # start the gui
    def start(self):
        self._root.protocol("WM_DELETE_WINDOW", self.on_quit)
        self._root.mainloop()

class WorkerThread(Thread):

    def __init__(self, frame):
        Thread.__init__(self)
        self._sideFrame = frame

    def run(self):
        self._gatheringdata = True
        timerStr = StringVar()
        self._timer = Label(self._sideFrame, textvariable=timerStr)
        self._timer.grid(row=3, sticky=E+W, padx=(22,15), pady=10)
        t = 300
        while t > 0:
            sleep(1)
            t = t-1
            timerStr.set(t)
        self._gatheringdata = False




def main():
    Gui().start()

if __name__ == '__main__':
    main()
