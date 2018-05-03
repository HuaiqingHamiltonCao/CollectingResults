# This code is for collecting metalic ligation results from Findgeo.py

import os
import sys

filename = "FindGeo.summary"

fl1 = open(filename, "r")
line1 = fl1.readlines()
line1 = [x.strip() for x in line1]

# Define a dictionary including the configuration types and their ligation numbers



# Get the ion information and configuration type of each ion

ionname = []
configtype = []

for x in line1:
	y = x.split(' ')
	ionname.append(y[0][:-1])
	configtype.append(y[1])
#	print ionname
#	print configtype

# Visit the subfolder which name is the same as recorded in ionname list

for i in range(len(ionname)):
	outpath = ionname[i] + '/' + configtype[i] + '.out'
	outfl = open(outpath, "r")
	line2 = []
	line2 = outfl.readlines()
