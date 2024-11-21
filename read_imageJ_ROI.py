'''

Reads a imageJ ROI file (.roi or.zip)

if .roi, returns a ROI, which is a list of parameters

if .zip, returns a list of ROIs, where every ROI is a list of parameters

ROI types and output format:
    
["oval",x,y,width,height]
["rectangle",x,y,width,height]
["polygon",number of corners of the polygone,x1,y1,x2,y2,x3,y3,...]
["line",x1,y1,x2,y2]
["angle",x1,y1,x2,y2,x3,y3] #The three points spanning the angle are read and given in the order of clicking (vertex always in the middle):
["point",number of points,x1,y1,x2,y2,x3,y3,...]

!!! ROI of type "freehand" is re-assigned as type "polygone"

'''

from read_roi import read_roi_file, read_roi_zip
import os
from tkinter import messagebox

def onlyname(file_path):
    basename=os.path.basename(file_path)
    alist=basename.split('.')
    namebase=''
    for k in range(len(alist)-2):
        namebase=namebase+alist[k]+'.'
    namebase=namebase+alist[len(alist)-2]
    return namebase

def read_imageJ_ROI_single(path):
    
    print("Reading imageJ ROI from file:")
    print(path,"\n")
    roi = read_roi_file(path)
    
    # roi is a dictionnary
    # Get the outer key dynamically
    outer_key = next(iter(roi))
    print("Outer key:",outer_key)

    ROI = roi[outer_key]
        
    ROI_type = ROI['type']
    
    ROI_list = []
    
    if ROI_type == 'rectangle':
        ROI_list.append(ROI_type)
        ROI_list.append(ROI['left']) # upper left corner, position x
        ROI_list.append(ROI['top']) # upper left corner, position x
        ROI_list.append(ROI['width'])
        ROI_list.append(ROI['height'])
    
    if ROI_type == 'oval':
        ROI_list.append(ROI_type)
        ROI_list.append(ROI['left']) # upper left corner of the enclosing rectangle, position x
        ROI_list.append(ROI['top']) # upper left corner of the enclosing rectangle, position y
        ROI_list.append(ROI['width'])
        ROI_list.append(ROI['height'])
    
    if ROI_type == 'polygon':
        ROI_list.append(ROI_type)
        ROI_list.append(ROI['n']) # number of corners of the polygone
        
        Xs = ROI['x']
        Ys = ROI['y']
        
        for i in range(ROI['n']):
            ROI_list.append(Xs[i]) # corner i, position x
            ROI_list.append(Ys[i]) # corner i, position y

    if ROI_type == 'freehand':
        ROI_list.append('polygon')
        ROI_list.append(ROI['n']) # number of corners of the polygone
        
        Xs = ROI['x']
        Ys = ROI['y']
        
        for i in range(ROI['n']):
            ROI_list.append(Xs[i]) # corner i, position x
            ROI_list.append(Ys[i]) # corner i, position y

    if ROI_type == 'line':
        ROI_list.append(ROI_type)
        ROI_list.append(ROI['x1'])
        ROI_list.append(ROI['y1'])
        ROI_list.append(ROI['x2'])
        ROI_list.append(ROI['y2'])
    
    if ROI_type == 'angle':
        ROI_list.append(ROI_type)
        # points of the two lines spanning the angle are read and given in the order of clicking (vertex always in the middle):
        Xs = ROI['x']
        Ys = ROI['y']
        ROI_list.append(Xs[0])
        ROI_list.append(Ys[0])
        ROI_list.append(Xs[1])
        ROI_list.append(Ys[1])
        ROI_list.append(Xs[2])
        ROI_list.append(Ys[2])
    
    if ROI_type == 'point':
        ROI_list.append(ROI_type)
        ROI_list.append(ROI['n']) # number of points
        
        Xs = ROI['x']
        Ys = ROI['y']
        
        for i in range(ROI['n']):
            ROI_list.append(Xs[i]) # point i, position x
            ROI_list.append(Ys[i]) # point i, position y
    
    print("ROI parameter:", ROI_list,"\n")

    return ROI_list

def read_imageJ_ROI_zip(zip_path):
    # reads an imageJ ROIs file (.zip), filters out non-elliptic ROIs
    
    print("Reading multiple imageJ ROIs from zip file:")
    print(zip_path,"\n")
    
    ROI_dict = read_roi_zip(zip_path)

    liste = list(ROI_dict)
    print("Number of ROIs:",len(liste),"\n")
    print("ROI keys:",liste,"\n")

    ROIs_list = []
    counter = 1
    for outerkey in liste:
        
        print(f"ROI #{counter}:")
        print(outerkey)
        ROI = ROI_dict[outerkey]
        
        ROI_type = ROI['type']
        
        ROI_list = []
        
        if ROI_type == 'rectangle':
            ROI_list.append(ROI_type)
            ROI_list.append(ROI['left']) # upper left corner, position x
            ROI_list.append(ROI['top']) # upper left corner, position x
            ROI_list.append(ROI['width'])
            ROI_list.append(ROI['height'])
        
        if ROI_type == 'oval':
            ROI_list.append(ROI_type)
            ROI_list.append(ROI['left']) # upper left corner of the enclosing rectangle, position x
            ROI_list.append(ROI['top']) # upper left corner of the enclosing rectangle, position y
            ROI_list.append(ROI['width'])
            ROI_list.append(ROI['height'])
        
        if ROI_type == 'polygon':
            ROI_list.append(ROI_type)
            ROI_list.append(ROI['n']) # number of corners of the polygone
            
            Xs = ROI['x']
            Ys = ROI['y']
            
            for i in range(ROI['n']):
                ROI_list.append(Xs[i]) # corner i, position x
                ROI_list.append(Ys[i]) # corner i, position y

        if ROI_type == 'freehand':
            ROI_list.append('polygon')
            ROI_list.append(ROI['n']) # number of corners of the polygone
            
            Xs = ROI['x']
            Ys = ROI['y']
            
            for i in range(ROI['n']):
                ROI_list.append(Xs[i]) # corner i, position x
                ROI_list.append(Ys[i]) # corner i, position y

        if ROI_type == 'line':
            ROI_list.append(ROI_type)
            ROI_list.append(ROI['x1'])
            ROI_list.append(ROI['y1'])
            ROI_list.append(ROI['x2'])
            ROI_list.append(ROI['y2'])
        
        if ROI_type == 'angle':
            ROI_list.append(ROI_type)
            # points of the two lines spanning the angle are read and given in the order of clicking (vertex always in the middle):
            Xs = ROI['x']
            Ys = ROI['y']
            ROI_list.append(Xs[0])
            ROI_list.append(Ys[0])
            ROI_list.append(Xs[1])
            ROI_list.append(Ys[1])
            ROI_list.append(Xs[2])
            ROI_list.append(Ys[2])
        
        if ROI_type == 'point':
            ROI_list.append(ROI_type)
            ROI_list.append(ROI['n']) # number of points
            
            Xs = ROI['x']
            Ys = ROI['y']
            
            for i in range(ROI['n']):
                ROI_list.append(Xs[i]) # point i, position x
                ROI_list.append(Ys[i]) # point i, position y
        
        if len(ROI_list) <= 16:
            print(ROI_list,"\n")
        else:
            ROIprint = ROI_list[:16]
            ROIprint.append("...")
            print(ROIprint,"\n")
            
        ROIs_list.append(ROI_list)
        counter = counter+1

    return ROIs_list

def read_imageJ_ROI(path):
    
    name, extension = os.path.splitext(path)

    if extension == ".roi":
        ROI_list = read_imageJ_ROI_single(path)
        return ROI_list
    elif extension == ".zip":
        ROI_list = read_imageJ_ROI_zip(path)
        return ROI_list
    else:
        messagebox.showinfo('Error', r'Wrong file format. Chose ".zip" or ".roi"')
        print(r'Error reading imageJ ROIfile: Wrong file format. Chose ".zip" or ".roi"',"\n")
