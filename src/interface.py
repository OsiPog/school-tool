from tkinter import *
from tkinter import messagebox
import tkinter.filedialog as filedialog
import os
import subprocess
import random

from src.path import Path

def func(function_call): #because lambda doesnt want to work
    nameless_function = []

    name = "_" + str(random.randint(0,9999999))

    exec(f'''
def {name}():
    {function_call}
nameless_function.append({name})''')

    return nameless_function[0]

class Interface:
    instances = []

    def __init__(self, options, window_size=(500, 500), title="App"):
        Interface.instances.append(self)

        self.restart_commands = []

        self.options = options

        self.tk = Tk()
        self.tk.title(title)
        self.tk.geometry("{}x{}+0+0".format(*window_size))
        self.tk.grid_rowconfigure(0, weight=1)
        self.tk.grid_columnconfigure(0, weight=1)
        self.tk.config()

        # Menu bar
        self.menu_bar = Menu(self.tk)
        self.tk.config(menu=self.menu_bar)

        # Settings menu
        self.settings_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        # change the markdown directory
        def md_dir_update():
            new_dir = self.open_file_dialog(folder=True)
            if new_dir:
                options["md_dir"] = Path.format(new_dir)
                self.restart()
        self.settings_menu.add_command(label="Markdown Dir", command=md_dir_update)

        # Import menu
        self.import_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Import", menu=self.import_menu)

        # Open Menu
        self.subjects = []
        self.selected_subject = None
        if self.options["md_dir"]: 
            self.setup_subject_menu()
            if self.options["selected"] is not None:
                self.change_subject(self.options["selected"])

        # Buttons
        self.frame = Frame(self.tk)
        self.frame.grid(row=0)

        # Open in Typora
        self.open_typora_button = Button(self.frame, text="Open in Typora")
        self.open_typora_button.grid(row=0)
        self.open_typora_button.configure(command=self.open_typora)

        # Update Subject
        self.update_button = Button(self.frame, text="Update Subject")
        self.update_button.grid(row=1)

        # New Graph Sheet (Portrait)
        self.import_portrait_button = Button(self.frame, text="New Graph Sheet (Portrait)")
        self.import_portrait_button.grid(row=2)

        # New Graph Sheet (Landscape)
        self.import_landscape_button = Button(self.frame, text="New Graph Sheet (Landscape)")
        self.import_landscape_button.grid(row=3)



    def setup_subject_menu(self):
        self.subject_menu = Menu(self.menu_bar, tearoff=0)

        files = os.listdir(self.options["md_dir"])

        for file in files:

            if file.split(".")[-1] == "md":
                name = file.split(".")[0]
                self.subjects.append(name)
                
                self.subject_menu.add_command(
                    label=name, 
                    command=func(f"Interface.change_subject(Interface.instances[0],'{name}')")
                )
        
        self.menu_bar.add_cascade(label="Open", menu=self.subject_menu)

    def open_file_dialog(self,folder=False, filetypes=(("All Files", "*.*"),), initialdir=None):
        if initialdir is None: initialdir = self.options["md_dir"]

        path = None
        if folder:
            path = filedialog.askdirectory(initialdir=initialdir)
        else:
            path = filedialog.askopenfilename(filetypes=filetypes,initialdir=initialdir)

        # test path for file or folder
        try:
            if path == (): return None
            elif folder:
                os.listdir(path)
            else:
                open(path)
        except FileNotFoundError:
            return None
        
        return path

    def alert(self, message, title="Info", kind='info'):
        if kind not in ('error', 'warning', 'info'):
            raise ValueError('Unsupported alert kind.')

        show_method = getattr(messagebox, 'show{}'.format(kind))
        show_method(title, message)

    def open_typora(self):
        if not self.selected_subject: return
        md_path = Path.join(self.options["md_dir"], self.selected_subject + ".md")
        subprocess.Popen(["typora",md_path])

    def change_subject(self, name):
        self.selected_subject = name
        self.tk.title(name)
        self.options["selected"] = name

    def to_clipboard(self, text):
        self.tk.clipboard_clear()
        self.tk.clipboard_append(text)

    def add_restart_command(self, func):
        self.restart_commands.append(func)

    def restart(self):
        for command in self.restart_commands: command()
        subprocess.Popen(["python", "src/restart.py"])
        exit()