#clip to CA_AK and reproject and merge and reproject
import arcpy, os


path = 'D:\\ABoVE\\mcd14ml\\monthly_global_reproject_caeac\\'
opath = 'D:\\ABoVE\\mcd14ml\\AK_CA_monthly\\'

AK_CA_shapefile = 'D:\\Dropbox\\ABOVE\\USA_Canada_shapefile\\ak_canada_CAEAC.shp'

for year in range(2016, 2020):
    for month in range(1, 13):
        infile = path + os.sep +  str(year) + str(month).zfill(2) + '_global_C3_reproj.shp'
        ofile = opath + os.sep + str(year) + str(month).zfill(2) + "_mcd_c3_af.shp"

        arcpy.Clip_analysis(infile, AK_CA_shapefile, ofile, "")







