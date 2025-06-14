import customtkinter as CTk
from NewModules.newcommon import create_input, scroll_display, set_replacerbuttons

class AccountApp():

    def lock(self,entry):
        if entry.cget("state") == "disabled":
            entry.configure(state="normal")
        else:
            entry.configure(state="disabled")

    def set_saves(self):
        for child in self.account_scroll.winfo_children() + self.channel_scroll.winfo_children():
            child.destroy()

        set_replacerbuttons(self.account_scroll, 'accounts', self.vars['Account'])
        set_replacerbuttons(self.channel_scroll, 'channels', self.vars['Channel'])

    def __init__(self, master):
        self.vars = {}
        self.master = master
        create_input(self, 'Channel', (130, 15), (22, 35), (295, 35))
        create_input(self, 'Account', (130,65), (22, 85), (295, 84))

        self.channel_scroll = scroll_display(
            self.master['info display'],
            (155,245), 
            places={'label':(67,5),'scroll':(7,35)},
            text='Channel'
        )

        self.account_scroll = scroll_display(
            self.master['info display'],
            (155,245), 
            places={'label':(253,5),'scroll':(193,35)},
            text='Account'
        )
        
        self.set_saves()