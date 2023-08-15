#Selects the AFs within the buffered scars and add the UID_fire to each AF point

import arcpy, glob
arcpy.env.overwriteOutput = True

buff_scars_path = 'D:\\Dropbox\\ABOVE\\Fire_progression\\Version2.0_2016_2019_update\\AK_CA_scars\\merged\\buffer_proj_clean\\'
af_path = 'D:\\ABoVE\\mcd14ml\\monthly_global_reproject_caeac\\'
opath = 'D:\\ABoVE\\mcd14ml\\AF_Scar_Join\\'
for year in range(2016, 2020):
    for month in range(1,13):
      #search for AFs
      af = glob.glob(af_path + str(year)+str(month).zfill(2)+'_global_C3_reproj.shp')

      arcpy.MakeFeatureLayer_management(af[0], "af_lyr")

      #search for buffered scars
      scars = glob.glob(buff_scars_path + str(year)+'_NA_FD_proj_buff.shp')
      arcpy.MakeFeatureLayer_management(scars[0], "scar_lyr")

      outfile = opath + str(year)+str(month).zfill(2)+'_AF_scar.shp'

      #Spatial Join to join UID_Fire to AF point
      arcpy.SpatialJoin_analysis("af_lyr", "scar_lyr", outfile,"JOIN_ONE_TO_MANY","KEEP_COMMON",'',"INTERSECT",'',''  )




