import arcpy

for year in range(2016, 2020):
    file = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Round2\\final_cleaning\\V2\\ABOVE_DOB_'+str(year)+'.shp'
    ofile = 'D:\\Dropbox\\ABOVE\\Fire_progression\\Version2.0_2016_2019_update\\DAAC\\ABoVE_DoB_'+str(year)+'.shp'

    arcpy.CopyFeatures_management(file, ofile)