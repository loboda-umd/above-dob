#this script changes the attributes within the date error shapefiles

import glob, os, arcpy
arcpy.env.overwriteOutput = True
direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Round2\\'

for year in range(2019, 2020):

    inpath = direct + "no_FD_date_error\\"+ str(year) + '\\'
    no_fd_scars = glob.glob(inpath + '*.shp')

    for no_fd_scar in no_fd_scars:
        fname = no_fd_scar.split('\\')[-1]
        ffname = fname.split(".")[0]
        print ffname

        fieldNames = [f.name for f in arcpy.ListFields(no_fd_scar)]
        subList = fieldNames[2:]

        for s in subList:
            if (s == 'date_src'):
                arcpy.DeleteField_management(no_fd_scar, s)
        del fieldNames, subList, s

        arcpy.AddField_management(no_fd_scar, "date_src", "Text", "50")
        arcpy.CalculateField_management(no_fd_scar, "date_src", '"NA"', "PYTHON_9.3")