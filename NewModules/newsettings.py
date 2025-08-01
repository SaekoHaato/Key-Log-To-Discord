import customtkinter as CTk
from configparser import ConfigParser
from pynput import keyboard
import win32con
import win32gui

class ListenerApp(CTk.CTk):

    def listen(self) -> None:
        
        def key_pressed(key) -> None:
            self.listener.stop()
    
            key: str = key.__str__()

            if key.startswith("'"):
                key = key[1:-1]
            elif key.startswith('Key.'):
                key = key[4:]

            settings_file: ConfigParser = ConfigParser()
            settings_file.read('Saves/settings.ini')

            settings_file[self.section][self.element.get()] = key

            with open('Saves/settings.ini','w') as file:
                settings_file.write(file)

            self.textvar.set(key)

            print(key)
            self.button.configure(text=key,state='normal')

        self.button.configure(text='Listening...',state='disabled')

        self.listener: keyboard.Listener = keyboard.Listener(on_press=key_pressed)
        self.listener.start()

    def __init__(self, placement: tuple[CTk.StringVar,CTk.StringVar], textvar: CTk.StringVar) -> None:
        super().__init__()

        self.section, self.element = placement
        self.textvar: CTk.StringVar = textvar

        self.geometry('300x200')
        self.title(f'Key Log To Discord: Settings: {self.element.get()}')
        self.resizable(False,False)

        self.button: CTk.CTkButton = CTk.CTkButton(
            self,
            fg_color='light grey',
            text_color='red',
            hover_color='grey',
            text='Click to Start Listening',
            command=self.listen
        )
        self.button.pack(expand=True,fill='both',pady=5,padx=5)

        self.mainloop()


class ListenerButton(CTk.CTkButton):

    def __init__(self, master: CTk.CTkFrame, placement: tuple[CTk.StringVar,CTk.StringVar], textvar: CTk.StringVar) -> None:
        super().__init__(
            master,
            fg_color='transparent',
            text_color='red',
            command=lambda: ListenerApp(placement, textvar),
            textvariable=textvar,
            width=100
        )


class EntryApp(CTk.CTk):

    def save(self) -> None:
        text: str = self.entry.get()

        settings_file: ConfigParser = ConfigParser()
        settings_file.read('Saves/settings.ini')

        settings_file.remove_option(self.section, self.element)
        settings_file.set(self.section, text, self.value.get())

        with open('Saves/settings.ini','w') as file:
            settings_file.write(file)

        self.textvar.set(text)

        self.after(150,self.destroy)

    def __init__(self, placement: tuple[str, CTk.StringVar, CTk.StringVar], textvar: CTk.StringVar):
        super().__init__()
        self.geometry('300x200')
        self.title(f'Key Log To Discord: Settings: {textvar.get()}')
        self.resizable(False,False)

        self.textvar = textvar
        self.section, self.element, self.value = placement

        self.entry = CTk.CTkEntry(self,placeholder_text='Quick Send Message Here')
        self.entry.pack(side='top',pady=50,fill='x',padx=15)

        save = CTk.CTkButton(self,text='Save',command=self.save)
        save.pack()

        self.mainloop()


class EntryButton(CTk.CTkButton):

    def __init__(self, master: CTk.CTkFrame, placement: tuple[str, CTk.StringVar, CTk.StringVar], textvar: CTk.StringVar) -> None:
        super().__init__(
            master,
            fg_color='transparent',
            text_color='red',
            width=100,
            textvariable=textvar,
            command=lambda: EntryApp(placement, textvar)
        )


class BoolButton(CTk.CTkButton):

    def __init__(self, master: CTk.CTkFrame, textvar: CTk.StringVar, setting: str)  -> None:
        super().__init__(
            master=master,
            textvariable=textvar,
            fg_color='transparent',
            text_color='red',
            command=self.on_click
        )
        self.setting=setting

    def on_click(self) -> None:
        """Makes value swap between True and False and saves it in  settings.ini
        """

        value: str = 'True' if self._textvariable.get() == 'False' else 'False'
        self._textvariable.set(value)

        file: ConfigParser = ConfigParser()
        file.read('Saves/settings.ini')

        file['settings'][self.setting] = value.lower()

        with open('Saves/settings.ini', 'w') as content:
            file.write(content)


class SettingsApp(CTk.CTk):

    def __init__(self) -> None:
        hwnd: int = win32gui.FindWindow(None, 'Key Log to Discord: Settings')
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return

        super().__init__()

        self.resizable(False,False)
        self.geometry('400x350')
        self.title('Key Log to Discord: Settings')

        self.hotkey_frame: CTk.CTkFrame = CTk.CTkFrame(self,fg_color='grey')
        self.hotkey_frame.pack(side='left',fill='both',padx=2.5,pady=10,expand=True)

        self.key_frame: CTk.CTkFrame = CTk.CTkFrame(self,fg_color='grey')
        self.key_frame.pack(side='left',fill='both',padx=2.5,pady=10,expand=True) 

        settings_file: ConfigParser = ConfigParser()
        settings_file.read('Saves/settings.ini')

        for section in settings_file.sections():
            hotkey_section: CTk.CTkFrame = CTk.CTkFrame(
                self.hotkey_frame,
                fg_color='transparent'
            )

            key_section: CTk.CTkFrame = CTk.CTkFrame(
                self.key_frame,
                fg_color='transparent'
            )

            hotkey_section.pack(pady=3)
            key_section.pack(pady=3)

            hotkey_section_label: CTk.CTkLabel = CTk.CTkLabel(
                hotkey_section,
                fg_color='grey',
                text=section.upper(),
                font=('CTkFont',11),
                text_color='white'
            )

            key_section_label: CTk.CTkLabel = CTk.CTkLabel(
                key_section,
                fg_color='grey',
                text=section.upper(),
                font=('CTkFont',11),
                text_color='white'
            )

            hotkey_section_label.pack(side='top',pady=3)
            key_section_label.pack(side='top',pady=3)

            for element, value in settings_file[section].items():
                element_textvar = CTk.StringVar(hotkey_section,value=element)
                button_textvar = CTk.StringVar(key_section,value=value)

                # Hotkey Section
                match section:
                    case'quick send':
                        element_button: EntryButton = EntryButton(
                            hotkey_section,
                            (section, element, button_textvar),
                            element_textvar
                        )
                        element_button.pack()
                    case _:
                        element_label: CTk.CTkLabel = CTk.CTkLabel(
                            hotkey_section,
                            fg_color='transparent',
                            text_color='red',
                            text=element
                        )
                        element_label.pack()
                
                # Key Section
                value_button: ListenerButton | BoolButton

                match section:
                    case 'settings':
                        button_textvar.set(button_textvar.get().capitalize())
                        value_button = BoolButton(
                            key_section,
                            button_textvar,
                            element
                        )
                    case _:
                        value_button = ListenerButton(
                            key_section,
                            (section, element_textvar),
                            button_textvar
                        )
                value_button.pack()

        self.mainloop()

if __name__ == '__main__':
    App = SettingsApp()