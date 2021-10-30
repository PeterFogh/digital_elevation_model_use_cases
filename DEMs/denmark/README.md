# Danish Elevation Models
The Danish Elevation Models is also called DK-DEM or Danish Height Model ("Danmarks Højdemodel (DHM)" in danish). Read this intro of DHM in danish https://sdfe.dk/hent-data/danmarks-hoejdemodel.

The DHM is a collection of digital elevation models (DEMs) that have been preprocessed to products for various applications. The various DEMs are detailed and public available (after the year 2021 at https://dataforsyningen.dk/data?filter=129;tag-135;137,99;tag-101&view=gallery - before 2021 at https://kortforsyningen.dk/indhold/data. The DHN have as of November 2021 been updated twice - in the years 2007 and 2015.

Each DHM version and their data products have been produced and quality controlled by Digital Height Model Quality Control system (DHMQC), see https://github.com/Kortforsyningen/DHMQC.

## Danish Elevation Model 2015
- Documentation: 
  - DHM product specification v1.0.0: https://kortforsyningen.dk/sites/default/files/dhm-prodspec-v1.0.0.pdf
  - Quality assessment report to the Danish Elevation Model (DK-DEM): https://www.kortforsyningen.dk/sites/default/files/qualityassessmentdk-dem.pdf
  - About data docs - contains links to docs for each DHM data product: https://www.kortforsyningen.dk/sites/default/files/about.data_.pdf

## Danish Elevation Model 2007
- Documentation: 
  - DHM 2007 terrain model: https://kortforsyningen.dk/sites/default/files/old_gst/DOKUMENTATION/Data/dk_dhm-2007_terraen_okt_2014.pdf
  - DHM 2007 surface model: https://kortforsyningen.dk/sites/default/files/old_gst/DOKUMENTATION/Data/dk_dhm-2007_overflade_okt_2014.pdf
  - About data docs - contains links to docs for each DHM data product: https://www.kortforsyningen.dk/sites/default/files/about.data_.pdf

## Download data
The DHM data products are public available and can (as of November 2021) be download via "Datafordeler" (https://dataforsyningen.dk/data?filter=129;tag-135;137,99;tag-101&view=gallery) or Kortforsyningn (https://kortforsyningen.dk/indhold/data)

### Fetch data from Datafordeler
Datafordeler (in english "the data distributer") facilitate download of many public available Danish geo data - replaces Kortforsyningen in 2020-2021. This page documents the new way to fetch DHM data after 2021, see https://confluence.sdfe.dk/pages/viewpage.action?pageId=25722925.

### Fetch data from Kortforsyningen
Kortforsigningen (in english "the map supply") facilitate download of many public available Danish geo data - however it is phased out in 2020-2021 and replaced by "Datafordeler". The DHM data products may be downloaded from the "ftp.kortforsyningen.dk" ftp server, see https://kortforsyningen.dk/indhold/om-download and there after https://kortforsyningen.dk/indhold/download-af-data. Note that the DHM is considered a non-static dataset, i.e. it may be updated at any point in time. You can be notified about changes via Atom feed, see https://kortforsyningen.dk/content/atom-feed.

## Examples of a danish elevation model data products

### DHM/Terræn - DTM
The DTM is specified in the document "dk_dhm_terraen_v2_1_aug_2016.pdf". The DTM consist of a raster grid, 0.4m x 0.4m resolution, of the height of the terrain relative to the average sea level (as defined by the "Dansk Vertikal Reference 1990" (DVR90)).

The DTM uses the ETRS89 reference system with an UTM32N projection (i.e. EPSG:25832). The coordinates of the bounding of the entire dataset is (V:440000, E:900000, N:6410000, S:6040000).

#### The downloaded dataset
The downloaded dataset (548GB total) has the following folder structure:

- DTM/
  - DTM-6[YY]_[XX]_TIF_UTM32-ERTSA89.zip (10km x 10km DTM tiles for relevant values of XX, YY)
  - GRID/
    - GRID_2014_DTM_SHP_UTM32-ETRS89.zip (overview of the layout of the 10km x 10km tiles)
    - GRID_2014_DTM_TAB_UTM32-ETRS89.zip
  - TIF-ASC-konvertering.pdf (a guide for converting to ASC format)

The (XX, 6YY) values represent the coordinates of the south west corners of the 10km x 10km tiles. Thus, for each 10km x 10km tile XX increments by 1 from 604 to 641 and YY increments by 1 from 44 to 90, although no tiles exist for areas that have no land surface (ocean tiles).

The GRID vector files contains an overview of the available 10km x 10km tiles.

In each DTM-6[YY]_[XX]_TIF_UTM32-ERTSA89.zip, one finds 100 deflate compressed GeoTIFF images of 1km x 1km sub-tiles of its 10km x 10km tile named DTM_1km_6[YYY]_[XXX].tif. Each of these 1km x 1km tiles consists of 2500px x 2500px (corresponding to the resolution of 0.4m x 0.4m). Again, the (XXX, 6YYY) values identify the south west corner of the tile.

#### The unpacked DTM
On Ahsoka at /projects/BDICG/3 Hoejdedata DK/DDS_unpacked in the tiles folder, one may find all of the 1km x 1km tiles. The integrity of these files have been checked against the md5 checksums that are shipped with the tiles. The entire unpackage-and-check procedure has been carried out using the script "unpack_and_check_DHM.py"

#### General strategy for using the DTM with xarray
Specify a bounding box of the relevant area in ETRS84/UTM32N (EPSG:25832).
Identify the (XXX, 6YYY) 1km x 1km tiles that overlap with the bounding box of interest.
Load the relevant GeoTIFF files into an xarray dataarray - possibly converting the grids to another reference system (e.g. WGS84), if needed.
Re-grid the data to the grid of the relevant area (e.g. using the xesmf python package for lon/lat referenced data or xarray.interp_like for projected data).