#!/bin/sh

# Download MODIS active fires from FIRMS for the United States and Canada
# bash ./download_modis_afd.sh $path_to_store_data

for YEAR in {2000..2022}
do
    wget -O "$1/modis_${YEAR}_United_States.csv" "https://firms.modaps.eosdis.nasa.gov/data/country/modis/${YEAR}/modis_${YEAR}_United_States.csv" 
    wget -O "$1/modis_${YEAR}_Canada.csv" "https://firms.modaps.eosdis.nasa.gov/data/country/modis/${YEAR}/modis_${YEAR}_Canada.csv"
done
