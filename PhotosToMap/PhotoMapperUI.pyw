#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      calebma
#
# Created:     01/06/2016
# Copyright:   (c) calebma 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
try:
    from Tkinter import *
except:
    from tkinter import *

from tkFileDialog import askdirectory, Open
import tkMessageBox
import photomapper
import thread
import time

class ProgressBar(object):
    def __init__(self, title='Progress Bar'):
        self.root = Tk()
        self.title = title
        self.isRunning = False

    def start(self):
        """ create the progress bar widget """
        self.root.title(self.title)
        self.root.geometry("+700+200")
        canvas = Canvas(self.root, width=261, height=60, bg='lightgray')
        canvas.pack()
        rc2 = canvas.create_rectangle(15, 20, 243, 50, outline='blue', fill='lightblue')
        rc1 = canvas.create_rectangle(24, 20, 34, 50, outline='white',  fill='green')
        total=100
        x = 5
        self.isRunning = True

        while self.isRunning:
            # infinite loop, will continue until self.isRunning is set to False, Danger zone!
            # I'm sure there are MUCH better ways to do this...

            # move the small rectangle +5 or -5 units
            total += x
            if total > 311:
                x = -5
            elif total < 100:
                x = 5
                # in a separate process so should not interfere with mainloop()
                time.sleep(0.2)
                if isinstance(canvas, Canvas):
                    canvas.move(rc1, x, 0)
                    if canvas.coords(rc1)[0] >= 239:
                        canvas.delete(rc1)
                        rc1 = canvas.create_rectangle(24, 20, 34, 50, outline='white',  fill='green')
                    canvas.update()
    
        self.root.destroy()

    def stop(self):
        """stops the progress bar"""
        self.isRunning = False

class GUI(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.folder = StringVar()
        self.new_folder = StringVar()
        self.name = StringVar()
        self.app_option = StringVar()
        self.executeButton = None
        self.options = ('Create a portable app', 'Embed in original photo directory')
        self.app_option.set(self.options[0])
        self.name.set('my_photos')
        self.portable = True
        self.initUI()

    def initUI(self):
        self.parent.title('Create Map from Geotagged Photos')
        self.columnconfigure(0, uniform=True)

        # in folder open
        self.inFolderButton = Button(self, text='Choose folder containing photos', command=self.onPhotoFolderOpen)
        self.inFolderDisplay = Entry(self, textvariable=self.folder, width=75, state=DISABLED)
        self.inFolderButton.grid(row=0, column=0, sticky=E+W)
        self.inFolderDisplay.grid(row=0, column=1, sticky=W, padx=10)

        # out folder open
        self.outFolderButton = Button(self, text='Choose output folder', command=self.onNewFolderOpen)
        self.outFolderDisplay = Entry(self, textvariable=self.new_folder, width=75, state=DISABLED)
        self.outFolderButton.grid(row=1, column=0, sticky=E+W)
        self.outFolderDisplay.grid(row=1, column=1, sticky=W, padx=10)

        # name
        nameLabel = Label(self, text='Name of application')
        nameBox = Entry(self, textvariable=self.name)
        nameLabel.grid(row=2, column=0, sticky=E)
        nameBox.grid(row=2, column=1, sticky=W, padx=10)
        nameBox.focus()

        # execute button
        self.executeButton = Button(self, text='Create Photo Map', command=self.onExecute, state=DISABLED)
        self.executeButton.grid(row=4, column=3, sticky=W)

        # radio buttons for portable app
        for i, option in enumerate(self.options):
            b = Radiobutton(self, text=option, variable=self.app_option, value=option, command=self.onAppOption)
            b.grid(row= 5 + i, column=1, sticky=W)

        # bmi image
        bmi_img = PhotoImage(file="./images/BOLT-GreenCircle.gif")
        bmi_lbl = Label(self, image=bmi_img)
        bmi_lbl.image = bmi_img
        bmi_lbl.grid(row=0,column=3, columnspan=3, rowspan=3, sticky=W, padx=10, pady=15)

        # pack it all up
        self.pack(side=LEFT, fill=BOTH, expand=1, padx=10, pady=10)

    def onPhotoFolderOpen(self):
        fl = askdirectory(initialdir=os.path.join(os.path.expanduser('~'), 'Desktop'))
        self.folder.set(os.path.abspath(fl))
        self.inFolderDisplay.config(state=NORMAL)
        if self.app_option == self.options[0]:
            if all(map(os.path.exists, [self.folder.get(), self.new_folder.get()]) + [bool(self.name.get())]):
                self.executeButton.config(state=NORMAL)
        else:# self.app_option == self.options[1] and os.path.exists(self.folder.get()):
            self.executeButton.config(state=DISABLED)

    def onNewFolderOpen(self):
        fl = askdirectory(initialdir=os.path.join(os.path.expanduser('~'), 'Desktop'))
        self.new_folder.set(os.path.abspath(fl))
        self.outFolderDisplay.config(state=NORMAL)
        if all(map(lambda x: bool(x), [self.folder.get(), self.new_folder.get(), self.name.get()])):
            self.executeButton.config(state=NORMAL)

    def onAppOption(self):
        if self.app_option.get() == self.options[1]:
            self.portable = False
            self.outFolderButton.config(state=DISABLED)
            self.outFolderDisplay.config(state=DISABLED)
            if os.path.exists(self.folder.get()):
                self.executeButton.config(state=NORMAL)
            else:
                self.executeButton.config(state=DISABLED)
        elif self.app_option.get() == self.options[0]:
            self.portable = True
            self.outFolderButton.config(state=NORMAL)
            if all(map(os.path.exists, [self.folder.get(), self.new_folder.get()]) + [bool(self.name.get())]):
                self.executeButton.config(state=NORMAL)
                self.outFolderDisplay.config(state=NORMAL)
            else:
                self.executeButton.config(state=DISABLED)

    def onExecute(self):
        self.progressBar = ProgressBar('Creating Photo Viewer...')
        thread.start_new_thread(self.progressBar.start, ())
        photomapper.map_photos(self.folder.get(), self.new_folder.get(), self.name.get(), self.portable)
        self.progressBar.stop()

def main():
    root = Tk()
    root.geometry("800x225")
    root.iconbitmap("./images/Tripod_16x16.ico")
    gui = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
