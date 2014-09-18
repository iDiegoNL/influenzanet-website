#!/usr/bin/env python
import datetime
import string
from pychart import chart_data
import sys
output_png_dir = './output/'

data_incidence = []
count = 0
f = open(sys.argv[1])
for line in f.readlines():
   fields = string.split(line[:-1], ',')
   if len(fields) < 2:
	continue
   count += 1
   data_incidence.append( (count, int(fields[2]), int(fields[1]), fields[0] ) )
   
f.close


data_mav_active = chart_data.moving_average(data_incidence, 0, 2, 7)
data_mav_ill = chart_data.moving_average(data_incidence, 0, 1, 7)

data_incidence = [(x[0], y[1], z[1], x[3]) for
                 x,y,z in zip(data_incidence, data_mav_ill, data_mav_active)]

#print data_incidence
fz = lambda x: (x[0], x[1]/x[2]*1000., x[3])
data_incidence =  chart_data.transform(fz, data_incidence)

#print data_incidence
for u in data_incidence:
   print u[2], u[1]


