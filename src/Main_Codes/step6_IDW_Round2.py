
import arcpy, sys, traceback, glob, os
import numpy as np
from arcpy.sa import *

arcpy.env.overwriteOutput = True

arcpy.CheckOutExtension("Spatial")
direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\'

for year in range (2019, 2020):

    #paths
    #Round 1 path
    orig_path = direct + 'Output\\' + str(year) + '\\'
    #Round 2 path
    path = direct + 'Output\\Round2\\' + str(year) + '\\'
    outpath = path  + 'IDW\\'
    if not os.path.exists(outpath): os.makedirs(outpath)
    outpath_clip = outpath + "clip\\"
    if not os.path.exists(outpath_clip): os.makedirs(outpath_clip)
    outpath_polygon = outpath + "polygon_error\\"
    if not os.path.exists(outpath_polygon): os.makedirs(outpath_polygon)

    #searching for split scars

    scars_len = len(glob.glob(orig_path + 'scar_split\\*.shp'))

    for i in range(1,scars_len+1):

        print 'this is i ' +str(i)

        scar = orig_path + 'scar_split\\' + str(i)+'.shp'
        clean = path + 'fires_cl_split_medpath\\' + str(i) + '_fires_nodup.shp'
        if os.path.exists(clean) and os.path.exists(scar):

            rows = [row for row in arcpy.da.SearchCursor(clean, "FID")]
            count = len(rows)

            if count > 1:

                # create extent for each individual scar
                arcpy.env.extent = scar

                #set up environment to extent of scar

                outfile1 = outpath+'IDW_'+str(i)+'_'+str(year)+'.tif'
                outsurf = Idw(clean, "JD", 30,2)
                outsurf.save(outfile1)

                outsurfplus = arcpy.sa.Plus(outsurf, 0.5)
                outsurfint = arcpy.sa.Int(outsurfplus)
                outsurfint.save(outpath+'IDW_'+str(i)+'_'+str(year)+'.tif')


                #print 'Finished interpolation of fire progression using IDW for '+str(i)+'fires\n'

                #test if raster is empty
                ras = outpath+'IDW_'+str(i)+'_'+str(year)+'.tif'
                array = arcpy.RasterToNumPyArray(ras)
                if np.max(array) > 0:

                    #Raster to Vector
                    outvec = arcpy.RasterToPolygon_conversion(outsurfint,outpath+'poly_'+str(i)+'_'+str(year)+'.shp', "NO_SIMPLIFY")
                    clip_out = arcpy.Clip_analysis(outvec,scar,outpath_clip+'clip_'+str(i)+'_'+str(year)+'.shp')
                else:
                    print 'polygon error: '+'IDW_'+str(i)+'_'+str(year)+'.tif'
                    arcpy.Copy_management(ras, outpath_polygon + 'IDW_'+str(i)+'_'+str(year)+'.tif')
            else:
                pass

        else:
            pass

