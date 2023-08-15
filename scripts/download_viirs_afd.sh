#!/bin/sh

# Download VIIRS active fires from FIRMS for the United States and Canada
# bash ./download_modis_afd.sh $path_to_store_data

for YEAR in {2012..2021}
do
    wget -O "$1/viirs-snpp_${YEAR}_United_States.csv" "https://firms.modaps.eosdis.nasa.gov/data/country/viirs-snpp/${YEAR}/viirs-snpp_${YEAR}_United_States.csv"
    wget -O "$1/viirs-snpp_${YEAR}_Canada.csv" "https://firms.modaps.eosdis.nasa.gov/data/country/viirs-snpp/${YEAR}/viirs-snpp_${YEAR}_Canada.csv"
done
