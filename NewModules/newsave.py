import customtkinter as CTk
from configparser import ConfigParser

class SaveApp(CTk.CTk):

    def save(self):
        save_file = ConfigParser()
        save_file.read('Saves/saves.ini')

        if self.account:  
            if self.channel_check.get():
                save_file['channels'][self.channel_entry.get()] = self.values[0]
            if self.account_entry.get():
                save_file['accounts'][self.account_entry.get()] = self.values[1]
        else:
            if self.webhook_check.get():
                save_file['webhooks'][self.webhook_entry.get()] = self.values[0]

        with open('Saves/saves.ini', 'w') as file:
            save_file.write(file)
        
        self.app.reset_saves()

        self.after(150,self.destroy)

    def create_entry_group(self, text):
        frame = CTk.CTkFrame(self, fg_color='transparent')
        frame.pack(fill='x', pady=20, side='top')

        check = CTk.CTkCheckBox(
            frame,
            text='',
            width=15
        )
        check.pack(side='left', padx=7.5)

        entry = CTk.CTkEntry(
            frame,
            placeholder_text=text
        )
        entry.pack(fill='x', side='left', expand=True, padx=7.5)

        return entry, check

    def __init__(self, account, values, app):
        super().__init__()

        self.geometry('300x200')
        self.resizable(False,False)
        self.title(f'Key Log To Discord: Save Account')

        self.account = account
        self.values = values
        self.app = app

        if self.account:
            self.channel_entry, self.channel_check = self.create_entry_group('Channel')
            self.account_entry, self.account_check = self.create_entry_group('Account')        
        else:
            self.webhook_entry, self.webhook_check = self.create_entry_group('Webhook')

        self.save_button = CTk.CTkButton(
            self,
            text='Save',
            command=self.save
        )
        self.save_button.pack()


        self.mainloop()

if __name__ == '__main__':
    SaveApp(True)