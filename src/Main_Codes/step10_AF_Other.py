#This code deals with the scars with 1 AF and therefore the IDW cannot be performed


import glob,  os, datetime, arcpy
arcpy.env.overwriteOutput = True
#paths
direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\'
dropbox = 'D:\\Dropbox\\ABOVE\\Fire_progression\\Version2.0_2016_2019_update\\scar_date_tables\\'

for year in range(2019, 2020):
    path = direct + 'Output\\Round2\\' + str(year) + '\\IDW_error\\'
    path_af = path + 'other\\'
    err_path = path_af + "error\\"
    if not os.path.exists(err_path): os.makedirs(err_path)

    ########### Scars with one AF
    no_af_scars = glob.glob(path_af + '*.shp')

    for af_scar in no_af_scars:
        fname = af_scar.split('\\')[-1]
        ffname = fname.split(".")[0]
        print fname


        #First check it doesn't already exist in clip folder
        correct_file = direct + str(year)+"\\IDW\\clip\\clip_"+ffname+"_"+str(year)+".shp"

        if os.path.isfile(correct_file):
            print 'problem 1 '
            import pdb
            pdb.set_trace()

        else:

            #check if AF is within boundary

            #open buffer scar
            buf_scar = direct + "Output\\" + str(year) + "\\scar_split_buf\\"+str(fname)
            if not os.path.isfile(buf_scar):
                print 'problem 2 '
                import pdb
                pdb.set_trace()

            else:

                #open AF

                af_file = direct +'Output\\Round2\\' + str(year) + '\\fires_cl_split_medpath\\' + str(ffname) + '_fires_nodup.shp'

                if not os.path.isfile(buf_scar):
                    print 'problem 3 '
                    import pdb
                    pdb.set_trace()

                else:
                    #if there is 1 Active Fire


                    # Make feature layer of feature classes to allow selection
                    arcpy.MakeFeatureLayer_management(af_file, "af_lyr")
                    arcpy.MakeFeatureLayer_management(buf_scar, "buf_lyr")

                    arcpy.SelectLayerByLocation_management("af_lyr", "INTERSECT", "buf_lyr","","NEW_SELECTION")
                    count = int(arcpy.GetCount_management("af_lyr").getOutput(0))


                    #AF and Buffered scar intersect so extract date from AF JD value

                    if arcpy.Describe("af_lyr").FIDSet:
                        print ' selection'
                        r, rows = None, None
                        # iterate through polygons with cursor
                        cursor = arcpy.SearchCursor("af_lyr")
                        for row in cursor:
                            AF_JD = row.getValue("JD")

                        #extract UID_Fire from file name
                        arcpy.AddField_management(af_scar, "UID_Fire", "Long")
                        arcpy.CalculateField_management(af_scar, "UID_Fire", ffname, "PYTHON_9.3")

                        #to differentiate where the date was calcualted from
                        arcpy.AddField_management(af_scar, "date_src", "Text", "50")
                        arcpy.CalculateField_management(af_scar, "date_src", '"1AF"', "PYTHON_9.3")

                        arcpy.AddField_management(af_scar, "Year", "Long")
                        arcpy.CalculateField_management(af_scar, "Year", year, "PYTHON_9.3")

                        arcpy.AddField_management(af_scar, "JD", "Long")
                        arcpy.CalculateField_management(af_scar, "JD", AF_JD, "PYTHON_9.3")

                        r, rows = None, None
                        arcpy.Delete_management("af_lyr")
                        arcpy.Delete_management("buf_lyr")


                # AF and Buffered scar DID NOT intersect so move to another folder for extraction from FD
                    else:

                        arcpy.Copy_management(af_scar, err_path + ffname)
                        arcpy.Delete_management(af_scar)

