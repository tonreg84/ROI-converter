def read_Possum_regions(regions_file):
    #reads a Possum regions file
    from numpy import fromfile
    
    #read regions
    fileID = open(regions_file, 'rb')
    nREG = fromfile(fileID, dtype="i4", count=1)
    nREG=nREG[0]
    parameters_list=[]
    for k in range(nREG):
        parameters_k=[None] * 100
        bstring=fileID.read(4)
        parameters_k[0]=bstring.decode('utf-8')
        if parameters_k[0] == "circ":
            numpara = fromfile(fileID, dtype="i4", count=1) # number of parameters, should be 2
            parameters_k[1]=numpara[0]
            posx = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position x
            parameters_k[2]=posx[0]
            posy = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position y
            parameters_k[3]=posy[0]
            what = fromfile(fileID, dtype="i4", count=1) # param counter,should be 0
            parameters_k[4]=what[0]
            dimx = fromfile(fileID, dtype="i4", count=1) # dimension x
            parameters_k[5]=dimx[0]
            dimy = fromfile(fileID, dtype="i4", count=1) # dimension y
            parameters_k[6]=dimy[0]
            count = fromfile(fileID, dtype="i4", count=1) # param counter, should be 1
            parameters_k[7]=count[0]
            
        elif parameters_k[0] == "rect":
            numpara = fromfile(fileID, dtype="i4", count=1) # number of parameters, should be 2
            parameters_k[1]=numpara[0]
            posx = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position x
            parameters_k[2]=posx[0]
            posy = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position y
            parameters_k[3]=posy[0]
            what = fromfile(fileID, dtype="i4", count=1) # param counter,should be 0
            parameters_k[4]=what[0]
            dimx = fromfile(fileID, dtype="i4", count=1) # dimension x
            parameters_k[5]=dimx[0]
            dimy = fromfile(fileID, dtype="i4", count=1) # dimension y
            parameters_k[6]=dimy[0]
            count = fromfile(fileID, dtype="i4", count=1) # param counter, should be 1
            parameters_k[7]=count[0]
            
        elif parameters_k[0] == "poly":
            numpara = fromfile(fileID, dtype="i4", count=1) # number of points of the polygone
            parameters_k[1]=numpara[0]
            for i in range(parameters_k[1]):
                posx = fromfile(fileID, dtype="i4", count=1) # point i, position x
                parameters_k[1+3*i+1] = posx[0]
                posy = fromfile(fileID, dtype="i4", count=1) # point i, position y
                parameters_k[1+3*i+2] = posy[0]
                counter = fromfile(fileID, dtype="i4", count=1) # counter
                parameters_k[1+3*i+3] = counter[0]
        elif parameters_k[0] == "poin":
            numpara = fromfile(fileID, dtype="i4", count=1) # number of parameters, should be 3
            parameters_k[1]=numpara[0]
            posy = fromfile(fileID, dtype="i4", count=1) #position y
            parameters_k[2]=posx[0]
            posx = fromfile(fileID, dtype="i4", count=1) #position x
            parameters_k[3]=posy[0]
            counter = fromfile(fileID, dtype="i4", count=1) # counter, should be 1
            parameters_k[4]=counter[0]
            
        parameters_list.append(parameters_k)
            
    fileID.close
    return parameters_list
    

def read_Possum_regions_elliptic(regions_file):
    #reads a Possum regions file
    #selects only ellyptic regions and gives out a list of region parameter tuples (posx,posy,Lx,Ly)
    #give out a boolean: "True" if only elliptic regions, else "False"
    from numpy import fromfile
    
    ellips_ROI_list=[]
    ellips_only = True
    
    #read regions
    fileID = open(regions_file, 'rb')
    nREG = fromfile(fileID, dtype="i4", count=1)
    nREG=nREG[0]
    parameters_list=[]
    for k in range(nREG):
        parameters_k=[None] * 100
        bstring=fileID.read(4)
        parameters_k[0]=bstring.decode('utf-8')
        if parameters_k[0] == "circ":
            numpara = fromfile(fileID, dtype="i4", count=1) # number of parameters, should be 2
            parameters_k[1]=numpara[0]
            posx = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position x
            parameters_k[2]=posx[0]
            posy = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position y
            parameters_k[3]=posy[0]
            what = fromfile(fileID, dtype="i4", count=1) # param counter,should be 0
            parameters_k[4]=what[0]
            dimx = fromfile(fileID, dtype="i4", count=1) # dimension x
            parameters_k[5]=dimx[0]
            dimy = fromfile(fileID, dtype="i4", count=1) # dimension y
            parameters_k[6]=dimy[0]
            count = fromfile(fileID, dtype="i4", count=1) # param counter, should be 1
            parameters_k[7]=count[0]
            
            circparas=[posx,posy,dimx,dimy]
            ellips_ROI_list.append(circparas)
            
        elif parameters_k[0] == "rect":
            numpara = fromfile(fileID, dtype="i4", count=1) # number of parameters, should be 2
            parameters_k[1]=numpara[0]
            posx = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position x
            parameters_k[2]=posx[0]
            posy = fromfile(fileID, dtype="i4", count=1) # parameter 1: min position y
            parameters_k[3]=posy[0]
            what = fromfile(fileID, dtype="i4", count=1) # param counter,should be 0
            parameters_k[4]=what[0]
            dimx = fromfile(fileID, dtype="i4", count=1) # dimension x
            parameters_k[5]=dimx[0]
            dimy = fromfile(fileID, dtype="i4", count=1) # dimension y
            parameters_k[6]=dimy[0]
            count = fromfile(fileID, dtype="i4", count=1) # param counter, should be 1
            parameters_k[7]=count[0]
            
            ellips_only = False
            
        elif parameters_k[0] == "poly":
            numpara = fromfile(fileID, dtype="i4", count=1) # number of points of the polygone
            parameters_k[1]=numpara[0]
            for i in range(parameters_k[1]):
                posx = fromfile(fileID, dtype="i4", count=1) # point i, position x
                parameters_k[1+3*i+1] = posx[0]
                posy = fromfile(fileID, dtype="i4", count=1) # point i, position y
                parameters_k[1+3*i+2] = posy[0]
                counter = fromfile(fileID, dtype="i4", count=1) # counter
                parameters_k[1+3*i+3] = counter[0]
                
            ellips_only = False
             
        elif parameters_k[0] == "poin":
            numpara = fromfile(fileID, dtype="i4", count=1) # number of parameters, should be 3
            parameters_k[1]=numpara[0]
            posy = fromfile(fileID, dtype="i4", count=1) #position y
            parameters_k[2]=posx[0]
            posx = fromfile(fileID, dtype="i4", count=1) #position x
            parameters_k[3]=posy[0]
            counter = fromfile(fileID, dtype="i4", count=1) # counter, should be 1
            parameters_k[4]=counter[0]
            
            ellips_only = False
            
        parameters_list.append(parameters_k)
            
    fileID.close
    return ellips_ROI_list, ellips_only
    
