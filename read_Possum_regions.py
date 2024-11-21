'''

Reads a Possum regions file (.reg)

Returns a list of ROIs, where every ROI is a list of parameters.

ROI types and output format:
    
["circ",x,y,width,height]
["rect",x,y,width,height]
["poly",number of corners of the polygone,x1,y1,x2,y2,x3,y3,...]
["poin",Y,X]

'''

from numpy import fromfile

def read_Possum_regions(regions_file):
    
    print("Reading multiple Possum ROIs from file:")
    print(regions_file,"\n")

    fileID = open(regions_file, 'rb')
    nREG = fromfile(fileID, dtype="i4", count=1)
    nREG=nREG[0]
    print("Number of ROIs:",nREG,"\n")
    parameters_list=[]
    for k in range(nREG):
        print(f"ROI #{k+1}:")
        parameters_k=[None] * 1000
        bstring=fileID.read(4)
        
        ROI_type = bstring.decode('utf-8')
        
        if ROI_type == "circ":
            
            parameters_k=[None] * 5
            
            parameters_k[0] = ROI_type
            
            numpara = fromfile(fileID, dtype="i4", count=1) # number of parameters, should be 2
            posx = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position x (upper left corner of the enclosing rectangle, position x)
            parameters_k[1]=posx[0]
            posy = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position y (upper left corner of the enclosing rectangle, position y)
            parameters_k[2]=posy[0]
            counter1 = fromfile(fileID, dtype="i4", count=1) # param counter,should be 0
            dimx = fromfile(fileID, dtype="i4", count=1) # dimension x
            parameters_k[3]=dimx[0]
            dimy = fromfile(fileID, dtype="i4", count=1) # dimension y
            parameters_k[4]=dimy[0]
            counter2 = fromfile(fileID, dtype="i4", count=1) # param counter, should be 1
            
        elif ROI_type == "rect":
            
            parameters_k=[None] * 5
            
            parameters_k[0] = ROI_type
            
            numpara = fromfile(fileID, dtype="i4", count=1) # number of parameters, should be 2
            posx = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position x (upper left corner, position x)
            parameters_k[1]=posx[0]
            posy = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position y (upper left corner, position y)
            parameters_k[2]=posy[0]
            counter1 = fromfile(fileID, dtype="i4", count=1) # param counter,should be 0
            dimx = fromfile(fileID, dtype="i4", count=1) # dimension x
            parameters_k[3]=dimx[0]
            dimy = fromfile(fileID, dtype="i4", count=1) # dimension y
            parameters_k[4]=dimy[0]
            counter2 = fromfile(fileID, dtype="i4", count=1) # param counter, should be 1
            
        elif ROI_type == "poly":
            
            numpara = fromfile(fileID, dtype="i4", count=1) # number of corners of the polygone
            
            parameters_k = [None] * (numpara[0]*2 + 2)
            
            parameters_k[0] = ROI_type
            
            parameters_k[1]=numpara[0]
            
            for i in range(numpara[0]):
                posx = fromfile(fileID, dtype="i4", count=1) # corner i, position x
                parameters_k[2+2*i] = posx[0]
                posy = fromfile(fileID, dtype="i4", count=1) # corner i, position y
                parameters_k[3+2*i] = posy[0]
                counter = fromfile(fileID, dtype="i4", count=1) # counter
                
        elif ROI_type == "poin":
            
            parameters_k=[None] * 3
            
            parameters_k[0] = ROI_type
            
            numpara = fromfile(fileID, dtype="i4", count=1) # number of parameters, should be 3
            posy = fromfile(fileID, dtype="i4", count=1) #position y
            parameters_k[1]=posy[0]
            posx = fromfile(fileID, dtype="i4", count=1) #position x
            parameters_k[2]=posx[0]
            counter = fromfile(fileID, dtype="i4", count=1) # counter, should be 1
        
        if len(parameters_k) <= 16:
            print(parameters_k,"\n")
        else:
            ROIprint = parameters_k[:16]
            ROIprint.append("...")
            print(ROIprint,"\n")    
        
        parameters_list.append(parameters_k)
            
    fileID.close
    return parameters_list