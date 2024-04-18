import customtkinter as CTk

class data_buttons(CTk.CTkFrame):
    def __init__(self, parent, log,size,instance):
        super().__init__(master = parent,width=size[0],height=size[1],fg_color='transparent',bg_color='transparent')
        if log != "":
            self.pack()

            CTk.CTkButton(self,text=log,command=lambda:instance.set(log),width=size[0]).pack(side = "left")