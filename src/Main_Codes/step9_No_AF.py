#This code deals with the scars with either no AF  and therefore the IDW cannot be performed
#For no AF, we will use the date from the Fire Database
#If there is no date then the shapefile is copied into another folder for further work

#need to check that it is not in the clip folder

import glob, arcpy, os, datetime
import os.path
#paths
direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\'
dropbox = 'D:\\Dropbox\\ABOVE\\Fire_progression\\Version2.0_2016_2019_update\\scar_date_tables\\'

for year in range(2019, 2020):
    path = direct + 'Output\\Round2\\' + str(year)+ '\\IDW_error\\'

    path_no_af = path + 'no_af\\'
    err_path = path_no_af + "error\\"
    if not os.path.exists(err_path): os.makedirs(err_path)

    yfile = open(dropbox  + str(year)+".csv", 'r')
    ydata = yfile.read()
    yfile.close()

    ylist = ydata.split('\n')
    yheader = ylist[0]
    ufIndex = (yheader.split(',')).index(str("UID_Fire"))
    monthIndex = (yheader.split(',')).index(str("MONTH"))
    dayIndex = (yheader.split(',')).index(str("DAY"))

    ########### Scars with no AF
    no_af_scars = glob.glob(path_no_af + '*.shp')

    for no_af_scar in no_af_scars:
        fname = no_af_scar.split('\\')[-1]
        ffname = fname.split(".")[0]
        print ffname


        #First check it doesn't already exist in clip folder
        correct_file = direct + str(year)+"\\IDW\\clip\\clip_"+ffname+"_"+str(year)+".shp"

        if os.path.isfile(correct_file):
            print 'problem'
            import pdb
            pdb.set_trace()

        else:


            #extract UID_Fire from file name
            arcpy.AddField_management(no_af_scar, "UID_Fire", "Long")
            arcpy.CalculateField_management(no_af_scar, "UID_Fire", ffname, "PYTHON_9.3")

            #to differentiate where the date was calcualted from
            arcpy.AddField_management(no_af_scar, "date_src", "Text", "50")
            arcpy.CalculateField_management(no_af_scar, "date_src", '"FD"', "PYTHON_9.3")

            arcpy.AddField_management(no_af_scar, "Year", "Long")
            arcpy.CalculateField_management(no_af_scar, "Year", year, "PYTHON_9.3")

            arcpy.AddField_management(no_af_scar, "JD", "Long")

            #To calculate JD we need to extract date from the FD table and convert to JD

            for line in ylist[1:]:

                UID_FIRE = line.split(',')[ufIndex]
                #print UID_FIRE

                if UID_FIRE == ffname:
                    day = line.split(',')[dayIndex]
                    month = line.split(',')[monthIndex]


                    if day == '0' and month == '0':

                        arcpy.Copy_management(no_af_scar, err_path + ffname)
                        arcpy.Delete_management(no_af_scar)


                    else:

                        # need to convert to JD from calendar date
                       # print ffname, month, day
                        day_of_year = datetime.date(year, int(month), int(day)).timetuple().tm_yday
                        arcpy.CalculateField_management(no_af_scar, "JD", day_of_year, "PYTHON_9.3")


                else:
                    pass