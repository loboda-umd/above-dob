import arcpy
import glob
import os
arcpy.env.overwriteOutput = True
outpath = 'F:\\Fire_progression_modelling\\MCD14ML_FPM\\final\\add_column\\'


for year in range(2016, 2020):
    inpath = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Round2\\'+str(year)+'\\fires_cl_split_medpath\\'
    outpath = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\primary_residual\\'+str(year)+"\\"
    medpath = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\primary_residual\\medpath\\'+str(year)+"\\"
    if not os.path.exists(outpath): os.makedirs(outpath)
    if not os.path.exists(medpath): os.makedirs(medpath)

    #Making sure we loop through each scar
    af_len = len(glob.glob('D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\'+str(year)+'\\scar_split\\' + '*.shp'))
    #print af_len

    for afi in range(1,af_len+1):

        origFire = inpath + str(afi) + '_fires.shp'
        fires = inpath + str(afi) + '_fires_nodup.shp'

        if os.path.isfile(origFire):

            #if duplicate and original have same number of rows then no duplicate will be copied and assigned primary

            orig_num = arcpy.GetCount_management(origFire)
            orig_count = int(orig_num.getOutput(0))


            dup_num = arcpy.GetCount_management(fires)
            dup_count = int(dup_num.getOutput(0))
           # print(afi, orig_count, dup_count)


            if orig_count == dup_count:

                outdup = outpath + str(afi) + '_fires_nodup_col.shp'
                arcpy.CopyFeatures_management(fires, outdup)
                arcpy.AddField_management(outdup, "Status", "Text", 20)
                arcpy.CalculateField_management(outdup, "Status", "'primary'", "PYTHON_9.3")

            #if they are not equal then they will be copied to an intermediate location for further analysis

            if orig_count <> dup_count:
                #print(year, afi, orig_count, dup_count)
                meddup = medpath + str(afi) + '_fires_nodup_med.shp'
                arcpy.CopyFeatures_management(fires, meddup)
                arcpy.AddField_management(meddup, "Status", "Text", 20)

                medorig = medpath + str(afi) + '_fires_med_col.shp'
                arcpy.Copy_management(origFire, medorig)
                arcpy.AddField_management(medorig, "Status", "Text", 20)

                #The code assigns these fires as primary to begin with and only overwrites the ones that are residual in the next code
                arcpy.CalculateField_management(meddup, "Status", "'primary'", "PYTHON_9.3")

        else:
            continue


