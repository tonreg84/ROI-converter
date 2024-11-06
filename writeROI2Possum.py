# write elliptic ROIs to a file in "Possum regions format"

import struct

def writeROI2Possum(ROI_list, reg_file_path):
    
    #ROI_list[i]: x pos, y pos, width, height  (all integer)
    
    nREG = len(ROI_list)
    
    type_string = "circ"
    bstring = type_string.encode('utf-8')
    
    with open(reg_file_path, 'wb') as fileID:
        
        #write number of ROIs to regions file
        nREGdata=struct.pack('i', nREG)
        fileID.write(nREGdata)
        
        # write all ROI specs to regions file
        for ROI in ROI_list:
            binary_data = struct.pack('4siiiiiii', bstring, 2, ROI[0], ROI[1], 0, ROI[2], ROI[3], 1)
            fileID.write(binary_data)
            
    fileID.close