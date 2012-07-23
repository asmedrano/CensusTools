#!/usr/bin/python

import csv
import sys
import re


STATES = {}
MUNIS = {}
TRACTS = {}
BLOCKGROUPS = {}

STATE_NAME = 'Rhode Island'

def read_geo_records(reader):
	for row in reader:
		geography = {}
		geography['sumlev'] = row[0][8:11]
		geography['name'] = get_name_from_row(row[0],geography['sumlev'])
		geography['logrecno'] = row[0][18:25]
		geography['parent_fip'] = get_parent_fips(row[0],geography['sumlev'])

		yield geography


def get_parent_fips(row,sumlev):
	""" Here we extract the parent fips_id based on what level we are wanting to find parent for"""
	if sumlev == '060':
		#munis
		return {'name':0,'logrecno':0}
	elif sumlev == '140':
		#TRACT returns County --- We would like County sub, but thats not available in the geo file.
		parent_fip = row[31:34]
		return parent_fip
	elif sumlev =='150':
		#block group, return tract
		parent_fip = row[55:61]
		return parent_fip

def find_geo_by_fips(reader,fips_id, target_sumlevel):
	""" Expects:csv reader object, target fips_id and the target level we should be searching for
		We'll have to interate the file again to accomplish this
	"""
	for row in reader:
		#1. Check to see if this row meets the criteria of our target_sumlevel
		if row[0][8:11] == target_sumlevel:
			#2. We should now be isolated to the right sum_level, we can now check to see if the fips_id is in this row.
			if check_for_fips(row[0], fips_id,target_sumlevel):
				
				return {'logrecno':row[0][18:25],'name':get_name_from_row(row[0],target_sumlevel)}

def get_name_from_row(row, sumlev):
	if sumlev=='040':
		return STATE_NAME
	elif sumlev =='050':
		p = re.compile(r'[a-zA-Z]+\sCounty')
		matches = p.findall(row)
	elif sumlev =='060':
		#muni level
		p = re.compile(r'([a-zA-Z]+\s?[a-zA-Z]+\s?)(?=city|town)')
		matches = p.findall(row)
		
	elif sumlev =='140':
		#tracts
		p = re.compile(r'Census\sTract\s[0-9.]+')
		matches = p.findall(row)

	elif sumlev =='150':
		#Block  Groups
		p = re.compile(r'Block\sGroup\s[0-9.]+')
		matches = p.findall(row)
	else:
		return 'None'
	if len(matches)!=0:
		return matches[0].strip()
	else:
		return 'Name Look up failed'

def check_for_fips(row,fips_id,sumlev):
	if sumlev == '050':
		fips = row[31:34]
		return fips_id == fips
	elif sumlev =='140':
		fips = row[55:61]
		return fips_id == fips

def sort_geographies(filename):
	f = open(filename, 'rt',)
	try:
		reader = csv.reader(f)
		for row in read_geo_records(reader):
			if row['sumlev'] == '040':
				STATES[row['logrecno']] = row
			elif row['sumlev'] =='060':
				MUNIS[row['logrecno']] = row
			elif row['sumlev'] =='140':
				TRACTS[row['logrecno']] = row
			elif row['sumlev'] =='150':
				BLOCKGROUPS[row['logrecno']] = row
		
		# We now have to grab all the parents by fips.
		for tract_id in TRACTS:
			f.seek(0)
			tract = TRACTS[tract_id]
			tract['parent'] = find_geo_by_fips(reader, tract['parent_fip'],'050') # this is the best we can do with tracts. We can only narrow down the tract parent to county and not county subdivision
		for bg_id in BLOCKGROUPS:
			f.seek(0)
			blkgrp = BLOCKGROUPS[bg_id]
			blkgrp['parent'] = find_geo_by_fips(reader, blkgrp['parent_fip'],'140') # looking for parent Tract 
		
	finally:
		f.close()





