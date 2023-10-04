import sys
import pandas as pd
import geopandas as gpd
import dask.dataframe as dd
import dask_geopandas
from glob import glob

csvs_regex = '/explore/nobackup/projects/ilab/projects/LobodaTFO/data/ABoVE_DoB/DAAC_Update_2023/Active_Fires/MODIS_Active_Fire/*.csv'


def main():

    ddf = dd.read_csv(csvs_regex, dtype={
        'latitude': 'float64', 'longitude': 'float64', 'brightness': 'float64',
        'scan': 'float64', 'track': 'float64'
    })
    ddf = ddf.set_geometry(
            dask_geopandas.points_from_xy(ddf, 'longitude', 'latitude')
    )
    print(ddf.shape)
    print(ddf.head())


# -----------------------------------------------------------------------------
# Invoke the main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())

