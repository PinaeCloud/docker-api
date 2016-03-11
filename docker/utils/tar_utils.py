# coding=utf-8

import os
import os.path
import tarfile
import tempfile

from text import string_utils as str_utils
from text import regex_utils as reg_utils

def tar(filelist, tar_path = None, exclude = None):
        
    if str_utils.is_not_empty(tar_path):
        t = tarfile.open(name = tar_path, mode = __get_tar_mode(tar_path))
    else: 
        fileobj = tempfile.NamedTemporaryFile()
        t = tarfile.open(mode = 'w', fileobj=fileobj)
    
    exclude = exclude or []

    if isinstance(filelist, str):
        filepath = os.path.abspath(filelist)
        filelist = []
        if os.path.isdir(filepath):
            for root, dirs, files in os.walk(filepath):
                for _file in files:
                    match = True
                    for pattern in exclude:
                        if reg_utils.check_line(pattern, _file):
                            match = False
                            break
                    if match:
                        filelist.append(os.path.join(root, _file))
        elif os.path.isfile(filepath):
            filelist = [filelist]
            
    if isinstance(filelist, list):     
        for _file in filelist:
            t.add(_file)

    t.close()
    
    if str_utils.is_not_empty(tar_path):
        return tar_path
    else:
        fileobj.seek(0)
        return fileobj

def untar(tar_data, target_path = None, extract_file = None):
    
    if isinstance(tar_data, str):
        t = tarfile.open(name = tar_data, mode = __get_tar_mode(tar_data))
    else:
        t = tarfile.open(mode = 'r', fileobj = tar_data)
        
    if extract_file != None:
        if extract_file.startswith('/'):
            extract_file = extract_file[1:]
        if target_path != None:
            t.extract(extract_file, target_path)
            result = os.path.join(target_path, extract_file) 
        else:
            f = t.extractfile(extract_file)
            result = f.read()
    else:
        result = []
        filelist = t.getnames()
        for _file in filelist :
            t.extract(_file, target_path)
            result.append(os.path.join(target_path, _file))
            
    t.close()
    return result
    

def __get_tar_mode(filename):
    if filename.endswith('gz'):
        mode = 'w:gz'
    elif filename.endswith('bz2'):
        mode = 'w:bz2'
    else:
        mode = 'w'
    return mode
