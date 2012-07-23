#!/usr/bin/python
from acs_geo_file_reader import reader
import csv
import os

def main():
	reader.sort_geographies('census_src/g20105ri.csv')
	create_acs_tracts("asdf")
	
	 #print reader.STATES
	 #print reader.MUNIS
	 #print reader.TRACTS
	 #print reader.BLOCKGROUPS
	

def create_acs_tracts(geo_level):
    """ This method was added late by a second developer, so it doesnt nessesarily follow all the previously used patterns"""

    #lets read the Xwalk File
    try:
        f = open('TRACT_COUNTYSUBDIV_2010_XWALK.csv')
        xwalkreader = csv.reader(f)
        xwalkreader.next()
        for row in xwalkreader:
			tract_logrecno = row[4]
			parent_logrecno = row[7]
			#some values are blank
			if tract_logrecno is not '' and parent_logrecno is not '':
				print "---------------------------------------------"
				print "Tract"
				print reader.TRACTS[tract_logrecno]
				print "Parent"
				print reader.MUNIS[parent_logrecno]

			
    finally:
        f.close()


if __name__ == '__main__':
	main()
