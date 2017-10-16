from tkinter import *
import SpotifySearch

gui = Tk()
ent = StringVar()

def perform_search():
    SpotifySearch.SpotifySearch(ent.get())
    return

gui.geometry('300x200+500+300')
gui.title('SpotifySearcher')

label = Label(gui, text='Insert a mixesdb.com URL', font = (None, 15)).pack()
Entry = Entry(gui, textvariable=ent).pack()
button = Button(gui, text = 'Search', command = perform_search, fg = 'black', bg = 'white').pack()

gui.mainloop()


