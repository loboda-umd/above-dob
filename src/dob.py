import os
import logging
import pandas as pd
import geopandas as gpd
from glob import glob
from pathlib import Path
from itertools import repeat
from multiprocessing import Pool, cpu_count


class DoB(object):

    def __init__(
                self,
                af_regex: str,
                afp_filename: str,
                cfp_filename: str,
                aoi_filename: str,
                start_year: int,
                end_year: int,
                output_dir: str,
                epsg: str = 'ESRI:102001'
            ):

        # epsg
        self.epsg = epsg

        # set active fire perimeters regex
        self.af_regex = af_regex

        # set Alaska fire perimeters regex
        self.afp_filename = afp_filename

        # set Canada fire perimeters regex
        self.cfp_filename = cfp_filename

        # set start year
        self.start_year = start_year

        # set end year
        self.end_year = end_year

        # set output directory
        self.output_dir = output_dir

        # area of interest
        self.aoi_gdf = gpd.read_file(aoi_filename)

        # active fire output dir
        self.af_output_dir = os.path.join(self.output_dir, 'active_fires')

        # active fire output dir
        self.fp_output_dir = os.path.join(self.output_dir, 'fire_perimeters')

    def preprocess_active_fires_subprocess(
                self,
                filenames: list,
                year: int,
                aoi_gdf: gpd.GeoDataFrame
            ):
        """
        Subprocess to handle parallel preprocessing.
        filename_pair: list of two filenames with active fires (Alaska, Canada)
        """
        logging.info('Starting preprocess_active_fires_subprocess')

        gdf_list = []
        for filename in filenames:
            
            # read csv file
            af_df = pd.read_csv(filename)
            
            # convert to GeoDataFrame
            af_gdf = gpd.GeoDataFrame(
                af_df,
                geometry=gpd.points_from_xy(af_df.longitude, af_df.latitude),
                crs="EPSG:4326"
            )
            gdf_list.append(af_gdf)
            logging.info(f'{Path(filename).stem} - {af_gdf.shape}')
        
        # concatenate dataframes
        full_gdf = gpd.GeoDataFrame(
            pd.concat(gdf_list, ignore_index=True), crs=gdf_list[0].crs
        ).to_crs(self.epsg)

        full_gdf = full_gdf.clip(aoi_gdf)

        # save output file
        full_gdf.to_file(os.path.join(self.af_output_dir, f'active_fires_{year}.gpkg'))
        return

    def preprocess_active_fires(self):
        """
        Preprocess and georeference active fire.
        """
        # create output directory for active fires
        os.makedirs(self.af_output_dir, exist_ok=True)
        logging.info(f'Created {self.af_output_dir}')

        # get active fire filenames
        af_filenames = glob(self.af_regex)
        logging.info(f'Processing {len(af_filenames)} active fire filenames.')

        # iterate over each year
        filename_pairs = []
        for year in range(self.start_year, self.end_year + 1):

            # we are going to get the files for each year using regex
            # we assume each file has the year in the filename
            file_matches = [fi for fi in af_filenames if str(year) in Path(fi).stem]
            if len(file_matches) == 0:
                logging.info(f'No active fires found for {year}, skipping year.')
                continue
            else:
                filename_pairs.append(file_matches)

        # Distribute a file per processor
        p = Pool(processes=cpu_count())
        p.starmap(
            self.preprocess_active_fires_subprocess,
            zip(
                filename_pairs,
                range(self.start_year, self.end_year + 1),
                repeat(self.aoi_gdf)
            )
        )
        p.close()
        p.join()

        logging.info(f'Saved output to {self.af_output_dir}.')

        return

    def preprocess_fire_perimeters_subprocess(
                self,
                gdf: list,
                year: int,
            ):
        """
        Subprocess to handle parallel preprocessing.
            gdf: GeoDataFrame to save
        """
        logging.info(f'Starting preprocess_fire_perimeters_subprocess: {year}')

        # reset index to start from 0
        gdf = gdf.reset_index(drop=True)

        # do we really need to buffer 1000m?
        gdf['geometry'] = gdf['geometry'].buffer(500)

        # assign unique id to fire based on index
        gdf['UID_Fire'] = gdf.index

        # save output file
        gdf.to_file(
            os.path.join(self.fp_output_dir, f'fire_perimeters_{year}.gpkg'))
        return

    def preprocess_fire_perimeters(self):
        """
        Preprocess and georeference fire perimeters.
        """
        # create output directory for active fires
        os.makedirs(self.fp_output_dir, exist_ok=True)
        logging.info(f'Created {self.fp_output_dir}')

        # read fire perimeters from Alaska
        afp_gdf = gpd.read_file(self.afp_filename)
        logging.info(f'{afp_gdf.shape[0]} Alaska fire perimeters')

        # read fire perimeters from Canada
        cfp_gdf = gpd.read_file(self.cfp_filename )
        logging.info(f'{cfp_gdf.shape[0]} Canada fire perimeters')

        # fix projection between both database
        afp_gdf = afp_gdf.to_crs(self.epsg)
        cfp_gdf = cfp_gdf.to_crs(self.epsg)

        # get attributes from Alaska database
        afp_gdf = afp_gdf[['PERIMETERD', 'FIREYEAR', 'FIREID', 'geometry']]
        afp_gdf['FIREYEAR'] = afp_gdf['FIREYEAR'].astype(int)
        afp_gdf['FD_Agency'] = 'AK'
        afp_gdf = afp_gdf.rename(
            columns={'FIREID': 'REF_ID', 'FIREYEAR': 'Year'})

        # get attributes from Alaska database
        cfp_gdf = cfp_gdf[
            ['SDATE', 'EDATE', 'AFSDATE', 'AFEDATE',
             'CAPDATE', 'YEAR', 'NFIREID', 'geometry']
        ]
        cfp_gdf['YEAR'] = cfp_gdf['YEAR'].astype(int)
        cfp_gdf['FD_Agency'] = 'CA'
        cfp_gdf = cfp_gdf.rename(columns={'YEAR': 'Year', 'NFIREID': 'REF_ID'})

        # merge the two databases
        fp_gdf = pd.concat([afp_gdf, cfp_gdf], axis=0)
        logging.info(f'Merged Alaska/Canada, {fp_gdf.shape} fire perimeters.')
        
        # filter by year
        fp_gdf = fp_gdf[
            (fp_gdf['Year'] >= self.start_year) &
            (fp_gdf['Year'] <= self.end_year)
        ]
        logging.info(f'Total fires {self.start_year}-{self.end_year}: {fp_gdf.shape}.')

        # iterate over each year
        perimeter_gdfs = []
        for year in range(self.start_year, self.end_year + 1):

            # we are going to strip the dataframe for each year
            # and save them in their own file
            perimeter_gdf = fp_gdf[fp_gdf['Year'] == year]
            if perimeter_gdf.shape[0] == 0:
                logging.info(f'No fire perimeters found for {year}, skipping year.')
                continue
            else:
                logging.info(f'Total fires {year}: {perimeter_gdf.shape[0]}.')
                perimeter_gdfs.append(perimeter_gdf)

        # Distribute a file per processor
        p = Pool(processes=cpu_count())
        p.starmap(
            self.preprocess_fire_perimeters_subprocess,
            zip(
                perimeter_gdfs,
                range(self.start_year, self.end_year + 1),
            )
        )
        p.close()
        p.join()

        logging.info(f'Saved output to {self.fp_output_dir}.')

        return

    def calculate_fire_progression_subprocess(self):

        # get fire perimeter coordinates
        xmin, ymax, res, w, h, fire_geom = compute_fire_perimeter(tundra_fires, FIRE_ID)

        # save active fires for that perimeter

        # saved cleaned active fires

        # compute IDW

    def calculate_fire_progression(self):

        # gather active fire filenames
        af_filenames = sorted(glob(os.path.join(self.af_output_dir, '*.gpkg')))
        logging.info(f'Loaded {len(af_filenames)} active fire filenames.')

        # gather fire perimeter filenames
        fp_filenames = sorted(glob(os.path.join(self.fp_output_dir, '*.gpkg')))
        logging.info(f'Loaded {len(fp_filenames)} fire perimeter filenames.')

        # iterate over each filename
        for af_filename, fp_filename in zip(af_filenames, fp_filenames):

            # read active fire GeoDataFrame
            af_gdf = gpd.read_file(af_filename)

            # read fire perimeter GeoDataFrame

        """
        for af_filename, fp_filename in zip(af_filenames, fp_filenames):
        
        # get fire perimeter
        xmin, ymax, res, w, h, fire_geom = compute_fire_perimeter(tundra_fires, FIRE_ID)
        print(fire_geom)

        # get modis and viirs active fire dataframes, save as GPKG
        fire_incident_to_gpkg(tundra_viirs, tundra_fires, FIRE_ID, f'{FIRE_ID}_viirs.gpkg')
        fire_incident_to_gpkg(tundra_modis, tundra_fires, FIRE_ID, f'{FIRE_ID}_modis.gpkg')

        # COMPUTE IDW
        fire_idw_viirs = compute_idw(f'{FIRE_ID}_viirs.gpkg', xmin, ymax, res, w, h, fire_geom)
        fire_idw_viirs_clean = compute_idw(f'{FIRE_ID}_viirs_clean.gpkg', xmin, ymax, res, w, h, fire_geom)

        fire_idw_modis = compute_idw(f'{FIRE_ID}_modis.gpkg', xmin, ymax, res, w, h, fire_geom)
        fire_idw_modis_clean = compute_idw(f'{FIRE_ID}_modis_clean.gpkg', xmin, ymax, res, w, h, fire_geom)
        """


    def compute_fire_perimeter(tundra_fires, fire_incident):
        fire_row = tundra_fires[tundra_fires.UniqueFireIdentifier == fire_incident]
        bbox = fire_row.total_bounds
        xmin, ymin, xmax, ymax = bbox
        res = 30 # desired resolution
        w = (xmax - xmin) // res 
        h = (ymax - ymin) // res
        return [round(xmin), round(ymax), res, w, h, fire_row]


    def clean_active_fires(active_fire_gdf):
        
        x_coords = ((active_fire_gdf.geometry.x / 100) + 0.5).to_list()
        y_coords = ((active_fire_gdf.geometry.y / 100) + 0.5).to_list()
        del_index = []
        
        for i_id in range(0, active_fire_gdf.shape[0]):
            x1 = int(x_coords[i_id])
            y1 = int(y_coords[i_id])

            for k_id in range(i_id + 1, active_fire_gdf.shape[0]):
                x2 = int(x_coords[k_id])
                y2 = int(y_coords[k_id])
                if x1 == x2 and y1 == y2:
                    del_index.append(active_fire_gdf.index[k_id])
        return del_index

    def fire_incident_to_gpkg(af_geometry, tundra_fires, fire_incident, output_filename):
        af_geometry_clip = af_geometry.clip(tundra_fires[tundra_fires.UniqueFireIdentifier == fire_incident])
        acq_date = pd.to_datetime(af_geometry_clip['acq_date'])
        af_geometry_clip['JD'] = acq_date.dt.dayofyear.astype(str)
        af_geometry_clip.to_file(output_filename)
        
        delete_indexes = clean_active_fires(af_geometry_clip)
        af_geometry_clip_clean = af_geometry_clip.drop(delete_indexes)
        af_geometry_clip_clean.to_file(f'{Path(output_filename).with_suffix("")}_clean.gpkg')

        return af_geometry_clip_clean