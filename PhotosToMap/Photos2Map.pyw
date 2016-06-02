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
from Tkinter import *
from ttk import Progressbar
from tkFileDialog import askdirectory, Open
import tkMessageBox
import photo2map

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
        self.inFolderDisplay.config(state='normal')
        if self.app_option == self.options[0]:
            if all(map(lambda x: bool(x), [self.folder.get(), self.new_folder.get(), self.name.get()])):
                self.executeButton.config(state='normal')
        else:
            self.executeButton.config(state='normal')

    def onNewFolderOpen(self):
        fl = askdirectory(initialdir=os.path.join(os.path.expanduser('~'), 'Desktop'))
        self.new_folder.set(os.path.abspath(fl))
        self.outFolderDisplay.config(state='normal')
        if all(map(lambda x: bool(x), [self.folder.get(), self.new_folder.get(), self.name.get()])):
            self.executeButton.config(state='normal')

    def onAppOption(self):
        if self.app_option.get() == self.options[1]:
            self.portable = False
            self.outFolderButton.config(state=DISABLED)
            self.outFolderDisplay.config(state=DISABLED)
        elif self.app_option.get() == self.options[0]:
            self.portable = True
            self.outFolderButton.config(state='normal')


    def onExecute(self):
        photo2map.photos_to_map(self.folder.get(), self.new_folder.get(), self.name.get(), self.portable)

def main():
    root = Tk()
    root.geometry("800x225")
    root.iconbitmap("./images/Tripod_16x16.ico")
    gui = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
