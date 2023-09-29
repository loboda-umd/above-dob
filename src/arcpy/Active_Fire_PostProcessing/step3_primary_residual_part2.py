import arcpy
import glob
import os
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False

for year in range(2016, 2020):
    #outpath for the scars with residual fires
    outpath = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\primary_residual\\residuals\\'+ str(year) + "\\"
    medpath = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\primary_residual\\medpath\\'+str(year)+"\\"
    if not os.path.exists(outpath): os.makedirs(outpath)

    af_len = len(glob.glob('D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\'+str(year)+'\\scar_split\\' + '*.shp'))
    # print af_len


    for afi in range(1,af_len+1):
        origFire = medpath + str(afi) + '_fires_med_col.shp'
        fires = medpath + str(afi) + '_fires_nodup_med.shp'

        if os.path.isfile(origFire):

            arcpy.CalculateField_management(origFire, "Status", "'primary'", "PYTHON_9.3")

            arcpy.MakeFeatureLayer_management(origFire, "orig")
            arcpy.MakeFeatureLayer_management(fires, "dup")

            arcpy.AddJoin_management("orig", "UID","dup","UID")
            outFeature = outpath + str(afi) + '_fires_med_residuals.shp'

            arcpy.CopyFeatures_management("orig", outFeature)



            fieldNames = [f.name for f in arcpy.ListFields(outFeature)]
            subList = fieldNames[11:]
            for s in subList:
                if (s <> 'UID_1'):
                    arcpy.DeleteField_management(outFeature, s)
            del fieldNames, subList, s

            fields = ["Status", "UID_1"]
            rows = arcpy.UpdateCursor(outFeature)
            for row in rows:
                status = row.Status
                uid = row.UID_1

                if uid == 0:

                    new_status = 'residual'

                else:
                    new_status = 'primary'

                row.setValue("Status", new_status)
                rows.updateRow(row)

            del row
            del rows

