#merge each folder seperately
#I uncommented out each one one by one and ran the merge.
#I can't remember if I only had to run some of these or if I had to run each one

#merge the shapefiles
import arcpy, glob, os

arcpy.env.overwriteOutput = True
#merge

direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Round2\\'

for year in range (2019, 2020):
    opath = direct + "merged\\" + str(year) + '\\'
    if not os.path.exists(opath): os.makedirs(opath)

    ## FPM (IDW) outputs
    path = direct + "to_be_merged\\" + str(year) + '\\clip\\'
    oname = str(year) + "_FPM.shp"

    ## Scars without dates or Active Fires (no FD Date Error - step 11 code)
    #path = direct + "no_FD_date_error\\" + str(year) + '\\'
    #path =  direct + "to_be_merged\\" + str(year) + '\\NoDate_NA\\' # I copied the shapefiles into the "to_be_merged" folder
    #oname = str(year) + "_NA.shp"


    # Scars with date from FD because there were no Active Fires points
    # path = direct  + str(year) + '\\IDW_error\\no_af\\'
    #path = direct + "to_be_merged\\" + str(year) + '\\NoAF_FD\\'  # I copied the shapefiles into the "to_be_merged" folder
    #oname = str(year) + "_FD.shp"

    # Scars with 1 AF point
    # path = direct  + str(year) + '\\IDW_error\\other\\'
    #path = direct + "to_be_merged\\" + str(year) + '\\1AF\\'  # I copied the shapefiles into the "to_be_merged" folder
    #oname = str(year) + "_1AF.shp"

######## These are optional as they may not occur each year

    ## If you had scars that were straddling the AK/CA boundary and were manually dissolved and an IDW run seperately
    # path = direct + "to_be_merged\\" + str(year) + '\\boundary\\'
    # oname = str(year) + "_boundary.shp"

    # code error no af
    # path = direct + "to_be_merged\\" + str(year) + '\\code_error\\no_af\\'
    # oname = str(year) + "_code_err_no_af.shp"

    # For any scars manually checked and attributes changed to appropriate codes (IDW polygon error)
    # path = direct + "to_be_merged\\" + str(year) + '\\IDW_error\\'
    # oname = str(year) + "_code_err_idw.shp"



    scars = glob.glob(path + '*.shp')
    scarsM = opath + oname
    arcpy.Merge_management(scars,scarsM)
