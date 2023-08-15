# ABoVE Date of Born (DoB) DAAC Dataset

[DAAC ABoVE DoB](https://daac.ornl.gov/ABOVE/guides/Wildfires_Date_of_Burning.html)

## Data Download

1. Fire Perimeters: download the fire perimeters from the Alaska Large Fire Database (ALFD) and the
National Burned Area Composite (NBAC). The previous CNFDB used in DAAC v1.1 has not been updated since
2020, and thus has been replaced for Canada in versions after v1.1.

2. Active Fires: active fires are taken from FIRMS. A simple script to download the active fires as CSVs
is listed below. To run the script, just specify the output path at the end of the command:

```bash
bash scripts/download_modis_afd.sh .
```

## Process DoB

1. Join and Georeference Active Fires

```bash
python 1_preprocess_active_fires.py
```

2. Join Fire Perimeters

```bash
python 2_preprocess_fire_perimeters.py
```

## System Dependencies

TBD

## References

- Billmire, M., N. H. F. French, T. Loboda, R. C. Owen, and M. Tyner. 2014. Santa Ana winds and predictors of wildfire progression in southern California. International Journal of Wildland Fire 23:1119. http://dx.doi.org/10.1071/WF13046

- Giglio, L. 2015. MODIS Collection 6 Active Fire Product User’s Guide Revision A. Unpublished manuscript, Department of Geographical Sciences, University of Maryland. https://cdn.earthdata.nasa.gov/conduit/upload/3865/MODIS_C6_Fire_User_Guide_A.pdf

- Giglio, L., J. Descloitres, C.O. Justice, and Y.J. Kaufman. 2003. An Enhanced Contextual Fire Detection Algorithm for MODIS. Remote Sensing of Environment 87:273–282. http://dx.doi.org/10.1016/S0034-4257(03)00184-6

- Loboda, T.V., and J.V. Hall. 2017. ABoVE: Wildfire Date of Burning within Fire Scars across Alaska and Canada, 2001-2015. ORNL DAAC, Oak Ridge, Tennessee, USA. https://doi.org/10.3334/ORNLDAAC/1559

- MODIS Collection 6 NRT Hotspot / Active Fire Detections MCD14ML distributed from NASA FIRMS. Available on-line [https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms]. https://doi.org/10.5067/FIRMS/MODIS/MCD14ML
