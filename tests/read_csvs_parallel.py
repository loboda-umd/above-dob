import sys
import pandas as pd
import geopandas as gpd
from glob import glob
from multiprocessing import Pool, cpu_count

csvs_regex = '/explore/nobackup/projects/ilab/projects/LobodaTFO/data/ABoVE_DoB/DAAC_Update_2023/Active_Fires/MODIS_Active_Fire/*.csv'

def read_gdf(filename):
    gdf = gpd.read_file(filename, crs='epsg:4326')
    return gdf


def main():

    csvs_list = glob(csvs_regex)
    print(len(csvs_list))

    with Pool(processes=cpu_count()*2) as p:
        result = p.map(read_gdf, csvs_list)
    gdf = pd.concat(result)
    print(gdf.shape)

# -----------------------------------------------------------------------------
# Invoke the main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())

