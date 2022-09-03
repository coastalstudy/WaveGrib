# Extract ocean wave data series offshore Vietnam 
# from GRIB files (NOAA/ECMWF).

# Update to Python 3 (Anaconda)

# Make sellist: a list of water location points in South China Sea

import os
import sys
import time
import pygrib
import datetime
import numpy as np
from samples_SCS import sample_list


DATA_DIR = '../downloads/'  # relative path to *.grib2 file folder


# Zone Extent: 100E - 121E , 1N - 25N.
# Encoding: AA - BQ, 00 - 48.
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

typefloat64 = type(np.float64(1.))


def idxat(lon, lat):
    ''' Converting from `lon`, `lat` to indices 
        of the data matrix.

        Parameters
        ----------
        `lon`: `int`, Longitude
        `lat`: `int`, Latitude
        
        Returns
        -------
        A tuple of indices
        `idx`: `int`, row of data matrix
        `idy`: `int`, column of data matrix
    '''
    MAX_LAT = 77.5
    N_SAMPLES_PER_DEG = 2	# 2 samples/deg, aka "resolution"
    idx = int(round((MAX_LAT - lat) * N_SAMPLES_PER_DEG))
    idy = int(round(lon * N_SAMPLES_PER_DEG))
    return idx, idy


def process(yrmo, nmo, outfile, sample_list):
    """ Process the wave data, reading grib files and 
        extract the wave time series of corresponding 
        points in the sample list.

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
        An output text file created.
    """	
    st = time.time()
    yr, mo = yrmo // 100, yrmo % 100 
    t = datetime.datetime(yr, mo, 1, 3, 0)
    dt = datetime.timedelta(hours=3)
    outfile.write("Date Time\t")
    for label in sample_list:
        outfile.write("Hs{0}\tTp{0}\tDir{0}".format(label))
    outfile.write("\n")
    
    for j in range(nmo):
        num = yrmo + j  
        fileHs = 'multi_1.glo_30m.hs.%d.grb2' % num
        fileTp = 'multi_1.glo_30m.tp.%d.grb2' % num
        fileDir = 'multi_1.glo_30m.dp.%d.grb2' % num

        print(num, end='')
        
        with pygrib.open(os.path.join(DATA_DIR, fileHs)) as grbsHs, \
            pygrib.open(os.path.join(DATA_DIR, fileTp)) as grbsTp, \
            pygrib.open(os.path.join(DATA_DIR, fileDir)) as grbsDir:

            grbsHs.seek(1)
            grbsTp.seek(1)
            grbsDir.seek(1)
            
            for _ in range(248):
                try:
                    HsMat = grbsHs.read(1)[0].values
                    TpMat = grbsTp.read(1)[0].values
                    DirMat = grbsDir.read(1)[0].values
                except (IndexError, IOError):
                    continue  # tolerate bad data, on to next
                
                outfile.write("%s\t" % t)
                
                for label in sample_list:
                    lon = lon_of_code[label[0:2]]
                    lat = lat_of_code[label[2:4]]
                    idx, idy = idxat(lon,lat)
                    
                    Hs = HsMat[idx][idy]
                    Tp = TpMat[idx][idy]
                    Dir = DirMat[idx][idy]
                    
                    if type(Hs) == type(Tp) == type(Dir) == typefloat64:
                        outfile.write("%i\t%i\t%i\t" % (
                                        int(Hs * 100), 
                                        int(round(Tp,1) * 10), 
                                        int(Dir)  ) )
                    else:
                        outfile.write("9999\t9999\t9999\t")

                outfile.write("\n") 
                
                t += dt
            
    end = time.time()

    print("\nElapsed time in seconds: ", end - st)
    
    f.flush()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: $ python extract_wave_data_zone.py zone_name yyyymm n_months")
    else:
        zone_name = sys.argv[1]
        yrmo = int(sys.argv[2])
        nmo = int(sys.argv[3])
        with open('wave_zone_{}_{}.txt'.format(zone_name, yrmo),'w') as f:
            process(yrmo, nmo, f, sample_list)
