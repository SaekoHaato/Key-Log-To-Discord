import customtkinter as CTk
import tkinter as tk
from pynput import keyboard
from configparser import ConfigParser

if __name__ == '__main__':
    from accessdata import access_data
    from buttonlist import data_buttons
    from quickbuttons import Quick_Send_Buttons
else:
    from Modules import send
    from Modules.accessdata import access_data
    from Modules.buttonlist import data_buttons
    from Modules.quickbuttons import Quick_Send_Buttons

class Webhook_App(CTk.CTkFrame):
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
                data_buttons(parent,log,(300,10),set)

    def save(self,scroll_one):
        webhook_file = open('Saves/WebhookData.txt','a')
        webhook_file.write(f'{self.webhook_stringvar.get()}\n')
        webhook_file.close()

        for widget in scroll_one.winfo_children():
            widget.destroy()
        display_data(self,scroll_one,'Saves/WebhookData.txt',self.webhook_stringvar)

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

        def send_func():
            self.sending = False
            send.send_to_discord(2,(self.username_stringvar.get(),self.webhook_stringvar.get(),self.message))
            self.message = ""       

        def key_pressed(key):
            try:
                if self.logging:
                    hotkeys=Quick_Send_Buttons.get_hotkeys()
                    try:
                        if key == keyboard.Key[self.stop_key] and self.sending:
                            send_func()
                        elif key == keyboard.Key[self.start_key]:
                            self.sending = True
                        elif key.char in list(hotkeys.keys()) and  not self.sending:
                            send.send_to_discord(2,(self.username_stringvar.get(),self.webhook_stringvar.get(),hotkeys[str(key)]))
                        else:
                            if self.sending:
                                self.message += key.char
                    except Exception as e:
                        print(e,1)
                        if key.char == str(self.stop_key) and self.sending:
                            send_func()  
                        elif key.char == str(self.start_key):
                            self.sending = True
                        elif key.char in list(hotkeys.keys()) and not self.sending:
                            send.send_to_discord(2,(self.username_stringvar.get(),self.webhook_stringvar.get(),hotkeys[str(key.char)]))
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
        
        self.webhook_stringvar = CTk.StringVar(input_frame)

        webhook_label = CTk.CTkLabel(
            input_frame,
            width=15,
            height=10,
            text='Webhook',
            text_color='white',
            font=('CTkFont',14)
        )
        webhook_label.place(x=130,y=15)

        webhook_entry = CTk.CTkEntry(
            input_frame,
            width=270,
            height=10,
            textvariable=self.webhook_stringvar
        )
        webhook_entry.place(x=22,y=35)

        webhook_lock = CTk.CTkCheckBox(
            input_frame,
            text="",
            command=lambda:lock_entry(webhook_entry)
        )
        webhook_lock.place(x=295,y=34)

        self.username_stringvar = CTk.StringVar(input_frame)

        username_label = CTk.CTkLabel(
            input_frame,
            width=15,
            height=10,
            text='Username',
            text_color='white',
            font=('CTkFont',14)
        )
        username_label.place(x=130,y=65)

        username_entry = CTk.CTkEntry(
            input_frame,
            width=270,
            height=10,
            textvariable=self.username_stringvar
        )
        username_entry.place(x=22,y=85)

        username_lock = CTk.CTkCheckBox(
            input_frame,
            text="",
            command=lambda:lock_entry(username_entry)
        )
        username_lock.place(x=295,y=84)
        
        activate_button = CTk.CTkButton(
            input_frame,
            command=lambda:activate_logging(activate_button),
            text="Activate"
        )
        activate_button.place(x=97,y=200)

        webhook_display = CTk.CTkFrame(self,width=375,height=270)
        webhook_display.place(x=15,y=15)

        webhook_display_label = CTk.CTkLabel(webhook_display,text='Webhooks', text_color='Black')
        webhook_display_label.place(x=160,y=0)

        webhook_scroll = CTk.CTkScrollableFrame(webhook_display,width=330,height=220,fg_color='#b1b1b1')
        webhook_scroll.place(x=12,y=30)

        display_data(self,webhook_scroll,'Saves/WebhookData.txt',self.webhook_stringvar)

        save_button = CTk.CTkButton(
            master=input_frame,
            text="Save",
            command=lambda: save(self,webhook_scroll)
        )
        save_button.place(x=97,y=120)

        self.pack()

if __name__ == '__main__':
    window = CTk.CTk()
    username_app = Webhook_App(window)

    window.mainloop()