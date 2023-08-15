import arcpy

for year in range(2016, 2020):
    file = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\join\\'+str(year) + '_FD_AF_join.shp'

    fields = ["Status", "TARGET_F_1"]
    rows = arcpy.UpdateCursor(file)
    for row in rows:
        status = row.Status
        uid = row.TARGET_F_1

        if uid == 0:

            new_status = 'removed'


            row.setValue("Status", new_status)
            rows.updateRow(row)

    del row
    del rows