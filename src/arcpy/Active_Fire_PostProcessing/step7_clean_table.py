import arcpy
outpath = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\final\\'

for year in range(2016, 2020):
    file = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\join\\'+str(year) + '_FD_AF_join.shp'

    fieldNames = [f.name for f in arcpy.ListFields(file)]
    subList = fieldNames[2:]
    for s in subList:
        if (s == 'ORIG_FID') or (s == "YYYYMMDD_1") or (s == "HHMM_1") or (s == "UID_Fire_1")or (s == "JD_UTC")or (s == "JD")or (s == "Time_d")or (s == "UID")or (s == "TARGET_F_1")\
                or (s == "TARGET_FID"):
            arcpy.DeleteField_management(file, s)
    del fieldNames, subList, s

    #Rename the file
    ofile = outpath + 'ABoVE_DoB_MODIS_Active_Fires_' + str(year) + '.shp'
    arcpy.CopyFeatures_management(file, ofile)









