#Read in join AF scar shapefile
import arcpy
import csv
arcpy.env.overwriteOutput = True
for year in range(2016, 2020):

    file = 'D:\\ABoVE\\mcd14ml\\AF_Scar_Yearly\\' + str(year) + '_FD_AF.shp'
    opath = 'D:\\Dropbox\\ABOVE\\Fire_progression\\Version2.0_2016_2019_update\\consecutive_testing\\yearly\\'

    fname = file.split('\\')[-1]
    ffname = fname.split(".")[0]
    print ffname
    output = opath + ffname + '.csv'

    fields = arcpy.ListFields(file)
    field_names = [field.name for field in fields]

    with open(output, 'w') as f:
        w = csv.writer(f)
        w.writerow(field_names)
        with arcpy.da.SearchCursor(file, field_names) as cursor:
            for row in cursor:
                w.writerow(row)