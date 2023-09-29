import sys
import time
import logging
import argparse
import pandas as pd
import geopandas as gpd
from glob import glob
from dob import DoB
from datetime import date


# -----------------------------------------------------------------------------
# main
#
# python dob_pipeline.py -s preprocess_af
# -----------------------------------------------------------------------------
def main():

    # Process command-line args.
    desc = 'Use this application to process DoB for Alaska and Canada'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-sy',
                        '--start-year',
                        type=int,
                        required=False,
                        default=date.today().year - 1,
                        dest='start_year',
                        help='Start year for DoB')

    parser.add_argument('-ey',
                        '--end-year',
                        type=int,
                        required=False,
                        default=date.today().year - 1,
                        dest='end_year',
                        help='End year for DoB')

    parser.add_argument('-af',
                        '--active-fire-regex',
                        type=str,
                        required=True,
                        dest='af_regex',
                        help='Active fire regex')

    parser.add_argument('-afp',
                        '--alaska-fire-perimeter-filename',
                        type=str,
                        required=True,
                        dest='afp_filename',
                        help='Alaska fire perimeter filename')

    parser.add_argument('-cfp',
                        '--canada-fire-perimeter-filename',
                        type=str,
                        required=True,
                        dest='cfp_filename',
                        help='Canada fire perimeter filename')

    parser.add_argument('-aoi',
                        '--aoi-filename',
                        type=str,
                        required=True,
                        dest='aoi_filename',
                        help='Filename path to AOI')

    parser.add_argument('-o',
                        '--output-dir',
                        type=str,
                        required=True,
                        dest='output_dir',
                        help='Fire perimeter regex')

    parser.add_argument(
                        '-s',
                        '--pipeline-step',
                        type=str,
                        nargs='*',
                        required=True,
                        dest='pipeline_step',
                        help='Pipeline step to perform',
                        default=[
                            'preprocess_af', 'preprocess_fp',
                            'fire_progression'
                        ],
                        choices=[
                            'preprocess_af', 'preprocess_fp',
                            'fire_progression', 'all'
                        ])

    args = parser.parse_args()

    # Setup logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s; %(levelname)s; %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Setup timer to monitor script execution time
    timer = time.time()

    # Initialize pipeline object
    pipeline = DoB(
        args.af_regex,
        args.afp_filename,
        args.cfp_filename,
        args.aoi_filename,
        args.start_year,
        args.end_year,
        args.output_dir,
    )

    # DoB pipeline steps
    if "preprocess_af" in args.pipeline_step or "all" in args.pipeline_step:
        pipeline.preprocess_active_fires()
    if "preprocess_fp" in args.pipeline_step or "all" in args.pipeline_step:
        pipeline.preprocess_fire_perimeters()
    if "fire_progression" in args.pipeline_step or "all" in args.pipeline_step:
        pipeline.calculate_fire_progression()

    logging.info(f'Took {(time.time()-timer)/60.0:.2f} min.')


# -----------------------------------------------------------------------------
# Invoke the main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())
