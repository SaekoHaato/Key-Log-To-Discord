import customtkinter as CTk
import tkinter as tk
from pynput import keyboard
from configparser import ConfigParser
from pynput import keyboard

class Quick_Send_Buttons(CTk.CTkButton):
    global input_screen

    @staticmethod
    def get_hotkeys():
        settings_file = ConfigParser()
        settings_file.read('Saves/settings.ini')

        dic = {}

        for element in list(settings_file['quick send']):
                dic[settings_file['quick send'][element]] = element
        return dic

    def input_screen(stringvar):
        input_window = CTk.CTk()
        input_window.geometry('300x200')
        input_window.title('Key Log To Discord')

        text = CTk.CTkEntry(input_window,placeholder_text='Quick Send Text Here')
        text.pack(side='top',pady=50,fill='x',padx=15)

        save = CTk.CTkButton(input_window,text="Save")

        def write():

            settings_file = ConfigParser()
            settings_file.read('Saves/settings.ini')

            hotkey = settings_file['quick send'][stringvar.get()]
            settings_file.remove_option('quick send',stringvar.get())
            settings_file.set('quick send',text.get(),hotkey)

            with open('Saves/settings.ini','w') as configfile:
                settings_file.write(configfile)

            stringvar.set(text.get())

            input_window.after(150,lambda:input_window.destroy())

        save.configure(command=write)
        save.pack()

        input_window.mainloop()

    def __init__(self,parent,stringvar):
        super().__init__(
            parent,
            fg_color='transparent',
            text_color='red',
            width=90,
            textvariable=stringvar,
            command=lambda:input_screen(stringvar))