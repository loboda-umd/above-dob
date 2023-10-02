import sys
import pandas as pd
import geopandas as gpd
from glob import glob

csvs_regex = '/explore/nobackup/projects/ilab/projects/LobodaTFO/data/ABoVE_DoB/DAAC_Update_2023/Active_Fires/MODIS_Active_Fire/*.csv'

import numpy as np
from multiprocessing import Pool

def read_gdf(filename):
    gdf = gpd.read_file(filename, crs='epsg:4326')
    return gdf


def main():

    csvs_list = glob(csvs_regex)
    print(len(csvs_list))

    gdf = []
    for filename in csvs_list:
        gdf.append(read_gdf(filename))

    gdf = pd.concat(gdf)
    print(gdf.shape)

# -----------------------------------------------------------------------------
# Invoke the main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())

