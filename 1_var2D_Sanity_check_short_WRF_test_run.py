'''
Function: to check the variables in the short WRF test run.
Date: 20200710

'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr

from netCDF4 import Dataset
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature #LAND, OCEAN, COASTLINE, BORDERS, LAKES, RIVERS
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,cartopy_ylim, latlon_coords)

## to avoid Cartopy adding states error message
#urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain (_ssl.c:1076)>

###
import ssl
try:
     _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
# Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
# Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

####

path = '/home/qin5/Data/WRF_short_testrun/'
ncfile = Dataset(path+'wrfout_d01_2015-05-05_00_00_00.nc')

#ds = xr.open_dataset(path+'wrfout_d01_2015-05-05_00_00_00.nc')
#print(ds)

var2D_str_tried = ['T2','Q2','TSK','SWDNT','SWUPT','SWUPTC','OLR','LWUPTC','SWUPB','SWUPBC','SWDNB',\
             'SWDNBC','LWUPB','LWUPBC','LWDNB','LWDNBC','HFX','LH']
var2D_str_tried2 = ['PSFC','CFRACT','SFCEVP','PBLH','HGT','ALBEDO','EMISS','SFROFF','CANWAT']
var2D_str = ['RAINC','RAINNC']

for i_var in range(len(var2D_str)):
    var2D = getvar(ncfile, var2D_str[i_var])
    print(var2D)

    lats, lons = latlon_coords(var2D)

    # Get the cartopy mapping object
    cart_proj = get_cartopy(var2D)

    # Create a figure
    fig = plt.figure(figsize=(8,6))
    # Set the GeoAxes to the projection used by WRF
    ax = plt.axes(projection=cart_proj)

    # Download and add the states and coastlines
    states = NaturalEarthFeature(category="cultural", scale="50m",\
            facecolor="none", name="admin_1_states_provinces_shp")
    ax.add_feature(states, linewidth=.5, edgecolor="black")
    ax.coastlines('50m', linewidth=0.8)

    #plt.contour(to_np(lons), to_np(lats), to_np(var2D),  colors="black",\
    #        transform=crs.PlateCarree())
    plt.contourf(to_np(lons), to_np(lats), to_np(var2D),  \
            transform=crs.PlateCarree(),cmap=get_cmap("jet"))

    # Add a color bar
    plt.colorbar(ax=ax, shrink=.98)

    # Set the map bounds
    ax.set_xlim(cartopy_xlim(var2D))
    ax.set_ylim(cartopy_ylim(var2D))

    # Add the gridlines
    ax.gridlines(color="black", linestyle="dotted")

    plt.title(var2D.attrs['description']+' ('+var2D.attrs['units']+'), 2015-05-05:00:00:00')

    plt.show()
    fig.savefig('./Figures/'+var2D_str[i_var]+'.png', dpi=500, transparent=True, bbox_inches='tight')


