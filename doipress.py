'''
Created on 26 Jun 2017

@author: Richard Ostler
@license: MIT License
@copyright: Copyright 2017 Rothamsted Research
@organization: Rothamsted Research
@version: 1.0

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR 
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.
'''
import tkinter as tk
from tkinter import ttk
import pymysql
import configparser
from hashids import Hashids
from datetime import date
import time
import getpass

def generateDOI(*args):
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        chost = config['DATABASE']['host']
        cuser = config['DATABASE']['user']
        cpwd= config['DATABASE']['password']
        cdb = config['DATABASE']['db']
        doiPrefix = config['DOI']['prefix']
        db = pymysql.connect(host=chost,user=cuser,password=cpwd,db=cdb)
        cursor = db.cursor()

        cursor.execute("select sum(id) from ( select max(doi_sequence) as id from DOIManager union all select 1 as id ) nextid");
        data = cursor.fetchone()
        nextId = data[0]
        
        now = str(date.today()) + ":" + str(time.time())
        hashids = Hashids(min_length=16, salt=now.__str__())
        doi.set(doiPrefix+"/" + hashids.encode(int(nextId)))
        cursor.execute("insert into DOIManager (doi_sequence,doi,salt,created_by) values(" + str(nextId) + ",'"+doi.get()+"','"+now+"','"+getpass.getuser()+"')")
        db.commit()
        db.close()
    except ValueError:
        pass
    
def copyToClipboard(*args):
    root.clipboard_append(doi.get())
    
def centerWindow(width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

class MainApplication(tk.Frame):    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        centerWindow(300,300)
        root.title("DOI Press version 1.0")
        
        img = tk.Image("photo", file="rothamsted-favicon.ico")
        root.tk.call('wm','iconphoto',root._w,img)
        #root.iconbitmap("rothamsted-favicon.png")
        mainframe = ttk.Frame(root, padding="12 12 12 12")
        mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)      
        
        ttk.Button(mainframe, text="Mint DOI", command=generateDOI).grid(column=1, row=1, sticky=tk.W)
        ttk.Label(mainframe, text="New DOI is:").grid(column=1, row=2, sticky=tk.W)
        ttk.Label(mainframe, textvariable=doi).grid(column=1, row=3, sticky=(tk.W)) #note textvariable use
        ttk.Button(mainframe, text="Copy DOI to clipboard", command=copyToClipboard).grid(column=1, row=4, sticky=tk.W)
        
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5) # adds padding to content

if __name__ == "__main__":
    root = tk.Tk()
    doi = tk.StringVar()
    MainApplication(root)
    root.mainloop()