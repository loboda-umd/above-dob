#resplit the AFs that have been filtered after the first IDW filtering

import arcpy, os
arcpy.env.overwriteOutput = True
direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\'
af_path = direct + '\\ActiveFires\\AF_Yearly_IDW_filtered\\'

for year in range(2019, 2020):

    inpath = direct + 'Output\\Round2\\'+str(year)+'\\'

    #split by attribute (UID_Fire)
    af_infile = af_path + str(year) + '_FD_AF_v3.shp'
    af_opath = inpath + 'fires_cl_split\\'
    if not os.path.exists(af_opath): os.makedirs(af_opath)

    arcpy.MakeFeatureLayer_management(af_infile, "af_lyr")
    arcpy.SplitByAttributes_analysis("af_lyr", af_opath, 'UID_Fire')

