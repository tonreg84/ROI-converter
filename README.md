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
