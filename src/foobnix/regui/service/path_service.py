#-*- coding: utf-8 -*-
'''
Created on 3 окт. 2010

@author: ivan
'''
import os.path, sys
import logging

def get_foobnix_resourse_path_by_name(filename):
    if not filename:
        return None
    paths = ("/usr/local/share/pixmaps",
             "/usr/share/pixmaps",
             "/usr/share/foobnix",
             "/usr/local/share/foobnix",
             "pixmaps",
             "foobnix/pixmaps",
             "share/pixmaps",
             "./../../..",
             "./../../",
             "./../pixmaps",
             "./",
             sys.path[1],
             filename)
    for path in paths:
        full_path = os.path.join(path, filename)
        if os.path.isfile(full_path):
            return full_path
    
    logging.error("File " + filename + " not found")
    #raise TypeError, "******* WARNING: File " + filename + " not found *******"
