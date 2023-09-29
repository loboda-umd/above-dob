#Splitting filtered fires, buffered scares, and regular scars by UID Fire and saving in 3 seperate outfolder
#loop didn't work the first time; however, for the update I only updated 1 year at a time

import arcpy, os
arcpy.env.overwriteOutput = True
direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\'
scar_path = direct + '\\AK_CA_scars\\merged\\proj_clean\\'
buf_path = direct + '\\AK_CA_scars\\merged\\buffer_proj_clean\\'
af_path = direct + '\\ActiveFires\\AF_Scar_Yearly_consecutive_filtered\\'

for year in range(2016, 2017):

    inpath = direct + 'Final\\Output\\'+str(year)+'\\'

    #split by attribute (UID_Fire)
    af_infile = af_path + str(year) + '_FD_AF_v2.shp'
    af_opath = inpath + 'fires_cl_split\\'
    if not os.path.exists(af_opath): os.makedirs(af_opath)

    scar_infile = scar_path + str(year)+ '_NA_FD_proj.shp'
    scar_opath = inpath + 'scar_split\\'
    if not os.path.exists(scar_opath): os.makedirs(scar_opath)

    buf_scar_infile = buf_path + str(year)+ '_NA_FD_proj_buff.shp'
    buf_scar_opath = inpath + 'scar_split_buf\\'
    if not os.path.exists(buf_scar_opath): os.makedirs(buf_scar_opath)

    arcpy.MakeFeatureLayer_management(af_infile, "af_lyr")
    arcpy.SplitByAttributes_analysis("af_lyr", af_opath, 'UID_Fire')

    arcpy.MakeFeatureLayer_management(scar_infile, "scar_lyr")
    arcpy.SplitByAttributes_analysis("scar_lyr", scar_opath, 'UID_Fire')

    arcpy.MakeFeatureLayer_management(buf_scar_infile, "buf_scar_lyr")
    arcpy.SplitByAttributes_analysis("buf_scar_lyr", buf_scar_opath, 'UID_Fire')
