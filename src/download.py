# Download wave GRIB file from NOAA repository
# Update NOAA link
# Update for Python 3 (urllib.request instead of urllib)

from urllib.request import urlretrieve

# the_path = "ftp://polar.ncep.noaa.gov/history/waves/"
the_path = "https://www.ncei.noaa.gov/thredds-ocean/catalog/ncep/nww3"
# example: https://www.ncei.noaa.gov/thredds-ocean/fileServer/ncep/nww3/2015/10/glo_30m/multi_1.glo_30m.tp.201510.grb2
year_range = range(2011,2013) + [2015]
month_range = range(1, 13)

for year in year_range:
	for month in month_range:
		for qty in ['hs', 'tp', 'dp']:
			filename = "multi_1.glo_30m.%s.%i%02i.grb2" % (qty, year, month)
			print("Downloading %s ... " % filename)
			try:
				urlretrieve(the_path + filename, filename=filename)
			except:
				continue
