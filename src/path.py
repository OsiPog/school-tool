import regex as re

from src.utils import *

class Path:
    # Unify a path string
    def format(path):
        return re.sub(r"(\\+)|(\/\/+)", "/", path)
    
    def join(*args):
        result_path = args[0]
        
        for arg in args[1:]:
            result_path += "/" + str(arg)
            
        return Path.format(result_path)
    
    def get_file(path):
        
        # return the path if path is just a file
        if not re.search(r"[\\\/]", path): return path
        
        else:
            return regex_first_match(
                r"(?<=[\\\/])(.(?![\\\/]))+$", path)
            
    def get_parent_dir(path):
        segments = Path.format(path).split("/")
        segments.pop()
        return "/".join(segments)
    
    def is_absolute(path):
        return bool(re.search(r"^(([a-zA-Z]:)|\/)", path))
    
    def get_shared_absolute_dir(path0, path1):
        if not ( Path.is_absolute(path0) and Path.is_absolute(path1)):
            raise "Cannot compare none-absolute paths."
        
        shared_path: list = []
        
        segs0 = Path.format(path0).split("/")
        segs1 = Path.format(path1).split("/")
        
        for i in range( min((len(segs0), len(segs1))) ):
            if (segs0[i] != segs1[i]): break
            
            shared_path.append(segs0[i])
        
        return "/".join(shared_path)