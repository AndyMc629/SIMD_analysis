#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 20:22:18 2017

@author: apm13

Analyse and plot choropleths for Social Index of Multiple Deprivation and 
Disability data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fiona
from itertools import chain
from mpl_toolkits.basemap import Basemap
import pyproj
from functools import partial
from shapely.geometry import box
from shapely.ops import transform


# Import shapefile
shp = fiona.open('data/glasgow_city_wards_3rd.shp')
p_in = pyproj.Proj(shp.crs)
bound_box = box(*shp.bounds)

p_out = pyproj.Proj({'init': 'WGS84'})  # aka WGS84
project = partial(pyproj.transform, p_in, p_out)

bound_box_wgs84 = transform(project, bound_box)

print('native box: ' + str(bound_box))
print('WGS84 box: ' + str(bound_box_wgs84))

shp.close()

"""
crs_data = shp.crs
bds = shp.bounds
shp.close()
"""

extra = 0.01
# bounds need to be datum-shifted
wgs84 = pyproj.Proj("+init=EPSG:4326")
# osgb36 = pyproj.Proj("+init=EPSG:27700")
ll = pyproj.transform(osgb36, wgs84, bds[0], bds[1])
ur = pyproj.transform(osgb36, wgs84, bds[2], bds[3])
#ll = (bds[0], bds[1])
#ur = (bds[2], bds[3])
coords = list(chain(ll, ur))
w, h = coords[2] - coords[0], coords[3] - coords[1]

# Create basemap
m = Basemap(
    projection='tmerc',
    lon_0 = 4.2518,
    lat_0 = 55.8642,
    ellps = 'WGS84',
    llcrnrlon=coords[0] - extra * w,
    llcrnrlat=coords[1] - extra + 0.01 * h,
    urcrnrlon=coords[2] + extra * w,
    urcrnrlat=coords[3] + extra + 0.01 * h,
    lat_ts=0,
    resolution='i',
    suppress_ticks=True)
m.readshapefile(
    'data/OS/glasgow_city_wards_3rd.shp',
    'Glasgow',
    color='none',
    zorder=2)