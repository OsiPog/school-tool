# Packages
import json
import random
import shutil

# Modules
from src.path import Path
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
    return Path.join(options['md_dir'], interface.selected_subject + ".md")

def get_md_file_dir():
    if interface.selected_subject is None: return
    return Path.join(options["md_dir"], interface.selected_subject)

def import_pdf_menu():
    pdf_filepath = interface.open_file_dialog(filetypes=(("PDF Files", "*.pdf"),))
    md_filepath = get_md_file()
    if md_filepath and pdf_filepath:
        interface.to_clipboard(
            import_pdf(
                Path.format(pdf_filepath), 
                md_filepath)
        )
        interface.alert("Copied Markdown-tag to clipboard")

def update_markdown_file():
    md_filepath = get_md_file()
    if md_filepath:
        find_and_convert(md_filepath)
        interface.alert("Updated")


def import_blank(kind):
    md_dir = get_md_file_dir()
    if md_dir:
        xopp_path = Path.join(md_dir, f"{random.randint(0,99999999)}.xopp")
        shutil.copy(f"templates/{kind}.xopp", xopp_path)
        interface.to_clipboard(
            update_preview(xopp_path)
        )
        interface.alert("Copied Markdown-tag to clipboard")

def import_blank_portrait():
    import_blank("portrait")

def import_blank_landscape():
    import_blank("landscape")

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

    # import blank
    interface.import_portrait_button.configure(command=import_blank_portrait)
    interface.import_landscape_button.configure(command=import_blank_landscape)

    interface.tk.mainloop()

if __name__ == "__main__":
    main()