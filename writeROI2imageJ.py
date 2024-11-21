'''

creates a imageJ ROI file (.roi or.zip)

if input is a single ROI (list of parameters), creates a .roi file

if input is a list of ROIs (list of ROIs, where every ROI is a list of parameters) creates a .zip file

ROI types and input format:

["oval",x,y,width,height]
["rectangle",x,y,width,height]
["polygon",number of corners of the polygone,x1,y1,x2,y2,x3,y3,...]
["line",x1,y1,x2,y2] # Cannot write ROIs of type "line". Dummy "point" ROI is written to file instead.
["angle",x1,y1,x2,y2,x3,y3] #The three points spanning the angle are read and given in the order of clicking (vertex always in the middle).
["point",number of points,x1,y1,x2,y2,x3,y3,...]

'''

from tkinter import messagebox
import roifile
import zipfile
import os
import tempfile
import shutil

def writeROI2imageJ_single(ROI,path):
    
    print("Writing imageJ ROI to file:")
    print(path,"\n")
    
    ROI_type = ROI[0]
    
    if ROI_type == "oval":

        # Create a new ImagejRoi instance from an array of x, y coordinates:
        roi = roifile.ImagejRoi.frompoints([[ROI[1], ROI[2]], [ROI[1]+ROI[3]-1, ROI[2]+ROI[4]-1]])
        roi.roitype = roifile.ROI_TYPE.OVAL
        roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
        
        # Export the instance to an ImageJ ROI formatted byte string or file:
        roi.tofile(path)

    elif ROI_type == "rectangle":

        # Create a new ImagejRoi instance from an array of x, y coordinates:
        roi = roifile.ImagejRoi.frompoints([[ROI[1], ROI[2]], [ROI[1]+ROI[3]-1, ROI[2]+ROI[4]-1]])
        roi.roitype = roifile.ROI_TYPE.RECT
        roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
        
        # Export the instance to an ImageJ ROI formatted byte string or file:
        roi.tofile(path)
        
    elif ROI_type == "polygon":
        
        corner_list = []
        
        for k in range(int((len(ROI)-2)/2)):
            corner=[]
            corner.append(ROI[2*k+2])
            corner.append(ROI[2*k+3])
            corner_list.append(corner)
        
        # Create a new ImagejRoi instance from an array of x, y coordinates:
        roi = roifile.ImagejRoi.frompoints(corner_list)
        roi.roitype = roifile.ROI_TYPE.POLYGON
        roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
        
        # Export the instance to an ImageJ ROI formatted byte string or file:
        roi.tofile(path)
        
    elif ROI_type == "line":

        # # Create a new ImagejRoi instance from an array of x, y coordinates:
        # roi = roifile.ImagejRoi.frompoints( [ [ROI[1], ROI[2]] , [ROI[3], ROI[4]] ] )
        # roi.roitype = roifile.ROI_TYPE.LINE
        # roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
        
        # # Export the instance to an ImageJ ROI formatted byte string or file:
        # roi.tofile(path)
        
        messagebox.showinfo('Attention!', r'Cannot write ROIs of type "line". Dummy "point" ROI is written to file instead to keep ROI numbering.')
        print(r'Line ROI, cannot be writen to file. Dummy "point" ROI is written to file instead to keep ROI numbering.',"\n")
        
        point_list = []
        p1=[]
        p1.append(int(ROI[1]))
        p1.append(int(ROI[2]))
        p2=[]
        p2.append(int(ROI[3]))
        p2.append(int(ROI[4]))
        point_list.append(p1)
        point_list.append(p2)
        
        # Create a new ImagejRoi instance from an array of x, y coordinates:
        roi = roifile.ImagejRoi.frompoints(point_list)
        roi.roitype = roifile.ROI_TYPE.POINT
        roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
        
        # Export the instance to an ImageJ ROI formatted byte string or file:
        roi.tofile(path)
        
    elif ROI_type == "angle":

        point_list = []
        p1=[]
        p1.append(int(ROI[1]))
        p1.append(int(ROI[2]))
        p2=[]
        p2.append(int(ROI[3]))
        p2.append(int(ROI[4]))
        p3=[]
        p3.append(int(ROI[5]))
        p3.append(int(ROI[6]))
        point_list.append(p1)
        point_list.append(p2)
        point_list.append(p3)
        
        # Create a new ImagejRoi instance from an array of x, y coordinates:
        roi = roifile.ImagejRoi.frompoints(point_list)
        roi.roitype = roifile.ROI_TYPE.ANGLE
        roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
        
        # Export the instance to an ImageJ ROI formatted byte string or file:
        roi.tofile(path)
        
    elif ROI_type == "point":
        
        point_list = []
        
        for k in range(int((len(ROI)-2)/2)):
            p=[]
            p.append(ROI[2*k+2])
            p.append(ROI[2*k+3])
            point_list.append(p)
        
        # Create a new ImagejRoi instance from an array of x, y coordinates:
        roi = roifile.ImagejRoi.frompoints(point_list)
        roi.roitype = roifile.ROI_TYPE.POINT
        roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
        
        # Export the instance to an ImageJ ROI formatted byte string or file:
        roi.tofile(path)
        
    print("ROI succesfully written to file.","\n")
    
def writeROI2imageJ_zip(ROI_list,path):
    
    print("Writing multiple imageJ ROIs to zip file:")
    print(path,"\n")

    # Step 1: Create a temporary folder
    ROI_temp_dir = tempfile.mkdtemp()
    print(f"Temporary directory created: {ROI_temp_dir}","\n")
    
    try:
        # Create a ZIP file and add files to it
        with zipfile.ZipFile(path, 'w') as zipf:
        
            counter = 1
            for ROI in ROI_list:
                
                print(f"ROI #{counter}:")
                
                if len(ROI) <= 16:
                    print(ROI)
                else:
                    ROIprint = ROI[:16]
                    ROIprint.append("...")
                    print(ROIprint)    
                
                ROI_type = ROI[0]
                
                temp_path = ROI_temp_dir +"/"+ str(counter) +"_"+ ROI_type + ".roi"
                print("Temporary ROI save path:")
                print(temp_path,"\n")
                counter = counter+1
                
                if ROI_type == "oval":
        
                    # Create a new ImagejRoi instance from an array of x, y coordinates:
                    roi = roifile.ImagejRoi.frompoints([[ROI[1], ROI[2]], [ROI[1]+ROI[3]-1, ROI[2]+ROI[4]-1]])
                    roi.roitype = roifile.ROI_TYPE.OVAL
                    roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
                    
                    # Export the instance to an ImageJ ROI formatted byte string or file:
                    roi.tofile(temp_path)
        
                elif ROI_type == "rectangle":
        
                    # Create a new ImagejRoi instance from an array of x, y coordinates:
                    roi = roifile.ImagejRoi.frompoints([[ROI[1], ROI[2]], [ROI[1]+ROI[3]-1, ROI[2]+ROI[4]-1]])
                    roi.roitype = roifile.ROI_TYPE.RECT
                    roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
                    
                    # Export the instance to an ImageJ ROI formatted byte string or file:
                    roi.tofile(temp_path)
                    
                elif ROI_type == "polygon":
                    
                    corner_list = []
                    
                    for k in range(int((len(ROI)-2)/2)):
                        corner=[]
                        corner.append(ROI[2*k+2])
                        corner.append(ROI[2*k+3])
                        corner_list.append(corner)
                    
                    # Create a new ImagejRoi instance from an array of x, y coordinates:
                    roi = roifile.ImagejRoi.frompoints(corner_list)
                    roi.roitype = roifile.ROI_TYPE.POLYGON
                    roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
                    
                    # Export the instance to an ImageJ ROI formatted byte string or file:
                    roi.tofile(temp_path)
                    
                elif ROI_type == "line":
                    
                    messagebox.showinfo('Attention!', r'Cannot write ROIs of type "line". Dummy "point" ROI is written to file instead to keep ROI numbering.')
                    print(r'Line ROI, cannot be writen to file. Dummy "point" ROI is written to file instead to keep ROI numbering.',"\n")
                    
                    point_list = []
                    p1=[]
                    p1.append(int(ROI[1]))
                    p1.append(int(ROI[2]))
                    p2=[]
                    p2.append(int(ROI[3]))
                    p2.append(int(ROI[4]))
                    point_list.append(p1)
                    point_list.append(p2)
                    
                    # Create a new ImagejRoi instance from an array of x, y coordinates:
                    roi = roifile.ImagejRoi.frompoints(point_list)
                    roi.roitype = roifile.ROI_TYPE.POINT
                    roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
                    
                    # Export the instance to an ImageJ ROI formatted byte string or file:
                    roi.tofile(temp_path)
                    
                elif ROI_type == "angle":
                    
                    point_list = []
                    p1=[]
                    p1.append(int(ROI[1]))
                    p1.append(int(ROI[2]))
                    p2=[]
                    p2.append(int(ROI[3]))
                    p2.append(int(ROI[4]))
                    p3=[]
                    p3.append(int(ROI[5]))
                    p3.append(int(ROI[6]))
                    point_list.append(p1)
                    point_list.append(p2)
                    point_list.append(p3)
                    
                    # Create a new ImagejRoi instance from an array of x, y coordinates:
                    roi = roifile.ImagejRoi.frompoints(point_list)
                    roi.roitype = roifile.ROI_TYPE.ANGLE
                    roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
                    
                    # Export the instance to an ImageJ ROI formatted byte string or file:
                    roi.tofile(temp_path)
                    
                elif ROI_type == "point":
                    
                    point_list = []
                    
                    for k in range(int((len(ROI)-2)/2)):
                        p=[]
                        p.append(ROI[2*k+2])
                        p.append(ROI[2*k+3])
                        point_list.append(p)
                    
                    # Create a new ImagejRoi instance from an array of x, y coordinates:
                    roi = roifile.ImagejRoi.frompoints(point_list)
                    roi.roitype = roifile.ROI_TYPE.POINT
                    roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
                    
                    # Export the instance to an ImageJ ROI formatted byte string or file:
                    roi.tofile(temp_path)
            
                zipf.write(temp_path, arcname=os.path.basename(temp_path))  # Add each file to the ZIP
    
        print("ROIs succesfully written to file.","\n")
    
    except (ValueError, TypeError):
        # Show an error if the input was not a valid integer
        messagebox.showerror("Error", "An erroroccured while writing the ROI file.")
        print("Error: ROI zipfile not created. An error occured while writing the file.","\n")
    
    finally:
        # Step 3: Clear the files and folder
        shutil.rmtree(ROI_temp_dir)
        print(f"Temporary directory {ROI_temp_dir} and its contents have been removed.","\n")