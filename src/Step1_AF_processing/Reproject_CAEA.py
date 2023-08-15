import arcpy, os
#Reproject global active fires into CAEA projection

path = 'D:\\mcd14ml\\c6_v3\\xy_layer\\'
opath = 'D:\\ABoVE\\mcd14ml\\monthly_global_reproject_caeac\\'


ABoVE_coord = "PROJCS['Canada_Albers_Equal_Area_Conic',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983'," \
              "SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]," \
              "PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0]," \
              "PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',50.0]," \
              "PARAMETER['Standard_Parallel_2',70.0],PARAMETER['Latitude_Of_Origin',40.0],UNIT['Meter',1.0]]"
#need to run 2012 month 6
for year in range (2016, 2020):
    for month in range(1, 13):

        infile = path + os.sep + str(year) + str(month).zfill(2) + '_global_C3.shp'
        outname = opath + os.sep +  str(year) + str(month).zfill(2) + '_global_C3_reproj.shp'



        # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
        # The following inputs are layers or table views: "ABBA_2001_NA"
        arcpy.Project_management(in_dataset = infile,
                                 out_dataset = outname,
                                 out_coor_system = ABoVE_coord)

