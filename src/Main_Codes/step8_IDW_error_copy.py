#This code is copying the scars which either had 1 af or no af into seperate folders for additional processing

import arcpy, glob, os

arcpy.env.overwriteOutput = True
direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\'

arcpy.CheckOutExtension("Spatial")

for year in range(2019, 2020):
    inpath = direct + 'Output\\Round2\\' + str(year)
    scar_path = direct + 'Output\\' + str(year)

    scars_len = len(glob.glob(scar_path +'\\scar_split\\*.shp'))

    err_path = inpath + '\\IDW_error\\'
    if not os.path.exists(err_path): os.makedirs(err_path)

    err_path_af = err_path + 'other\\'
    if not os.path.exists(err_path_af): os.makedirs(err_path_af)

    err_path_no_af = err_path + 'no_af\\'
    if not os.path.exists(err_path_no_af): os.makedirs(err_path_no_af)

    for i in range(1, scars_len + 1):

        #print 'this is i ' + str(i)
        outpath = inpath + '\\IDW\\'
        outpath_clip = outpath + "clip\\"

        scar = scar_path +'\\scar_split\\' + str(i) + '.shp'
        clean = inpath + '\\fires_cl_split_medpath\\' + str(i) + '_fires_nodup.shp'
        name = scar.split("\\")[-1]

        if os.path.exists(scar):
            if os.path.exists(clean):

                rows = [row for row in arcpy.da.SearchCursor(clean, "FID")]
                count = len(rows)
                #print count

                if count > 1:
                    pass

                if count == 1:
                    #1 AF
                    arcpy.Copy_management(scar, err_path_af + name)
                    pass

                if count == 0:
                    import pdb
                    pdb.set_trace()

            else:

                #if no af
                arcpy.Copy_management(scar, err_path_no_af + name)
                pass
        else:
            pass

