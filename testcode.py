# This code is for collecting metalic ligation results from Findgeo.py

import os
import sys
import re

filename = "FindGeo.summary"

fl1 = open(filename, "r")
line1 = fl1.readlines()
line1 = [x.strip() for x in line1]

# Define a dictionary including the configuration types and their ligation numbers

lignum = {
	'lin': 2, # Linear
	'trv': 2, # Trigonal plane with a vacancy
	'tri': 3, # Trigonal plane
	'tev': 3, # Tetrahedron with a vacancy
	'spv': 3, # Square plane with a vacancy
	'tet': 4, # Tetrahedron
	'spl': 4, # Square plane
	'bva': 4, # Trigonal bipyramid with a vacancy (axial)
	'bvp': 4, # Trigonal bipyramid with a vacancy (equatorial)
	'pyv': 4, # Square pyramid with a vacancy (equatorial)
	'spy'; 5, # Square pyramid
	'tbp': 5, # Trigonal bipyramid
	'tpv': 5, # Trigonal prism with a vacancy
	'oct': 6, # Octahedron
	'tpr': 6, # Trigonal prism
	'pva': 6, # Pentagonal bipyramid with a vacancy (axial)
	'pvp': 6, # Pentagonal bipyramid with a vacancy (equatorial)
	'cof': 6, # Octahedron, face monocapped with a vacancy (capped face)
	'con': 6, # Octahedron, face monocapped with a vacancy (non-capped face)
	'ctf': 6, # Trigonal prism, square-face monocapped with a vacancy (capped face)
	'ctn': 6, # Trigonal prism, square-face monocapped with a vacancy (capped face)
	'pbp': 7, # Pentagonal bipyramid
	'coc': 7, # Octahedron, face monocapped
	'ctp': 7, # Trigonal prism, square-face monocapped
	'hva': 7, # Hexagonal bipyramid with a vacancy (axial)
	'hvp': 7, # Hexagonal bipyramid with a vacancy (equatorial)
	'cuv': 7, # Cube with a vacancy
	'sav': 7, # Square antiprism with a vacancy
	'hbp': 8, # Hexagonal bipyramid
	'cub': 8, # Cube
	'sqa': 8, # Square antiprism
	'boc': 8, # Octahedron, trans-bicapped
	'bts': 8, # Trigonal prism, square-face bicapped
	'btt': 8, # Trigonal prism, triangular-face bicapped
	'ttp': 9, # Trigonal prism, square-face tricapped
	'csa': 9  # Square antiprism, square-face monocapped
}

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
	i1 = ionname[i]
	c1 = configtype[i]

# Results without a best geometry will be recorded as 'irr'. When coming with an 'irr' result, we just skip it.
	if c1 not in ('irr'):
		outpath = i1 + '/' + c1 + '.out'
		outfl = open(outpath, "r")

# line2 contains the fulltext of target configuration output file. Next the coordinates of template with ideal geometry and coordinates of the fitted metal site will be extracted.
		line2 = []
		line2 = outfl.readlines()

# line3 will contain the extracted coordinates of the ideal template
# The first three lines of the fulltext will be obmitted
		line3 = []
		lnum = lignum[c1]
		for i in range(lnum):
			coor = line2[3+i].strip().split(' ')
			coor = [ e for e in coor if e not in (' ') ]
			coor = [ float(e) for e in coor ]
			line3.append(coor)

# line4 will contain the fitted coordinates and RMSD
# The coming three lines will be obmitted also
		line4 = []
		for i in range(lnum):
			coor2 = line2[6+lnum+i].strip().split(' ')
			coor2 = [ e for e in coor if e not in (' ') ]
			coor2 = [ float(e) for e in coor ]
			line4.append(coor2)

# tR will contain the total RMSD
		tRlnum = 2 * ( 3 + lnum )
		coor3 = line2[tRlnum+1].strip().split(' ')
		coor3 = re.findall("\d+\.\d+", coor3)
		tR = float(coor3[0])

	else:
		# Something to be done with the skipped results
		print "skipped"

# All data in configtype.out has been recorded in line3 and line4. 
