from read_roi import read_roi_file
import zipfile
import os
import tempfile

def onlyname(file_path):
    basename=os.path.basename(file_path)
    alist=basename.split('.')
    namebase=''
    for k in range(len(alist)-2):
        namebase=namebase+alist[k]+'.'
    namebase=namebase+alist[len(alist)-2]
    return namebase

def read_imageJ_ROI(path):
    # reads an elliptic imageJ ROI from file (.roi)
                
    roi = read_roi_file(path)
    
    # roi is a dictionnary
    # Get the outer key dynamically
    outer_key = next(iter(roi))
    print(outer_key)

    roi_para = roi[outer_key]

    roi_type = roi_para['type']
    print(roi_type)

    if roi_type != 'oval':
        print("The ROI is not an elliptical ROI")
    else:
        # Get the bounds of the ellipse
        x = roi_para['left']
        y = roi_para['top']
        w = roi_para['width']
        h = roi_para['height']
        print("x,y,width,height:",x,y,w,h)

    return x,y,w,h

def read_imageJ_ROI_ZIP(zip_path):
    # reads an imageJ ROIs file (.zip), filters out non-elliptic ROIs
    
    # create a temporary directory using the context manager
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
    
        unzip_path = tmpdirname + "/unzip_dir"
        
        ROI_list = []
        extracted_files = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            # List all files in the order they are read
            for file_info in zip_ref.infolist():
                extracted_files.append(file_info.filename)
        print(f"Files extracted from '{zip_path}' in the order of reading:")
            
        for roi_name in extracted_files:
            print(roi_name)
    
            roi_path = unzip_path + "\\" + roi_name
            
            roi = read_roi_file(roi_path)
    
            for roi_name, roi in roi.items():
                print(roi['type'])
                
                if roi['type'] != 'oval':
                    print("The ROI is not an elliptical ROI")
                else:
                    # Get the bounds of the ellipse
                    x = roi['left']
                    y = roi['top']
                    w = roi['width']
                    h = roi['height']
                    print(x,y,w,h)
                    ROI_list.append([x,y,w,h])

    return ROI_list