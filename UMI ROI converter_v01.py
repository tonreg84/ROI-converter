"""
UMI ROI converter
Autor: tonreg, team UMI, CNP-CHUV Lausanne
 
Version 01 - 05.11.2024

This program is used to convert ROI files between "Possum" and "imageJ" formats. Filters out non-elliptic ROIs.

Applies a scaling factor and x-y shift to the ROIs.

!!! Non-elliptic ROIs are filtered out during conversion.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from read_Possum_regions import read_Possum_regions
from writeROI2imageJ import writePossum2imageJzip
from read_imageJ_ROIs import read_imageJ_ROI_ZIP
from writeROI2Possum import writeROI2Possum

class MyApp:
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
        
        # check float, int

        # # You can add logic to process the inputs here
        # messagebox.showinfo("Procedure Started", f"Scaling: {scaling_factor}, X-shift: {x_shift}, Y-shift: {y_shift}")
        
        if self.P2J.get():
            print("Converting Possum format to imageJ format")
            
            try:
                ROIs = read_Possum_regions(self.filename)
            except Exception as e:
                print("Error loading ROI file. Check the format: Possum -> .reg")    
                ROIs = None
            
            if ROIs:
                newROIs = []
                for roi in ROIs:
                    roi_type = roi[0]
                    if roi_type != 'circ':
                        print("The ROI is not an elliptical ROI")
                    else:
                        x = roi[2]
                        y = roi[3]
                        w = roi[5]
                        h = roi[6]
                        
                        roi[2] = round(x*scaling_factor) + x_shift
                        roi[3] = round(y*scaling_factor) + y_shift
                        roi[5] = round(w*scaling_factor)
                        roi[6] = round(h*scaling_factor)
                        
                        newROIs.append(roi)

            writePossum2imageJzip(self.filename+"_Pos2imgJ.zip", newROIs)

        if self.J2P.get():
            print("Converting imageJ format to Possum format")
            
            try:
                ROIs = read_imageJ_ROI_ZIP(self.filename)
            except Exception as e:
                print("Error loading ROI file. Check the format: Possum -> .reg")    
                ROIs = None
            
            if ROIs:
                print(ROIs)
                newROIs = []
                for roi in ROIs:
                    
                        x = roi[0]
                        y = roi[1]
                        w = roi[2]
                        h = roi[3]
                        
                        newx = round(x*scaling_factor) + x_shift
                        newy = round(y*scaling_factor) + y_shift
                        neww = round(w*scaling_factor)
                        newh = round(h*scaling_factor)
                        
                        newROIs.append([newx,newy,neww,newh])
            
                print(newROIs)
                
            writeROI2Possum(newROIs,self.filename+"_imgJ2Pos.reg")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
