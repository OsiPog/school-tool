from tkinter import *
from tkinter import messagebox
import tkinter.filedialog as filedialog

import os

class Interface:
    def __init__(self, options, window_size=(500, 500), title="App"): 
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
                options["md_dir"] = new_dir
                self.alert("Restart required")
        self.settings_menu.add_command(label="Markdown Dir", command=md_dir_update)

        # Import menu
        self.import_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Import", menu=self.import_menu)

        # Open Menu
        self.subjects = []
        self.selected_subject = None
        if self.options["md_dir"]: 
            print(self.options["md_dir"])
            self.setup_subject_menu()
            self.selected_subject = self.subjects[0]

        # Buttons
        self.frame = Frame(self.tk)
        self.frame.grid(row=0)

        self.update_button = Button(self.frame, text="Update Subject")
        self.update_button.grid(row=0)



    def setup_subject_menu(self):
        self.subject_menu = Menu(self.menu_bar, tearoff=0)

        files = os.listdir(self.options["md_dir"])

        for file in files:

            if file.split(".")[-1] == "md":
                name = file.split(".")[0]
                self.subjects.append(name)

                def select_subject():
                    self.selected_subject = name
                    self.clicked_on_subject_name(name)
                    self.tk.title(name)

                self.subject_menu.add_command(label=name, command=select_subject)
        
        self.menu_bar.add_cascade(label="Open", menu=self.subject_menu)

    def open_file_dialog(self,folder=False, filetypes=(("All Files", "*.*"),)):
        path = None
        if folder:
            path = filedialog.askdirectory()
        else:
            path = filedialog.askopenfilename(filetypes=filetypes)

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


    # please override
    def clicked_on_subject_name(self, name):
        pass

    def to_clipboard(self, text):
        self.tk.clipboard_clear()
        self.tk.clipboard_append(text)