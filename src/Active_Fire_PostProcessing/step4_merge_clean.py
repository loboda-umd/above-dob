import arcpy, glob, os
#merge fires into 1 yearly layer
#clean columns
for year in range(2016, 2020):
    #path for the scars with residual fires
    respath = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\primary_residual\\residuals\\'+ str(year) + "\\"
    #path for primary fires
    primpath =  'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\primary_residual\\'+str(year)+"\\"
    opath = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\primary_residual\\merge\\'+str(year)+"\\"
    if not os.path.exists(opath): os.makedirs(opath)
    #initial merging and cleaning - residuals
    res_fires = glob.glob(respath + '*.shp')
    scarsR = opath + str(year)+'_res.shp'
    arcpy.Merge_management(res_fires, scarsR)


    fieldNames = [f.name for f in arcpy.ListFields(scarsR)]
    subList = fieldNames[2:]
    for s in subList:
        if (s == 'FID_1') or (s == 'UID_1'):
            arcpy.DeleteField_management(scarsR, s)
    del fieldNames, subList, s

    # initial merging - primary (no cleaning needed)
    prim_fires = glob.glob(primpath + '*.shp')
    scarsP = opath + str(year)+'_prim.shp'
    arcpy.Merge_management(prim_fires, scarsP)


    #final merging
    scarsO = opath + str(year)+'_prim_res.shp'
    arcpy.Merge_management([scarsR, scarsP], scarsO)