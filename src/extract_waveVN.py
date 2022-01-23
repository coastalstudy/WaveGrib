#!/usr/bin/python

# use default Python, not Anaconda Python

import pygrib
import sys
import time
import datetime

# Locations shown in the `map.png` file
locations = [(108.0, 21.0), (107.5, 20.5), (107.0, 20.5), \
(106.5, 20.0), (106.0, 19.5), (106.0, 19.0), (106.5, 18.5), \
(107.0, 18.0), (107.0, 17.5), (107.5, 17.0), (108.0, 16.5), \
(108.5, 16.0), (109.0, 15.5), (109.5, 15.0), (109.5, 14.5), \
(109.5, 14.0), (109.5, 13.5), (110.0, 13.0), (110.0, 12.5), \
(109.5, 12.0), (109.5, 11.5), (109.0, 11.0), (108.5, 10.5), \
(108.0, 10.5), (107.5, 10.0), (107.0, 9.5), (106.5, 9.0), \
(106.0, 9.0), (105.5, 8.5), (104.5, 8.5), (104.5, 9.0), \
(104.5, 9.5), (104.5, 10.0)]

def idxat(lon, lat):
	''' Converting from `lon`, `lat` to indices of the grid data cube.'''
	idx = int(round((77.5 - lat)*2))
	idy = int(round(lon*2))
	return idx, idy 

def process(yrmo, nmo, outfile):
	""" Process the wave data, reading grib files and 
		extract the wave time series to the output text file.

		Parameters
		----------
		`yrmo`: `str`
			The year and month at the beginning of extraction,
			with the format `yyyymm`
			
		`nmo`: `int`
			Number of months to extract the wave data 

		`outfile`: `str`
			Name of the output plain text files (without extension)

		Returns
		-------
		None

		Side effects
		------------
		A text file created.
	"""
	st = time.time()
	t = datetime.datetime(yrmo/100, yrmo%100, 1, 3, 0)
	dt = datetime.timedelta(hours=3)
	outfile.write("DateTime\t")
	for l in locations:
		outfile.write("Hs\tTp\tDir\t")
	
	outfile.write("\n")
	
	for j in range(nmo):
		num = yrmo + j  
		fileHs = 'multi_1.glo_30m.hs.%d.grb2' % num
		fileTp = 'multi_1.glo_30m.tp.%d.grb2' % num
		fileDir = 'multi_1.glo_30m.dp.%d.grb2' % num

		print "Year Month = ", num
		
		grbsHs = pygrib.open(fileHs)
		grbsTp = pygrib.open(fileTp)
		grbsDir = pygrib.open(fileDir)

		grbsHs.seek(1)
		grbsTp.seek(1)
		grbsDir.seek(1)
		
		for i in range(248):
			try:
				Hs = grbsHs.read(1)[0].values
				Tp = grbsTp.read(1)[0].values
				Dir = grbsDir.read(1)[0].values
			except (IndexError, IOError):
				continue
			
			outfile.write("%s\t" % t)
			for (lon,lat) in locations:
				idx, idy = idxat(lon,lat)
				outfile.write("%.2f\t%.2f\t%6.2f\t" % ( Hs[idx][idy], Tp[idx][idy], Dir[idx][idy]))
			outfile.write("\n") 
			
			t += dt
			
	end = time.time()

	print "Ellapsed time in seconds: ", end - st
	
	grbsHs.close()
	grbsTp.close()
	grbsDir.close()
	f.flush()


# main program
if len(sys.argv) < 4:
	print "Usage: python extract_waveVN.py yyyymm nmonths outfilename "
else:	
	yrmo = int(sys.argv[1])
	nmo = int(sys.argv[2])
	fname = sys.argv[3] + ".txt"

	f = open(fname,'w')
	process(yrmo, nmo, f)
	f.close()
