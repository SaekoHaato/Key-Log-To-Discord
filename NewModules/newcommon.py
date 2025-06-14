import customtkinter as CTk
from configparser import ConfigParser

def create_input(self, name,label_cords,entry_cords, lock_cords):
    x,y = label_cords
    label = CTk.CTkLabel(
        self.master['input frame'],
        width=15,
        height=10,
        text=name,
        text_color="white",
        font=("CTkFont", 14),
    )
    label.place(x=x, y=y)

    self.vars[name] = CTk.StringVar(self.master['input frame'])

    ex, ey = entry_cords
    entry = CTk.CTkEntry(
        self.master['input frame'], width=270, height=10, textvariable=self.vars[name]
    )
    entry.place(x=ex, y=ey)

    lx, ly = lock_cords
    lock = CTk.CTkCheckBox(
        self.master['input frame'], text='', command=lambda: self.lock(entry)
    )
    lock.place(x=lx, y=ly)


def scroll_display(master, size, places, text):
    label = CTk.CTkLabel(
        master=master,
        text=text,
        text_color='black'
    )
    x,y=places['label']
    label.place(x=x,y=y)

    width, height = size
    scroll = CTk.CTkScrollableFrame(
        master=master,
        width=width,
        height=height,
        fg_color='#b1b1b1',
        corner_radius=5
    )
    x,y=places['scroll']
    scroll.place(x=x,y=y)

    return scroll


class ReplacerButton(CTk.CTkButton):

    def __init__(self, master, var, save):
        super().__init__(
            master=master,
            text=save[0],
            command=lambda: var.set(save[1])
        )
        self.pack(pady=2.5)


def set_replacerbuttons(master, section, var):
    file = ConfigParser()
    file.read('Saves/saves.ini')

    for key, value in file[section].items():
        ReplacerButton(master,var,(key, value))