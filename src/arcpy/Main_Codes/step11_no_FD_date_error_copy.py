#copying error shapefiles into a new folder for analysis

import glob, os
import shutil

direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\Output\\Round2\\'

for year in range(2019, 2020):
    inpath = direct  + str(year) + '\\IDW_error\\no_af\\error\\'
    opath = direct + "no_FD_date_error\\"+ str(year) + '\\'
    if not os.path.exists(opath): os.makedirs(opath)
    files = glob.glob(inpath + '*')

    for file in files:

        shutil.copy2(file, opath)