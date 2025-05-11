import customtkinter as CTk
import tkinter as tk
from pynput import keyboard
from configparser import ConfigParser
from pynput import keyboard

if __name__ == '__main__':
    from change import hotkey_buttons
else:
    from Modules.change import hotkey_buttons

class Settings_App(CTk.CTk):
    global set_settings
    
    def set_settings(self,parent,value):
        settings_file = ConfigParser()
        settings_file.read('Saves/settings.ini')

        sections = settings_file.sections()

        for section in sections:
            section_holder = CTk.CTkFrame(parent,fg_color='transparent',height=100,width=140)
            section_holder.pack(side='top',padx=60)

            section_label = CTk.CTkLabel(section_holder,fg_color='grey',text=str(section).upper(),font=('CTkFont',11),text_color='white')
            section_label.pack(side='top',pady=3)

            for element in list(settings_file[section]):
                if value:
                    hotkey_stringvar = CTk.StringVar(section_holder,value=settings_file[section][element])
                    button = hotkey_buttons(section_holder,section,element,hotkey_stringvar)
                    
                    button.pack(expand=True)
                else:
                    element_label = CTk.CTkLabel(section_holder,fg_color='transparent',text_color='red',text=element)
                    element_label.pack()

    def __init__(self):
        super().__init__()
        
        self.resizable(False,False)
        self.geometry("400x350")
        self.title('Key Log to Discord')

        self.hotkey_frame = CTk.CTkFrame(self,fg_color='grey',height=100,width=190)
        self.hotkey_frame.pack(side='left',fill='y',padx=5,pady=10)

        self.key_frame = CTk.CTkFrame(self,fg_color='grey',height=100,width=190)
        self.key_frame.pack(side='right',fill='y',padx=5,pady=10) 

        set_settings(self,self.hotkey_frame,False)
        set_settings(self,self.key_frame,True)

        self.mainloop()

if __name__ == "__main__":
    settings_app = Settings_App()