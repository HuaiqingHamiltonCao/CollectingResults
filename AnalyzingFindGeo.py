# This code is for collecting metalic ligation results from Findgeo.py
from __future__ import division
import os
import sys
import re

from math import *

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
	'spy': 5, # Square pyramid
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


# Prepare to save the information into dictionaries
dicthome = {}


# Read the subfolder list in each metalic ion's folder
# Folder name will be changed if another ion will be tested
folderlist = "/media/caohq/DATA/Work/PDB/metalic_ion_ligand/FE/testfolder.txt"
fd1 = open(folderlist, "r")
line0 = fd1.readlines()
line0 = [x.strip() for x in line0]


# For each element in folderlist, the following code will collect the FindGeo result and analyze it.

for x in line0:

# Test the program
#	print x

	element = x

# Read the summary output file
	filename = element + "/" + "FindGeo.summary"

# Test the program
	print filename

	fl1 = open(filename, "r")
	line1 = []
	line1 = fl1.readlines()
	line1 = [a.strip() for a in line1]

# Test the program
#	print line1

# Get the ion name and configuration type for each ion
	ionname = []
	configtype = []

# Read the FindGeo.summary file
	for a in line1:
		y = a.split(' ')
		ionname.append(y[0][:-1])
		configtype.append(y[1])
		print "%s, %s, %s" % ("   ", y[0][:-1], y[1])

# Visit the subfolder which name i the same as recorded in ionname list

	for j in range(len(ionname)):
		i1 = ionname[j]
		c1 = configtype[j]
# Test the program
#		print "%s, %s, %s" % ("        ", i1, c1)

# Ready to create the main dictionary
		dicname = (i1)
		dicthome[dicname] = {'pdbid': element, 'filename': 'None', 'averageDistance': 0.0, 'totalRMSD': 0.0, 'configuration': c1, 'atoms': {}}
# What will be contained in dictatoms:
#     AtomNumber, AtomType, ResType, ChainID, ResNumber: From dictpdb
#     x, y, z, RMSD: From dictfitted


# Results without a best geometry will be recorded as 'irr'. When coming with an 'irr' result, we just skip it.
		if c1 not in ('irr'):
			outpath = element + '/' + i1 + '/' + c1 + '.out'
# Test the program
#			print outpath
			dicthome[dicname]['filename'] = outpath
			outfl = open(outpath, "r")


# Next we will read the *.pdb file to extract the ion information and ligation atoms information
			outpdb = element + '/' + i1 + '/' + c1 + '.pdb'
			opfl = open(outpdb, "r")

# line5 will contain the pdb coordinations
			line5 = []
			line5 = opfl.readlines()

# Only the second part is useful. It contains the coordination of ion and ligation atoms.
# Di5a will contain the coordination and the important information will extracted in to dictionary
# line2 contains the fulltext of target configuration output file. Next the coordinates of template with ideal geometry and coordinates of the fitted metal site will be extracted.

# Di3 will contain the extracted coordinates of the ideal template
# The first three lines of the fulltext will be obmitted
# Dictionary is made to contain the coordinate

# Di4 will contain the fitted coordinates and RMSD
# The coming three lines will be obmitted also
# Dictionary is made to contain the coordinate
			lnum = lignum[c1]
			label = -1 - lnum
			line2 = []
			line2 = outfl.readlines()

# Initiate the variant for calculating the average distance
			averdis = 0.0

# Test the program
#			print "%s, %d" % ("lnum =", lnum)

			for i in range(lnum+1):
				k = i + label

# Test the program
#				print "%d, %d" % (i, k)

# Formatted string decomposition is required
#				l5 = line5[k].strip().split(' ')
#				l5 = [ x for x in l5 if x not in (' ')]

# The atom number is taken from the 5th to 11th letter of the line: 
				ant1 = line5[k][5:11].strip()
				an1 = int(ant1)
# The atom type is taken from the 12th to 16th letter of the line:
				at1 = line5[k][11:16].strip()
# The residue type is taken from the 17th to 20th letter of the line:
				rt1 = line5[k][16:20].strip()
# The chain id is taken from the 21st and 22nd letters of the line:
				cid1 = line5[k][20:22].strip()
# The residue number is taken from the 23rd to 26th letter of the line:
				rn1 = int(line5[k][22:26])

# Test the program
#				print "%s, %d, %s, %s, %s, %d" % ("****", an1, at1, rt1, cid1, rn1)

				di5a = dict(AtomNumber=an1, AtomType=at1, ResType=rt1, ChainID=cid1, ResNumber=rn1)
				name5a = ( rt1 + '_' + ant1 )

# Test the program
#				print "%s, %s" % ("****", name5a)
		
				coor = line2[3+i].strip().split(' ')
				coor = [ e for e in coor if e not in (' ') ]
				coor = [ float(e) for e in coor ]

# Calculate the average distance between ion and ligation atoms
				if i == 0:
					x0 = coor[0]
					y0 = coor[1]
					z0 = coor[2]
				else:
					x1 = float(coor[0] - x0)
					y1 = float(coor[1] - y0)
					z1 = float(coor[2] - z0)
					aver1 = x1**2 + y1**2 + z1**2
					averdis += sqrt(aver1)
					print "%d, %d, %d" % (x1, y1, z1)
					print "%d, %d" % (aver1, averdis)

				coor2 = line2[7+lnum+i].strip().split(' ')
				coor2 = [ e for e in coor2 if e not in (' ') ]
				coor2 = [ float(e) for e in coor2 ]
				di4 = dict(x=coor2[0], y=coor2[1], z=coor2[2], RMSD=coor2[3])

				dicthome[dicname]['atoms'][name5a] = di5a
				dicthome[dicname]['atoms'][name5a].update(di4)

# tR will contain the total RMSD
			tRlnum = 2 * ( 4 + lnum )
			coor3 = line2[tRlnum+1].strip().split(' ')
			tR = float(coor3[-1])
			dicthome[dicname]['totalRMSD'] = tR

# Update dictionary with the average distance
			print "%d, %d" % (averdis, lnum)
			averdis /= float(lnum)
			dicthome[dicname]['averageDistance'] = averdis
			print "%d, %d" % (averdis, lnum)

# Test the program
#			print name5a
#			print dictatoms[name5a]
#			print dicthome[dicname]['averageDistance']


# If the 'irr' is read, it means that no regular configuration is found.
		else:
# Something to be done with the skipped results
			print "No regular configuration. Skipped"


# Test the program
# print dicthome


# After the data has been completely recorded in the main dictionary 'dicthome', following analysis will come.
# Frequencies of residues for all the ions will be calculated.
FreqRes = {}
for key in dicthome:
	for k1 in dicthome[key]['atoms']:
		dd1 = dicthome[key]['atoms'][k1]
		res1 = dd1['ResType']
		if res1 not in FreqRes:
			FreqRes[res1] = 1
		else:
			FreqRes[res1] += 1
#		print "%s, %s, %s, %s, %d, %d" % (key, dicthome[key]['filename'], dicthome[key]['pdbid'], res1, FreqRes[res1], dd1['AtomNumber'])

rfq = open("ResidueFrequency.txt", "w")
for key in FreqRes:
	printline = key + " : " + str(FreqRes[key]) + "\n"
	rfq.write(printline)


# Frequencies of configurations will be calculated.
FreqCog = {}
for key in dicthome:
	cfg1 = dicthome[key]['configuration']
	if cfg1 not in FreqCog:
		FreqCog[cfg1] = 1
	else:
		FreqCog[cfg1] += 1
#	print "%s, %s, %d" % (key, cfg1, FreqRes[cfg1])

cfq = open("ConfigurationFrequency.txt", "w")
for key in FreqCog:
	printline = key + " : " + str(FreqCog[key]) + "\n"
	cfq.write(printline)


# For one ion, the ligation residues will be analyzed.
IonWithRes = {}
for key in dicthome:
	ion1 = key[:2].strip()
	if ion1 not in IonWithRes:
		IonWithRes[ion1] = {}
	for k1 in dicthome[key]['atoms']:
		de1 = dicthome[key]['atoms'][k1]
		res1 = de1['ResType']
		if res1 not in IonWithRes[ion1]:
			IonWithRes[ion1][res1] = 1
		else:
			IonWithRes[ion1][res1] += 1

iwr = open("Ion-ResidueFrequency.txt", "w")
for key in IonWithRes:
	printkey = key + "\n"
	iwr.write(printkey)
	for k1 in IonWithRes[key]:
		printline = k1 + " : " + str(IonWithRes[key][k1]) + "\n"
		iwr.write(printline)
	iwr.write("\n")


# For one ion, the ligation atoms will be analyzed.
IonWithAtom = {}
for key in dicthome:
	ion1 = key[:2].strip()
	if ion1 not in IonWithAtom:
		IonWithAtom[ion1] = {}
	for k1 in dicthome[key]['atoms']:
		de1 = dicthome[key]['atoms'][k1]
		res1 = de1['AtomType']
		if res1 not in IonWithAtom[ion1]:
			IonWithAtom[ion1][res1] = 1
		else:
			IonWithAtom[ion1][res1] += 1

iar = open("AtomFrequency.txt", "w")
for key in IonWithAtom:
	printkey = key + "\n"
	iar.write(printkey)
	for k1 in IonWithAtom[key]:
		printline = k1 + " : " + str(IonWithAtom[key][k1]) + "\n"
		iar.write(printline)
	iar.write("\n")


# For one ion, the average distance between it and ligation atoms will be calculated.
# IonDis = {}
# ids = open("Distance.txt", "w")
# for key in dicthome:
#	adis = dicthome[key]['averageDistance']
#	ion2 = key[:2].strip()
#	if ion2 not in IonDis:
#		IonDis[ion2] = {"counter": 0.0, "averDis": 0.0}
#	else:
#		IonDis[ion2]["counter"] += 1
#		IonDis[ion2]["averDis"] += adis
#	print >> ids, "%s, %s, %d, %d" % (key, ion2, IonDis[ion2]["counter"], IonDis[ion2]["averDis"])

# for key in IonDis:
#	if IonDis[key]["counter"] != 0:
#		IonDis[key]["averDis"] /= IonDis[key]["counter"]
#	else:
#		IonDis[key]["averDis"] = -1
#	print >> ids, "%s, %d, %d" % (key, IonDis[key]["counter"], IonDis[key]["averDis"])
