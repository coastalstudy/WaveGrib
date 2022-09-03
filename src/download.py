# Download wave GRIB file from NOAA repository
# Update NOAA link
# Update for Python 3 (urllib.request instead of urllib)

import os
from urllib.request import urlretrieve

# old: path = "ftp://polar.ncep.noaa.gov/history/waves/"
# full path example: https://www.ncei.noaa.gov/thredds-ocean/fileServer/ncep/nww3/2015/10/glo_30m/multi_1.glo_30m.tp.201510.grb2

core_path = "https://www.ncei.noaa.gov/thredds-ocean/fileServer/ncep/nww3/"
year_range = [2011]
month_range = range(3, 4)

for year in year_range:
    for month in month_range:
        for qty in ['hs', 'tp', 'dp']:
            var_path = '%i/%02i/glo_30m/' % (year, month)
            filename = "multi_1.glo_30m.%s.%i%02i.grb2" % (qty, year, month)
            print("\nDownloading %s ... " % filename, end='')
            try:
                urlretrieve(os.path.join(core_path, var_path, filename), 
                            filename=os.path.join('../downloads', filename))
            except:
                print('Failed', end='')
                continue

print()