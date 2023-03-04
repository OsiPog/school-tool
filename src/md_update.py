import regex as re # Regex
import random # to guarantee a unique filename
import shutil # copying files cross-platform
import os # for cross platform os control
from tempfile import gettempdir # for temp directory
from PIL import Image

from src.path import Path
from src.utils import *
from src.tools.imgs2longimg import imgs2longimg
from src.tools.pil2xopp import pil2xopp

REGEX_PATH_IN_IMG_TAG = r"((?<=\<img.+src=\").+?(?=\"))|((?<=\!\[?.+\]\().+?(?=\)))"
REGEX_WHOLE_IMAGE_TAG = r"(\<img.*(?:(?:\/\s*\>)|(?:\<\/img\>)))|(\!\[.*\]\(.*\))"
        

def find_and_convert(markdown_filepath):
    # needed later
    md_parent_dir: str = Path.get_parent_dir(markdown_filepath)
    md_file_dir: str = Path.join(
        md_parent_dir,
        Path.get_file(markdown_filepath).split(".")[0]
    )
    
    # load the file
    with open(markdown_filepath, "r", encoding="utf-8") as file:
        text: str = file.read()
        
        image_tags: list[str] = re.findall(REGEX_WHOLE_IMAGE_TAG, text)

        for image_tag in image_tags:
            image_tag = first_non_empty(image_tag)

            # Get path to image
            image_path = regex_first_match(REGEX_PATH_IN_IMG_TAG, image_tag)
            
            # Unify path
            image_path = Path.format(image_path)

            # Make the path absolute if needed
            if not Path.is_absolute(image_path):
                image_path = Path.join(md_parent_dir, image_path)
            
            # Check if the image exists if it doesnt, stop that operation
            if not os.path.exists(image_path):
                print(f"Image on path '{image_path}' does not exist.")
                continue
            
            # Refresh the preview image and go to the next image tag from here
            # if its already a schooltool image
            if '![SCHOOLTOOL]' in image_tag:
                xopp_path = Path.join(
                    md_file_dir,
                    Path.get_file(image_path).split(".")[0] + ".xopp"
                )
                update_preview(xopp_path)
                continue
            
            # Make up the xopp path
            xopp_path: str = Path.join(md_file_dir, f"{random.randint(0,99999999)}.xopp")
            
            # Create the directory if it doesnt exist yet
            if not os.path.exists((path := Path.get_parent_dir(xopp_path))):
                os.mkdir(path)
            
            # convert the image to the xopp file
            with Image.open(image_path) as im:
                tag_replacement = import_imgs_as_xopp(
                    images=[im], 
                    xopp_path=xopp_path, 
                    markdown_filepath=markdown_filepath)
            
            print(f"Converted markdown image on '{image_path}' to xopp")
            
            # Replace the old markdown image with the new schooltool div
            text = text.replace(image_tag, tag_replacement)
            
            # raise Exception("Breakpoint")
    
    # save changed text
    with open(markdown_filepath, "w", encoding="utf-8") as file:
        file.write(text)
            

def import_imgs_as_xopp(images, xopp_path, markdown_filepath):
    # needed later
    relative_md_file_dir = Path.get_file(markdown_filepath).split(".")[0]
    md_file_dir: str = Path.join(
        Path.get_parent_dir(markdown_filepath),
        relative_md_file_dir
    )
    

    filename = Path.get_file(xopp_path).split(".")[0]
    pil2xopp(images, xopp_path)
    
    # Create a first preview for that xopp
    update_preview(xopp_path)
    
    # return the custom tag for the markdown file
    return f'''[Open XOPP]({relative_md_file_dir}/{filename}.xopp)<br>\
![SCHOOLTOOL]({relative_md_file_dir}/preview/{filename}.png)'''

def import_pdf(absolute_pdf_path, markdown_filepath):
    # needed later
    md_parent_dir: str = Path.get_parent_dir(markdown_filepath)
    md_file_dir: str = Path.join(
        md_parent_dir,
        Path.get_file(markdown_filepath).split(".")[0]
    )

    # Make up the xopp path
    xopp_path: str = Path.join(md_file_dir, f"{random.randint(0,99999999)}.xopp")
    
    # Create the directory if it doesnt exist yet
    if not os.path.exists((path := Path.get_parent_dir(xopp_path))):
        os.mkdir(path)

    return import_imgs_as_xopp(
        convert_from_path(absolute_pdf_path),
        xopp_path,
        markdown_filepath
    )


def update_preview(xopp_path):
    # get the filename of the xopp file
    filename = Path.get_file(xopp_path).split(".")[0]
    
    # create a preview image for the xopp file
    
    # create a temporary folder
    temp_dir: str = Path.join(
        Path.format(gettempdir()),
        filename, # should be fine, will get deleted anyway again
    )
    os.mkdir(temp_dir)
    
    # use Xournal++ (has to be installed and in PATH) to export the xopp file
    # as an image
    os.system(f'xournalpp -i "{temp_dir}/{filename}.png" "{xopp_path}"')
    
    # Get the filepath of the preview
    preview_path: str = Path.join(
        Path.get_parent_dir(xopp_path),
        "preview",
        filename + ".png"
    )
    # Create the directory if it doesnt exist yet
    if not os.path.exists((path := Path.get_parent_dir(preview_path))):
        os.mkdir(path)
    
    # append all these images together
    images = []
    for file in os.listdir(temp_dir):
        images.append(Path.join(temp_dir, file))
    
    imgs2longimg(images, preview_path, bypass_not_enough=True, max_width=1024)
    
    # delete the temp dir
    shutil.rmtree(temp_dir)
    
    # return the path of the preview image for convenience
    return preview_path
        
        
