import customtkinter as CTk
from NewModules.newaccount import AccountApp
from NewModules.newwebhook import WebhookApp
from NewModules.newsettings import SettingsApp
from NewModules.newsave import SaveApp
from configparser import ConfigParser
from pynput import keyboard
import requests
from discord import SyncWebhook


class MainApp(CTk.CTk):

    def reset_saves(self):
        if self.account_app:
            self.account_app.set_saves()
        else:
            self.webhook_app.set_saves()
    
    def key_pressed(self,key):
        if not self.activated: return

        settings_file = ConfigParser()
        settings_file.read('Saves/settings.ini')
        hotkeys = dict(zip(settings_file['quick send'].values(), settings_file['quick send'].keys()))

        try:
            if self.logging:
                if key.char == self.stop_key:
                    self.send(self.message)
                else:
                    self.message += key.char
            elif key.char == self.start_key:
                self.logging = True
            elif key.char in hotkeys.keys():
                self.send(hotkeys[key.char])
        except Exception as e:
            print(e)
            if self.logging:
                if key == keyboard.Key[self.stop_key]:
                    self.send(self.message)
                elif key == keyboard.Key.space:
                    self.message += ' '
                elif key == keyboard.Key.backspace:
                    self.message = self.message[0:-1]
            elif key in hotkeys.keys():
                self.send(hotkeys[key])
            elif key == keyboard.Key[self.start_key]:
                self.logging = True
        
    def activate(self):
        self.settings_file.read('Saves/settings.ini')
        self.start_key = self.settings_file['activation']['start']
        self.stop_key = self.settings_file['activation']['stop']

        if self.activated:
            self.activate_button.configure(text='Activate')
        else:
            self.activate_button.configure(text="Activated")
        
        self.activated = not self.activated

    def send(self,message):

        self.logging = False

        try:
            if self.account_app:
                payload = {'content': message}
                header = {'authorization': self.account_app.vars['Account'].get()}
                r = requests.post(self.account_app.vars['Channel'].get(), json=payload, headers=header)             
            else:   
                webhook = SyncWebhook.from_url(self.webhook_app.vars['Webhook'].get())
                webhook.send(message, username=self.webhook_app.vars['Username'].get())
        except Exception as e:
            print(e)        
        
        self.message = ''

    def __init__(self):
        super().__init__()

        self.geometry('750x300')
        self.resizable(False,False)
        self.title('Key Log To Discord')

        self.activated = False
        self.logging = False
        self.message = ''
        self.listener = keyboard.Listener(on_press=self.key_pressed)
        self.listener.start()

        self.settings_file = ConfigParser()
        self.settings_file.read('Saves/settings.ini')

        main_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        main_frame.pack()

        self.make_paths()

        self.input_frame = CTk.CTkFrame(
            self,
            width=325,
            height=245,
            fg_color="grey",
            corner_radius=5,
            border_width=1,
        )
        self.input_frame.place(x=410, y=35)

        self.activate_button = CTk.CTkButton(
            self.input_frame,
            command=self.activate,
            text="Activate",
        )
        self.activate_button.place(x=97, y=200)

        save_button = CTk.CTkButton(
            master=self.input_frame,
            text='Save',
            command=lambda: SaveApp(
                True if self.account_app else False, 
                (self.account_app.vars['Channel'].get(), self.account_app.vars['Account'].get()) if self.account_app else (self.webhook_app.vars['Webhook'].get()),
                self
            )
        )
        save_button.place(x=97, y=120)

        self.info_display = CTk.CTkFrame(self, width=375, height=270, corner_radius=5)
        self.info_display.place(x=15, y=15)

        self.masters={'input frame':self.input_frame, 'info display':self.info_display}
        self.account_app = AccountApp(self.masters)
        self.webhook_app = None#WebhookApp(masters)

    def make_paths(self):

        def change_apps():
            for child in self.input_frame.winfo_children() + self.info_display.winfo_children():
                try:
                    if child.cget('text') == 'Save' or child.cget('text') == 'Activate' or child.cget('text') == 'Activated': continue
                    child.destroy()
                except Exception:
                    child.destroy()
            if self.account_app is not None:
                self.account_app = None
                self.webhook_app = WebhookApp(self.masters)
                self.changeapp_button.configure(text='Account')
            else:
                self.webhook_app = None
                self.account_app = AccountApp(self.masters)
                self.changeapp_button.configure(text='Webhook')
            self.activated = False
            self.logging = False
            self.message = ''
        path_frame = CTk.CTkFrame(
            self, 
            width=325, 
            height=20, 
            bg_color="transparent", 
            fg_color="transparent"
            )
        path_frame.place(x=410, y=15)

        self.changeapp_button = CTk.CTkButton(
            path_frame,
            height=20,
            width=325 / 2,
            text="Webhook",
            command=change_apps
        )
        self.changeapp_button.pack(side="left")

        setting_button = CTk.CTkButton(
            path_frame,
            height=20,
            width=325 / 2,
            text="Settings",
            command=SettingsApp
        )
        setting_button.pack(side="left")

if __name__ == '__main__':
    App = MainApp()

    App.mainloop()