import urllib
the_path = "ftp://polar.ncep.noaa.gov/history/waves/"
#for filename in ["multi_1.glo_30m.tp.200502.grb2", "multi_1.glo_30m.hs.200502.grb2"]:
#	print "Downloading %s ... " % filename
#	urllib.urlretrieve(the_path + filename, filename=filename)
# urllib.urlretrieve("http://google.com/index.html", filename="local/index.html")

for year in range(2011,2013)+[2015]:
	for month in range(1, 13):
		for qty in ['hs', 'tp', 'dp']:
			filename = "multi_1.glo_30m.%s.%i%02i.grb2" % (qty, year, month)
			print "Downloading %s ... " % filename
			try:
				urllib.urlretrieve(the_path + filename, filename=filename)
			except:
				continue
