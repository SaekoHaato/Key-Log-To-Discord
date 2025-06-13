import customtkinter as CTk
from NewModules.newcommon import create_input, scroll_display, set_replacerbuttons

class WebhookApp():

    def lock(self,entry):
        if entry.cget("state") == "disabled":
            entry.configure(state="normal")
        else:
            entry.configure(state="disabled")

    def set_saves(self):
        for child in  self.webhook_scroll.winfo_children():
            child.destroy()

        set_replacerbuttons(self.webhook_scroll, 'Saves/WebhookData.txt', self.vars['Webhook'])

    def __init__(self, master):
        self.vars = {}
        self.master = master
        create_input(self, 'Webhook', (130, 15), (22, 35), (295, 35))
        create_input(self, 'Username', (130,65), (22, 85), (295, 84))

        self.webhook_scroll = scroll_display(
            self.master['info display'],
            (330,220),
            {
                'label':(167,5),
                'scroll':(12,30)
            },
            'Webhook'
        )

        self.set_saves()