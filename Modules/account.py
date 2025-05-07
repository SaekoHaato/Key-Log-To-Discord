import customtkinter as CTk
import tkinter as tk
from pynput import keyboard
from configparser import ConfigParser

if __name__ == '__main__':
    import send
    from accessdata import access_data
    from buttonlist import data_buttons
else:
    from Modules import send
    from Modules.accessdata import access_data
    from Modules.buttonlist import data_buttons

class Account_App(CTk.CTkFrame):
    global lock_entry
    global key_pressed
    global activate_logging
    global save
    global display_data

    def display_data(self,parent,data_file,set):
        data = access_data(data_file)
        
        logs = None

        if data:
            logs = data.split('\n')
        if logs != None:
            for log in logs:
                data_buttons(parent,log,(155,10),set)

    def save(self,scroll_one,scroll_two):
        channel_file = open('Saves/ChannelData.txt','a')
        channel_file.write(f'{self.channel_stringvar.get()}\n')
        channel_file.close()
        account_file=open('Saves/AccountData.txt','a')
        account_file.write(f'{self.account_stringvar.get()}\n')
        account_file.close()

        for widget in scroll_one.winfo_children():
            widget.destroy()
        for widget in scroll_two.winfo_children():
            widget.destroy()
        display_data(self,scroll_one,'Saves/ChannelData.txt',self.channel_stringvar)
        display_data(self,scroll_two,'Saves/AccountData.txt',self.account_stringvar)

    def lock_entry(entry):
        if entry.cget('state') == 'disabled':
            entry.configure(state = 'normal')
        else:
            entry.configure(state = 'disabled')

    def __init__(self,parent):
        super().__init__(parent,width = 750,height=300,fg_color='transparent')

        self.first = True
        self.listener = None
        self.logging = None
        self.message = ""
        self.sending = False

        global key_pressed
        global activate_logging

        self.settings_file = ConfigParser()
        self.settings_file.read('Saves/settings.ini')
        self.stop_key = str(self.settings_file['activation']['stop'])
        self.start_key = str(self.settings_file['activation']['start'])

        def key_pressed(key):
            try:
                if self.logging:
                    try:
                        if key ==  keyboard.Key[self.stop_key] and self.sending:
                                self.sending = False
                                send.send_to_discord(1,(self.account_stringvar.get(),self.channel_stringvar.get(),self.message))
                                self.message = ""
                                
                        elif key == keyboard.Key[self.start_key]:
                            self.sending = True
                        else:
                            if self.sending:
                                self.message += key.char
                    except Exception as e:
                        print(e,1)
                        if key.char ==  str(self.stop_key) and self.sending:
                                self.sending = False
                                send.send_to_discord(1,(self.account_stringvar.get(),self.channel_stringvar.get(),self.message))
                                self.message = ""
                                
                        elif key.char == str(self.start_key):
                            self.sending = True
                        else:
                            if self.sending:
                                self.message += key.char
            except Exception as e:
                print(e,2)
                if key == keyboard.Key.space and self.sending:
                    self.message += " "
                elif key == keyboard.Key.backspace and self.sending:
                    self.message = self.message[0:-1]
                    
        def activate_logging(button):
            self.settings_file.read('Saves/settings.ini')
            self.stop_key = str(self.settings_file['activation']['stop'])
            self.start_key = str(self.settings_file['activation']['start'])

            if button.cget('text') == 'Activate':
                button.configure(text = 'Activated')
                self.logging = True
                if self.first: 
                        self.first = False
                        listener = keyboard.Listener(on_press=key_pressed)
                        listener.start()
            else:
                button.configure(text ='Activate')
                self.logging = False

        input_frame = CTk.CTkFrame(
            self,
            width= 325,
            height=245,
            fg_color="grey",
            corner_radius=5,
            border_width=1
        )
        input_frame.place(x=410,y=35)
        
        self.channel_stringvar = CTk.StringVar(input_frame)

        channel_label = CTk.CTkLabel(
            input_frame,
            width=15,
            height=10,
            text='Channel',
            text_color='white',
            font=('CTkFont',14)
        )
        channel_label.place(x=130,y=15)

        channel_entry = CTk.CTkEntry(
            input_frame,
            width=270,
            height=10,
            textvariable=self.channel_stringvar
        )
        channel_entry.place(x=22,y=35)

        channel_lock = CTk.CTkCheckBox(
            input_frame,
            text="",
            command=lambda:lock_entry(channel_entry)
        )
        channel_lock.place(x=295,y=34)

        self.account_stringvar = CTk.StringVar(input_frame)

        account_label = CTk.CTkLabel(
            input_frame,
            width=15,
            height=10,
            text='Account',
            text_color='white',
            font=('CTkFont',14)
        )
        account_label.place(x=130,y=65)

        account_entry = CTk.CTkEntry(
            input_frame,
            width=270,
            height=10,
            textvariable=self.account_stringvar
        )
        account_entry.place(x=22,y=85)

        account_lock = CTk.CTkCheckBox(
            input_frame,
            text="",
            command=lambda:lock_entry(account_entry)
        )
        account_lock.place(x=295,y=84)
        
        activate_button = CTk.CTkButton(
            input_frame,
            command=lambda:activate_logging(activate_button),
            text="Activate"
        )
        activate_button.place(x=97,y=200)

        info_display = CTk.CTkFrame(self, width=375,height=270,corner_radius=5)
        info_display.place(x=15,y=15)

        channel_display = CTk.CTkFrame(info_display,width=177,height=260,fg_color='transparent',bg_color='transparent')
        channel_display.place(x=7,y=5)

        channel_display_label = CTk.CTkLabel(channel_display,text='Channel', text_color='Black')
        channel_display_label.place(x=60,y=0)

        channel_scroll = CTk.CTkScrollableFrame(channel_display,width=155,height=245,fg_color='#b1b1b1',corner_radius=5)
        channel_scroll.place(x=0,y=30)

        display_data(self,channel_scroll,'Saves/ChannelData.txt',self.channel_stringvar)

        account_display =CTk.CTkFrame(info_display,width=177,height=260,fg_color='transparent',bg_color='transparent')
        account_display.place(x=193,y=5)

        account_display_label = CTk.CTkLabel(account_display,text='Account', text_color='black')
        account_display_label.place(x=60,y=0)

        account_scroll = CTk.CTkScrollableFrame(account_display,width=155,height=245,fg_color='#b1b1b1',corner_radius=5)
        account_scroll.place(x=0,y=30)

        display_data(self,account_scroll,'Saves/AccountData.txt',self.account_stringvar)

        save_button = CTk.CTkButton(
            master=input_frame,
            text="Save",
            command=lambda: save(self,channel_scroll,account_scroll)
        )
        save_button.place(x=97,y=120)

        self.pack()

if __name__ == '__main__':
    window = CTk.CTk()
    account_app = Account_App(window)

    window.mainloop()