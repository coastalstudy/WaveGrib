#!/usr/bin/python

# use default Python, not Anaconda Python
# Python version 2.x

# Make sellist: a list of water location points in South China Sea

import pygrib
import sys
import numpy as np
import time
import datetime
from sealist_SCS import sealist

# Extent: 100E - 121E , 1N - 25N.
# Coding: AA - BQ, 00 - 48.
# Resolution 0.5 deg.
xlabels = []
for i in range(ord('A'), ord('Z')+1):
	xlabels.append('A' + chr(i))		# from 'AA' to 'AZ'
for i in range(ord('A'), ord('Q')+1):
	xlabels.append('B' + chr(i))		# from 'BA' to 'BQ'

ylabels = []
for i in range(49):
	ylabels.append('%02i' % i)		# format string with leading zero 00, 01, ..., 48.

xlocs = [100 + i*0.5 for i in range(43)]
ylocs = [1 + i*0.5 for i in range(49)]

lon_of_code = dict(zip(xlabels, xlocs))
lat_of_code = dict(zip(ylabels, ylocs))

typefloat64 = type(np.float64(1.))

def idxat(lon, lat):
	# convert lon/lat to index of array
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

		Returns
		-------
		None

		Side effects
		------------
		A text file created.
	"""	
	st = time.time()
	yr, mo = yrmo / 100, yrmo % 100 
	t = datetime.datetime(yr, mo, 1, 3, 0)
	dt = datetime.timedelta(hours=3)
	outfile.write("Date Time\t")
	for label in sealist:
		outfile.write("Hs{0}\tTp{0}\tDir{0}".format(label))
	outfile.write("\n")
	
	for j in range(nmo):
		num = yrmo + j  
		fileHs = 'multi_1.glo_30m.hs.%d.grb2' % num
		fileTp = 'multi_1.glo_30m.tp.%d.grb2' % num
		fileDir = 'multi_1.glo_30m.dp.%d.grb2' % num

		print num,
		
		grbsHs = pygrib.open(fileHs)
		grbsTp = pygrib.open(fileTp)
		grbsDir = pygrib.open(fileDir)

		grbsHs.seek(1)
		grbsTp.seek(1)
		grbsDir.seek(1)
		
		for i in range(248):
			try:
				HsMat = grbsHs.read(1)[0].values
				TpMat = grbsTp.read(1)[0].values
				DirMat = grbsDir.read(1)[0].values
			except (IndexError, IOError):
				continue
			
			outfile.write("%s\t" % t)
			
			for label in sealist:
				lon = lon_of_code[label[0:2]]
				lat = lat_of_code[label[2:4]]
				idx, idy = idxat(lon,lat)
				
				Hs = HsMat[idx][idy]
				Tp = TpMat[idx][idy]
				Dir = DirMat[idx][idy]
				
				if type(Hs)==typefloat64 and type(Tp)==typefloat64 and type(Dir)==typefloat64:
					outfile.write("%i\t%i\t%i\t" % (
										int(Hs * 100), 
										int(round(Tp,1) * 10), 
										int(Dir)  ) )
				else:
					outfile.write("9999\t9999\t9999\t")

			outfile.write("\n") 
			
			t += dt
			
	end = time.time()

	print "\nElapsed time in seconds: ", end - st
	
	grbsHs.close()
	grbsTp.close()
	grbsDir.close()
	f.flush()


# main program
if len(sys.argv) < 3:
	print "Usage: python extract_waveVN.py yyyymm nmonths"
else:
	yrmo = int(sys.argv[1])
	nmo = int(sys.argv[2])
	f = open('wave_East_Sea_{}.txt'.format(yrmo),'w')
	process(yrmo, nmo, f)
	f.close()
