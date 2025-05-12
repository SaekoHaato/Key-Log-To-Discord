import customtkinter as CTk
import tkinter as tk
from pynput import keyboard
from configparser import ConfigParser
from pynput import keyboard

if __name__ == '__main__':
    from change import hotkey_buttons
    from quickbuttons import Quick_Send_Buttons
else:
    from Modules.change import hotkey_buttons
    from Modules.quickbuttons import Quick_Send_Buttons

class Settings_App(CTk.CTk):
    global set_settings
    
    def set_settings(self):
        settings_file = ConfigParser()
        settings_file.read('Saves/settings.ini')

        sections = settings_file.sections()

        for section in sections:
            hsection_holder = CTk.CTkFrame(self.key_frame,fg_color='transparent',height=100,width=140)
            hsection_holder.pack(side='top',padx=30)

            hsection_label = CTk.CTkLabel(hsection_holder,fg_color='grey',text=str(section).upper(),font=('CTkFont',11),text_color='white')
            hsection_label.pack(side='top',pady=3)

            ksection_holder = CTk.CTkFrame(self.hotkey_frame,fg_color='transparent',height=100,width=140)
            ksection_holder.pack(side='top',padx=30)

            ksection_label = CTk.CTkLabel(ksection_holder,fg_color='grey',text=str(section).upper(),font=('CTkFont',11),text_color='white')
            ksection_label.pack(side='top',pady=3)

            for element in list(settings_file[section]):
                if str(section) == 'quick send':
                    send_stringvar = CTk.StringVar(ksection_holder,value=element)
                    entry = Quick_Send_Buttons(ksection_holder,send_stringvar)
                    entry.pack()

                    hotkey_stringvar = CTk.StringVar(hsection_holder,value=settings_file[section][send_stringvar.get()])
                    button = hotkey_buttons(hsection_holder,section,send_stringvar,hotkey_stringvar)        
                    button.pack()

                else:
                    hotkey_stringvar = CTk.StringVar(hsection_holder,value=settings_file[section][element])
                    button = hotkey_buttons(hsection_holder,section,element,hotkey_stringvar)
                    button.pack()

                    element_label = CTk.CTkLabel(ksection_holder,fg_color='transparent',text_color='red',text=element)
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

        set_settings(self)

        self.mainloop()

if __name__ == "__main__":
    settings_app = Settings_App()