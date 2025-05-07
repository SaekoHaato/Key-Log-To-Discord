import customtkinter as CTk
from pynput import keyboard
from configparser import ConfigParser
from pynput import keyboard

class hotkey_buttons(CTk.CTkButton):
    global change
    global key_change

    def key_change(label,section,element,stringvar):
        global listener
        
        def key_pressed(key):
            try:
                listener.stop()
                new_key=""

                if str(key).find('Key') != -1:
                    new_key = str(key)[4:]
                    print(new_key)
                elif str(key).find("'") != -1:
                    new_key = str(key)[1:-1]

                label.configure(text=new_key)
                settings_file = ConfigParser()
                settings_file.read('Saves/settings.ini')
                settings_file.set(str(section),str(element),str(new_key))
                
                with open('Saves/settings.ini', 'w') as configfile:
                    settings_file.write(configfile)
                
                stringvar.set(str(settings_file[section][element]))
            except Exception as e:
                print(e)

        label.configure(text='Listening')
                
        listener = keyboard.Listener(on_press=key_pressed)
        listener.start()

    def change(section,element,stringvar):
        change_window = CTk.CTk()
        change_window.geometry('300x200')
        change_window.title('Key Log To Discord')

        change_frame=CTk.CTkFrame(change_window,width=300,height=200,fg_color='transparent')
        change_frame.place(x=0,y=0)

        change_button = CTk.CTkButton(change_frame,text='Click to Start Listening',width=280,height=180,fg_color='light grey',hover_color='grey',text_color='red',command=lambda:key_change(change_button,section,element,stringvar))
        change_button.pack(expand=True,pady=10,padx=10)

        change_window.mainloop()

    def __init__(self,parent,section,element,hotkey_stringvar):
        super().__init__(parent,fg_color='transparent',text_color='red',width=90,command=lambda:change(section,element,hotkey_stringvar))
        
        settings_file = ConfigParser()
        settings_file.read('Saves/settings.ini')
        
        self.configure(textvariable=hotkey_stringvar)