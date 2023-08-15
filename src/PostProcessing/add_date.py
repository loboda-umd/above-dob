import glob, arcpy, os, datetime
#paths
direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Round2\\final_cleaning\\V2\\'

for year in range(2016, 2020):
    scars = direct + 'ABOVE_DOB_' + str(year) + '.shp'

    arcpy.AddField_management(scars, 'Map_Date', "String", 15)
    #I manually did this during clean up
    #arcpy.DeleteField_management(scars, 'DiscDate')
    #arcpy.DeleteField_management(scars, 'REP_DATE')


    fields = ["JD", "Map_Date"]
    rows = arcpy.UpdateCursor(scars)
    for row in rows:
        jd = row.JD
        map_date = row.Map_Date

        if jd == 0:

            new_date = '0000-00-00'

        else:


            file_date = datetime.datetime(year, 1, 1) + datetime.timedelta(jd-1)
            new_date = file_date.strftime('%Y-%m-%d')

        row.setValue("Map_Date", new_date)
        rows.updateRow(row)



    del row
    del rows
    print "finished year " + str(year)