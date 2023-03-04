# Packages
import json

# Modules
from src.md_update import find_and_convert, import_imgs_as_xopp, update_preview, import_pdf
from src.interface import Interface

def save_options():
    with open("options.json", "w") as file:
        json.dump(options, file)

def on_exit():
    save_options()
    exit()

def get_md_file():
    if interface.selected_subject is None: return
    return f"{options['md_dir']}/{interface.selected_subject}.md"

def import_pdf_menu():
    pdf_filepath = interface.open_file_dialog(filetypes=(("PDF Files", "*.pdf"),))
    md_filepath = get_md_file()
    if md_filepath and pdf_filepath:
        interface.to_clipboard(import_pdf(pdf_filepath, md_filepath))

def update_markdown_file():
    md_filepath = get_md_file()
    if md_filepath:
        find_and_convert(md_filepath)


# loading options
options = {
    "md_dir": None,
    "selected": None
}
try:
    with open("options.json", "r") as file:
        options = json.load(file)
except Exception as err:
    print(err)
    save_options()

interface = Interface(options, window_size=(200,200), title="SchoolTool")

def main():
    # window closing event
    interface.tk.protocol("WM_DELETE_WINDOW", on_exit)

    # Import PDF menu entry
    interface.import_menu.add_command(label="PDF", command=import_pdf_menu)

    # Update command
    interface.update_button.configure(command=update_markdown_file)

    interface.tk.mainloop()

if __name__ == "__main__":
    main()