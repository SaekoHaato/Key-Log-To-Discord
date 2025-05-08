import customtkinter as CTk
from Modules.account import Account_App
from Modules.webhook import Webhook_App
from Modules.settings import Settings_App
from Modules.change import hotkey_buttons
from backports import configparser

class Main_Frame(CTk.CTk):
        global make_app

        def make_app(self,other_app,new_app):
            other_app.destroy()
            if new_app == 'Account':
                account_app = Account_App(self.app_frame)
            elif new_app == 'Webhook':
                webhook_app = Webhook_App(self.app_frame)
             
        def __init__(self):
            super().__init__()
            self.geometry('750x300')
            self.resizable(False,False)
            self.title('Key Log to Discord')

            self.app_frame = CTk.CTkFrame(self,fg_color='transparent')
            self.app_frame.pack()
            account_app = Account_App(self.app_frame)
            webhook_app = None

            path_frame = CTk.CTkFrame(self,width= 325,height=20,bg_color='transparent',fg_color='transparent')
            path_frame.place(x=410,y=15)

            account_button = CTk.CTkButton(path_frame,height=20,width=325/3,text="Account",command=lambda:make_app(self,self.app_frame.winfo_children()[0],'Account'))
            account_button.pack(side="left")

            webhook_button = CTk.CTkButton(path_frame,height=20,width=325/3,text="Webhook",command=lambda:make_app(self,self.app_frame.winfo_children()[0],'Webhook'))
            webhook_button.pack(side="left")

            setting_button = CTk.CTkButton(path_frame,height=20,width=325/3,text="Settings",command=lambda:Settings_App())
            setting_button.pack(side="left")

            self.mainloop()

if __name__ == '__main__':
    main_frame = Main_Frame()