'''

Writes ROIs to a file in "Possum regions format" (.reg)

The inputs needs to be a list of ROIs, where every ROI is a list of parameters.
ROI types and input format:
    
["circ",x,y,width,height]
["rect",x,y,width,height]
["poly",number of corners of the polygone,x1,y1,x2,y2,x3,y3,...]
["poin",Y,X]

'''

import struct

def writeROI2Possum(ROI_list, reg_file_path):
    
    print("Writing multiple Possum ROIs to file:")
    print(reg_file_path,"\n")
    
    nREG = len(ROI_list)
        
    with open(reg_file_path, 'wb') as fileID:
        
        #write number of ROIs to regions file
        nREGdata=struct.pack('i', nREG)
        fileID.write(nREGdata)
        
        counter = 1
        # write all ROI specs to regions file
        for ROI in ROI_list:
            
            print(f"ROI #{counter}:")
            if len(ROI) <= 16:
                print(ROI,"\n")
            else:
                ROIprint = ROI[:16]
                ROIprint.append("...")
                print(ROIprint,"\n")    
            
            if ROI[0] == "circ":
                
                type_string = "circ"
                bstring = type_string.encode('utf-8')

                binary_data = struct.pack('4siiiiiii', bstring, 2, ROI[1], ROI[2], 0, ROI[3], ROI[4], 1)
                fileID.write(binary_data)
                
            if ROI[0] == "rect":
                
                type_string = "rect"
                bstring = type_string.encode('utf-8')

                binary_data = struct.pack('4siiiiiii', bstring, 2, ROI[1], ROI[2], 0, ROI[3], ROI[4], 1)
                fileID.write(binary_data)
                
            if ROI[0] == "poin":
                
                type_string = "poin"
                bstring = type_string.encode('utf-8')

                binary_data = struct.pack('4siiii', bstring, 3, ROI[1], ROI[2], 1)
                fileID.write(binary_data)
            
            if ROI[0] == "poly":
                
                type_string = "poly"
                bstring = type_string.encode('utf-8')
                
                number_corners = ROI[1]
                
                fileID.write(struct.pack("4si", bstring, number_corners))
                
                for k in range(number_corners):
                    binary_data = struct.pack("iii", ROI[2*k+2], ROI[2*k+3], k)
                    fileID.write(binary_data)
            
            counter = counter +1
            
    fileID.close
    print("ROIs succesfully written to file.","\n")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    