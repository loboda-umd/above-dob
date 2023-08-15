
import arcpy

#Read in original Active Fire shapefile, clean, and rename to '_orig.shp"

orig_path = 'D:\\Dropbox\\ABOVE\\Fire_progression\\Version2.0_2016_2019_update\\ActiveFires\\AF_Scar_Yearly_Base_Layer\\'
orig_opath = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\orig\\'

for year in range(2016, 2020):

    orig_infile = orig_path + str(year)+'_FD_AF.shp'
    orig_ofile = orig_opath + str(year)+'_FD_AF_orig.shp'
    arcpy.CopyFeatures_management(orig_infile, orig_ofile)

    fieldNames = [f.name for f in arcpy.ListFields(orig_ofile)]
    subList = fieldNames[2:]
    for s in subList:
        if (s == 'Join_Count') or (s == 'JOIN_FID') or (s == 'BUFF_DIST') or (s == 'PERIMETERD') or (s == 'REP_DATE'):
            arcpy.DeleteField_management(orig_ofile, s)
    del fieldNames, subList, s






