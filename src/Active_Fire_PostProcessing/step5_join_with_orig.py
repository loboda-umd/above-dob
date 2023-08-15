#join the primary and residual merged file with only a few columns to the original
# manually change null to removed that way I can make sure the join is correct

#######THIS TAKES WAY TOO LONG
import arcpy

for year in range(2017,2020):
    print(year)
    #this would be the real path but due to a code error, I manually joined the target_fid back to toe primary residual fires in ArcGIS
    #prim_res_path = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\primary_residual\\merge\\'+str(year)+"\\"

    prim_res_path ='D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\spatial_join\\prim_res_join\\'+str(year)+"\\"
    orig_path = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\orig\\'
    outpath = "D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Active_Fires\\join\\"

    merge_file = prim_res_path + str(year)+'_prim_res.shp'
    orig_file = orig_path + str(year) + '_FD_AF_orig.shp'
    out_file = outpath + str(year) + '_FD_AF_join.shp'

    arcpy.JoinField_management(orig_file, "TARGET_FID", merge_file, "TARGET_FID")
    arcpy.CopyFeatures_management(orig_file, out_file)



