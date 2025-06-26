import customtkinter as CTk
from configparser import ConfigParser

def create_input(self, name: str, label_cords: tuple[int,int], entry_cords: tuple[int,int], lock_cords: tuple[int,int]) -> None:
    """Creates Entry

    Args:
        name (str): Name for Label of Entry
        label_cords (tuple[int,int]): Ordered pair of (x,y) coordinates for Label
        entry_cords (tuple[int,int]): Ordered pair of (x,y) coordinates for Entry
        lock_cords (tuple[int,int]): Ordered pair of (x,y) coordinates for Lock
    """

    x,y = label_cords
    label: CTk.CTkLabel = CTk.CTkLabel(
        self.master['input frame'],
        width=15,
        height=10,
        text=name,
        text_color="white",
        font=("CTkFont", 14),
    )
    label.place(x=x, y=y)

    self.vars[name] = CTk.StringVar(self.master['input frame'])

    ex, ey = entry_cords
    entry: CTk.CTkEntry = CTk.CTkEntry(
        self.master['input frame'], width=270, height=10, textvariable=self.vars[name]
    )
    entry.place(x=ex, y=ey)

    lx, ly = lock_cords
    lock: CTk.CTkCheckBox = CTk.CTkCheckBox(
        self.master['input frame'], text='', command=lambda: self.lock(entry)
    )
    lock.place(x=lx, y=ly)


def scroll_display(master: CTk.CTkFrame, size: tuple[int,int], places: dict[str,tuple[int,int]], text: str) -> CTk.CTkScrollableFrame:
    """_summary_

    Args:
        master (CTk.CTkFrame): Master Frame to put ScrollableFrame
        size (tuple[int,int]): Size of ScrollableFrame
        places (dict[str,tuple[int,int]]): Dictionary of coordinates for each Widget
        text (str): Name of ScrollableFrame

    Returns:
        CTk.CTkScrollableFrame: Frame
    """

    label: CTk.CTkLabel = CTk.CTkLabel(
        master=master,
        text=text,
        text_color='black'
    )
    x,y=places['label']
    label.place(x=x,y=y)

    width, height = size
    scroll: CTk.CTkScrollableFrame = CTk.CTkScrollableFrame(
        master=master,
        width=width,
        height=height,
        fg_color='#b1b1b1',
        corner_radius=5
    )
    x,y=places['scroll']
    scroll.place(x=x,y=y)

    return scroll


class ReplacerButton(CTk.CTkButton):

    def __init__(self, master: CTk.CTkFrame, var: CTk.StringVar, save: tuple[str, str]) -> None:
        super().__init__(
            master=master,
            text=save[0],
            command=lambda: var.set(save[1])
        )
        self.pack(pady=2.5)


def set_replacerbuttons(master: CTk.CTkFrame, section: str, var: CTk.StringVar) -> None:
    """Creates ReplacerButtons

    Args:
        master (CTk.CTkFrame): Where to place Button
        section (str): What section in saves.ini button corrosponds to
        var (CTk.StringVar): StringVar
    """

    file = ConfigParser()
    file.read('Saves/saves.ini')

    for key, value in file[section].items():
        ReplacerButton(master,var,(key, value))