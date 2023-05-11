## Merced daily weather history bulk download

This file (`data/GHCN_USC00045532_USW00023257.csv`) contains daily weather reports from Merced Regional Airport stations (GHCN:USC00045532 & GHCN:USW00023257). The start date is June 1, 1899.

    GHCN:USC00045532
    - Historical data starting from June 1, 1899

    GHCN:USW00023257
    - More recent up to date data starting from August 1, 1998


The data fields are:

* PRCP - precipitation (inches)
* SNOW - snowfall (inches)
* SNWD - snow depth (inches)
* TMAX - maximum temperature (degrees Fahrenheit)
* TMIN - minimum temperature

Detailed field definitions are in [this NOAA documentation file](ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt).

This file is created by running `R/Retrieve_GHCN_USC00045532_USW00023257.R`. That script downloads the latest data, unzips it, filters for the desired statistics, converts those values to the desired units, formats date columns, and converts the data from long to wide format.
