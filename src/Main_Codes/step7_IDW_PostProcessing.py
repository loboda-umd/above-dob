import arcpy, sys, traceback, glob, os, datetime
from arcpy.sa import *

arcpy.env.overwriteOutput = True
direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\'
arcpy.CheckOutExtension("Spatial")

#This code adds additional attrbiutes into each scar's individual IDW output. Otherwise when we merge, we lose the information
#gridcode = JD
#ensure the dates etc are maintained

for year in range (2019, 2020):
    inpath = direct + 'Output\\Round2\\' + str(year) + '\\IDW\\clip\\'
    scars = glob.glob(inpath + 'clip_*.shp')
    med_path = direct + 'Output\\Round2\\to_be_merged\\' + str(year) + "\\clip\\"
    if not os.path.exists(med_path): os.makedirs(med_path)

    for scar in scars:
        fname = scar.split('\\')[-1]
        ffname = fname.split(".")[0]
        name = ffname.split("_")[1]

        #extract UID_Fire from file name
        arcpy.AddField_management(scar, "UID_Fire", "Long")
        arcpy.CalculateField_management(scar, "UID_Fire", name, "PYTHON_9.3")

        #The "gridcode" attribute needs to be changed to Julian Date
        arcpy.AddField_management(scar, "JD", "Long")
        arcpy.CalculateField_management(scar, "JD", "!gridcode!", "PYTHON_9.3")

        arcpy.AddField_management(scar, "Year", "Long")
        arcpy.CalculateField_management(scar, "Year", year, "PYTHON_9.3")

        #to differentiate where the date was calcualted from
        arcpy.AddField_management(scar, "date_src", "Text", "50")
        arcpy.CalculateField_management(scar, "date_src", '"FPM"', "PYTHON_9.3")

        arcpy.Copy_management(scar, med_path + fname)
