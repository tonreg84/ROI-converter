# writes an elliptic ROI to a file in imageJ format (.roi)

import roifile
import zipfile
import os

def writeROI2imageJ(path, x, y, width, height):
    
    # writes an elliptic ROI to a file in imageJ format (.roi)

    # Create a new ImagejRoi instance from an array of x, y coordinates:
    roi = roifile.ImagejRoi.frompoints([[x, y], [x+width-1, y+height-1]])
    roi.roitype = roifile.ROI_TYPE.OVAL
    roi.options = roifile.ROI_OPTIONS.SHOW_LABELS
    
    # Export the instance to an ImageJ ROI formatted byte string or file:
    
    out = roi.tobytes()
    out[:4]
    b'Iout'
    roi.tofile(path)
    

def writePossum2imageJzip(path, ROIs):
    # writes Possum style elliptic ROIs to a file in imageJ format (.zip)
    # input: a list of ROIs in format:
        # ['circ', 2, x1, y1, 0, w1, h1, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        # ['circ', 2, x2, y2, 0, w2, h2, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        # ...
    k = 1
    paths = []
    for roi in ROIs:
        roi_type = roi[0]
        if roi_type != 'circ':
            print("The ROI is not an elliptical ROI")
        else:
            x = roi[2]
            y = roi[3]
            w = roi[5]
            h = roi[6]
            
            ppath = path +"_"+ str(k) +"_"+ str(x)+"-"+str(y)+"-"+str(w)+"-"+str(h)+".roi"
            paths.append(ppath)
            k = k+1
            
            writeROI2imageJ(ppath, x, y, w, h)
    
    # Create a ZIP file and add files to it
    with zipfile.ZipFile(path, 'w') as zipf:
        for file in paths:
            
            zipf.write(file, arcname=os.path.basename(file))  # Add each file to the ZIP
    
    # Delete the original files after adding them to the ZIP
    for file in paths:
        os.remove(file)  # Remove each original file
