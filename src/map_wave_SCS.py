import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.animation as animation

from samples_SCS import sample_list


plt.figure()
my_map = Basemap( # projection='lcc', # default 'merc'
            resolution = 'l', area_thresh = 1000.0,
            lat_0=12, lon_0=110, 
            llcrnrlon=100, llcrnrlat=1,
            urcrnrlon=121, urcrnrlat=25)
my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color = 'coral')
my_map.drawmapboundary()
my_map.drawmeridians(np.arange(100, 122, 2))
my_map.drawparallels(np.arange(0, 26, 2))

# coords = [(52.00,1.50), (50.75,-4.75), (55.50,-5.00), (53.50,-3.50), (52.50,-4.25), (50.50,-3.25), (56.25,-2.50),
#                 (53.5,0.25), (54.00,-3.25), (51.75,-5.25), (50.75,-1.00), (51.25,-3.50), (51.50,1.00), (55.00,-1.25),
#                 ]

# Code portion similar to `extract_wave_data_zone.py`
RESOLUTION = 0.5  # deg.
LON_MIN = 100
LON_MAX = 121
LAT_MIN = 1
LAT_MAX = 25
N_LON = int((LON_MAX - LON_MIN) / RESOLUTION) + 1
N_LAT = int((LAT_MAX - LAT_MIN) / RESOLUTION) + 1

assert N_LON <= 26 * 26, 'Number of longitudinal grids exceeds the encoding range from AA to ZZ'

xlabels = []
first_ch = 'A'
second_ch = 'A'

for _ in range(N_LON):
    xlabels.append(first_ch + second_ch)
    next_ch = chr(ord(second_ch) + 1)
    if next_ch <= 'Z':
        second_ch = next_ch
    else:
        first_ch = chr(ord(first_ch) + 1)
        second_ch = 'A'

ylabels = []
for i in range(N_LAT):
    ylabels.append('%02i' % i)

xlocs = [LON_MIN + i*RESOLUTION for i in range(N_LON)]
ylocs = [LAT_MIN + i*RESOLUTION for i in range(N_LAT)]

lon_of_code = dict(zip(xlabels, xlocs))
lat_of_code = dict(zip(ylabels, ylocs))


for label in sample_list:
    lon = lon_of_code[label[0:2]]
    lat = lat_of_code[label[2:4]]
    point = my_map.plot(lon, lat, 'go', markersize=1)

# Annotate the long/lat axes
labels_lon = ['AA', 'AE', 'AI', 'AM', 'AQ', 'AU', 'AY', 'BC', 'BG', 'BK', 'BO']
labels_lat = ['%02i' % i for i in range(3, 49, 4)]
for lon, label in zip(range(100, 122, 2), labels_lon):
    plt.annotate(label, (lon, 1), ha='center', va='top').set_zorder(10)

for lat, label in zip(range(2, 26, 2), labels_lat):
    plt.annotate(label, (100, lat), ha='right', va='center').set_zorder(10)


plt.savefig('map_SCS.png')

