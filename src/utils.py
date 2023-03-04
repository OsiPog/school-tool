import regex as re
from pdf2image import convert_from_path # pillow doesnt support reading pdf

# re.findall returns a list of tuples, this here returns the first non empty
# match in such a tuple
def first_non_empty(tup):
    for part in tup:
        if part: return part
        
def regex_first_match(pattern, string):
    match = re.search(pattern, string)
    return match.group()