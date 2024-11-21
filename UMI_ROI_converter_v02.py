"""

UMI ROI converter
Autor: tonreg, team UMI, CNP-CHUV Lausanne
 
Version 02 - 21.11.2024

This program is used to convert ROI files between "Possum" and "imageJ" formats.
File extensions: 
Possum: .reg
imageJ: .roi (single ROI), .zip (multiple ROIs)

A scaling factor and x-y shift can be applied to the ROIs.

!!! Important !!!
When reading imageJ ROIs:

- ROIs of type "Freehand" will be assigned as type "Polygone"

When writing imageJ ROIs:

- Cannot write ROIs of type "line". Dummy "point" ROI is written to file instead to keep ROI numbering.

When converting from imageJ to Possum format:

- Possum does not support "angle" and "line" ROIs.
  Such ROIs will not be written to the "Possum" ROI file

- In imageJ format, several points can be handled as single ROI. 
  This is not the case for Possum, where every point is a ROI.
  Thus the number of ROIs might increase.

- In Possum format, polygone ROIs can have a maximum of 94 corners.
  Polygone ROIs with more then 94 corners will not be written to the file.

"""

import tkinter as tk
from tkinter import filedialog, messagebox
from read_Possum_regions import read_Possum_regions
from writeROI2imageJ import writeROI2imageJ_zip
from read_imageJ_ROI import read_imageJ_ROI
from writeROI2Possum import writeROI2Possum

class ROIconverter:
    def __init__(self, root):
        self.root = root
        self.root.title("ROI converter")
        self.root.geometry("400x400")

        # File selection
        self.browse_button = tk.Button(root, text="Browse ROI File", command=self.browse_file)
        self.browse_button.pack(pady=10)
        
        #conversion options
        self.P2J = tk.BooleanVar(value=False)
        self.checkB_P2J = tk.Checkbutton(root, text="convert Possum format to imageJ format", variable=self.P2J, command=self.update_1)
        self.checkB_P2J.pack(pady=5)
        self.J2P = tk.BooleanVar(value=False)
        self.checkB_J2P = tk.Checkbutton(root, text="convert imageJ format to Possum format", variable=self.J2P, command=self.update_2)
        self.checkB_J2P.pack(pady=5)

        # Scaling factor
        tk.Label(root, text="Scaling factor (float value):").pack(pady=5)
        self.scaling_factor_entry = tk.Entry(root)
        self.scaling_factor_entry.pack(pady=5)
        
        self.scaling_factor_entry.insert(0,"1")

        # X-shift
        tk.Label(root, text="X-shift (in pixel):").pack(pady=5)
        self.x_shift_entry = tk.Entry(root)
        self.x_shift_entry.pack(pady=5)
        
        self.x_shift_entry.insert(0,"0")

        # Y-shift
        tk.Label(root, text="Y-shift (in pixel):").pack(pady=5)
        self.y_shift_entry = tk.Entry(root)
        self.y_shift_entry.pack(pady=5)

        self.y_shift_entry.insert(0,"0")

        # Start button
        self.start_button = tk.Button(root, text="Start ROI conversion", command=self.start_procedure)
        self.start_button.pack(pady=20)
        self.start_button.config(state= "disabled")
        
    #if tik one box, set the other to false
    def update_1(self):
        if self.P2J.get() == True:
            self.J2P.set(False)
        if self.P2J.get() or self.J2P.get():
            if self.filename:
                self.start_button.config(state= "normal")
        else:
            self.start_button.config(state= "disabled")
    def update_2(self):   
        if self.J2P.get() == True:
            self.P2J.set(False)
        if self.P2J.get() or self.J2P.get():
            if self.filename:
                self.start_button.config(state= "normal")
        else:
            self.start_button.config(state= "disabled")
            
            
    def browse_file(self):
        self.filename = None
        self.filename = filedialog.askopenfilename()
        if self.filename:
            print(f"ROI file selected: {self.filename}")
            if self.P2J.get() or self.J2P.get():
                self.start_button.config(state= "normal")
        else:
            print("No file selected")
            self.start_button.config(state= "disabled")

    def start_procedure(self):
        scaling_factor = float(self.scaling_factor_entry.get())
        x_shift = int(self.x_shift_entry.get())
        y_shift = int(self.y_shift_entry.get())
        
        if self.P2J.get():
            print("Converting Possum format to imageJ format","\n")
            
            try:
                ROI_list = read_Possum_regions(self.filename)
            except Exception as e:
                messagebox.showerror("Error", r'Error loading Possum regions file. Check the file format -> ".reg"')  
                print("Error loading the file. Check the file format!","\n")
                ROI_list = None
            
            print("Converting regions, applying scaling and shift...","\n")
            
            if ROI_list:
                new_ROI_list = []
                for ROI in ROI_list:
                    ROI_type = ROI[0]
                    newROI = []
                    
                    if ROI_type == 'circ':
                        newROI.append("oval")
                        newROI.append(round(ROI[1]*scaling_factor) + x_shift)
                        newROI.append(round(ROI[2]*scaling_factor) + y_shift)
                        newROI.append(round(ROI[3]*scaling_factor))
                        newROI.append(round(ROI[4]*scaling_factor))
                        
                    if ROI_type == 'rect':
                        newROI.append("rectangle")
                        newROI.append(round(ROI[1]*scaling_factor) + x_shift)
                        newROI.append(round(ROI[2]*scaling_factor) + y_shift)
                        newROI.append(round(ROI[3]*scaling_factor))
                        newROI.append(round(ROI[4]*scaling_factor))
                        
                    if ROI_type == 'poly':
                        newROI.append("polygon")
                        newROI.append(ROI[1])
                        
                        for i in range(ROI[1]):
                            newROI.append(round(ROI[2+2*i]*scaling_factor) + x_shift)
                            newROI.append(round(ROI[3+2*i]*scaling_factor) + y_shift)
                    
                    if ROI_type == 'poin':
                        newROI.append("point")
                        newROI.append(1)
                        newROI.append(round(ROI[2]*scaling_factor) + y_shift)  # !!!!!!!!!! here x and y are transmuted
                        newROI.append(round(ROI[1]*scaling_factor) + x_shift)  # !!!!!!!!!! here x and y are transmuted
                    
                    new_ROI_list.append(newROI)
                
                writeROI2imageJ_zip(new_ROI_list, self.filename+"_Pos2imgJ.zip")

        if self.J2P.get():
            print("Converting imageJ format to Possum format","\n")
            
            try:
                ROI_list = read_imageJ_ROI(self.filename)
            except Exception as e:
                messagebox.showerror("Error", r'Error loading imageJ regions file. The file may be corrupted.',"\n")
                print("Error loading the file. Check the file format!","\n")
                ROI_list = None
            
            print("Converting regions, applying scaling and shift...","\n")
            
            if ROI_list:
                
                new_ROI_list = []
                
                counter = 1
                for ROI in ROI_list:
                    ROI_type = ROI[0]
                    newROI = []
                    
                    if ROI_type == 'oval':
                        newROI.append("circ")
                        newROI.append(round(ROI[1]*scaling_factor) + x_shift)
                        newROI.append(round(ROI[2]*scaling_factor) + y_shift)
                        newROI.append(round(ROI[3]*scaling_factor))
                        newROI.append(round(ROI[4]*scaling_factor))
                        
                        new_ROI_list.append(newROI)
                        
                    if ROI_type == 'rectangle':
                        newROI.append("rect")
                        newROI.append(round(ROI[1]*scaling_factor) + x_shift)
                        newROI.append(round(ROI[2]*scaling_factor) + y_shift)
                        newROI.append(round(ROI[3]*scaling_factor))
                        newROI.append(round(ROI[4]*scaling_factor))
                        
                        new_ROI_list.append(newROI)
                        
                    if ROI_type == 'polygon':
                        
                        if ROI[1] > 94:
                            messagebox.showinfo("Attention!", f'ROI #{counter} is a polygone ROI with more than 94 corners. Cannot be writen to Possum regions file.')
                            print(f'ROI #{counter} not written to Possum regions file, as it has more than 94 corners.',"\n")
                        else:
                            newROI.append("poly")
                            newROI.append(ROI[1])
                            
                            for i in range(ROI[1]):
                                newROI.append(round(ROI[2+2*i]*scaling_factor) + x_shift)
                                newROI.append(round(ROI[3+2*i]*scaling_factor) + y_shift)
                                
                            new_ROI_list.append(newROI)
                    
                    if ROI_type == 'point':
                        
                        for i in range(ROI[1]):
                            newROI = []
                            newROI.append("poin")
                            newROI.append(round(ROI[3+i*2]*scaling_factor) + y_shift)   # !!!!!!!!!! here x and y are transmuted
                            newROI.append(round(ROI[2+i*2]*scaling_factor) + x_shift)   # !!!!!!!!!! here x and y are transmuted
                            new_ROI_list.append(newROI)
                            
                    if ROI_type == 'line':   
                        messagebox.showinfo("Attention!", f'ROI #{counter} is a line ROI. Cannot be writen to Possum regions file.')
                        print(f'ROI #{counter} not written to Possum regions file, as it is of type "line".',"\n")
                        
                    if ROI_type == 'angle':   
                        messagebox.showinfo("Attention!", f'ROI #{counter} is an angle ROI. Cannot be writen to Possum regions file.')
                        print(f'ROI #{counter} not written to Possum regions file, as it is of type "angle".',"\n")
                        
                    counter = counter+1        
                    
                writeROI2Possum(new_ROI_list,self.filename+"_imgJ2Pos.reg")

if __name__ == "__main__":
    root = tk.Tk()
    app = ROIconverter(root)
    root.mainloop()
