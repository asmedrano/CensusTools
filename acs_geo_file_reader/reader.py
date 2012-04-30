import csv
import sys
import re


"""
Summary Level Definitions
Defined as:
SUMLEV: (Geographies, Hierarchy)
"""
SUMLEV = {
	'010':('United States', 'United States',),
	'020':('Region',),
	'030':('Division',),
	'040':('State','State',),
	'050':('County','State-County',),
	'060':('County Subdivision', 'State-County-County-Subdivision',),
	'067':('Subminor Civil Division','State-County-County Subdivision-Subminor Civil Division',),
	'070':('Place/Remainder', 'State-County-County Subdivision-Place/Remainder',),
	'080':('Census Tract','State-County-County Subdivision-Place/Remainder-Census Tract',),
	'140':('State-County-Census Tract',),
	'150':('State-County-Census Tract-Block Group',),
	'155':('State-Place-County',),
	'160':('State-Place',),
	'170':('State-Consolidated City',),
	'172':('State-Consolidated City-Place Within Consolidated City',),
	'230':('State-Alaska Native Regional Corporation',),
	'250':('American Indian Area/Alaska Native Area/Hawaiian Home Land',),
	'251':('American Indian Area-Tribal Subdivision/Remainder',),
	'252':('American Indian Area/Alaska Native Area (Reservation or Statistical Entity Only) US', ' All Geos Xcpt T&BG', '',),
	'254':('American Indian Area (Off-Reservation Trust Land Only)/Hawaiian Home Land',),
	'256':('American Indian Area-Tribal Census Tract',),
	'258':('American Indian Area-Tribal Census Tract-Tribal Block Group',),
	'260':('American Indian Area/Alaska Native Area/Hawaiian Home Land-State',),
	'269':('American Indian Area/Alaska Native Area/Hawaiian Home Land-State- Place/Remainder',),
	'270':('American Indian Area/Alaska Native Area/Hawaiian Home Land-State-County',),
	'280':('State-American Indian Area/Alaska Native Area/Hawaiian Home Land',),
	'283':('State-American Indian Area/Alaska Native Area (Reservation or Statistical Entity Only)',),
	'286':('State-American Indian Area (Off-Reservation Trust Land Only)/Hawaiian Home Land State', ' All Geos Xcpt T&BG', '',),
	'290':('American Indian Area-Tribal Subdivision/Remainder-State',),
	'291':('American Indian Area (Reservation Only)-Tribal Census Tract',),
	'292':('American Indian Area (Off-Reservation Trust Land Only)-Tribal Census Tract',),
	'293':('American Indian Area (Reservation Only)-Tribal Census Tract-Tribal Block Group',),
	'294':('American Indian Area (Off-Reservation Trust Land Only)-Tribal Census Tract-Tribal Block Group',),
	'310':('Metropolitan Statistical Area/Micropolitan Statistical Area',),
	'311':('Metropolitan Statistical Area/Micropolitan Statistical Area-State',),
	'312':('Metropolitan Statistical Area/Micropolitan Statistical Area-State-Principal City',),
	'313':('Metropolitan Statistical Area/Micropolitan Statistical Area-State-County',),
	'314':('Metropolitan Statistical Area-Metropolitan Division',),
	'315':('Metropolitan Statistical Area-Metropolitan Division-State',),
	'316':('Metropolitan Statistical Area-Metropolitan Division-State-County',),
	'320':('State-Metropolitan Statistical Area/Micropolitan Statistical Area',),
	'321':('State-Metropolitan Statistical Area/Micropolitan Statistical Area-Principal City',),
	'322':('State-Metropolitan Statistical Area/Micropolitan Statistical Area-County',),
	'323':('State-Metropolitan Statistical Area-Metropolitan Division',),
	'324':('State-Metropolitan Statistical Area-Metropolitan Division-County',),
	'330':('Combined Statistical Area',),
	'331':('Combined Statistical Area-State',),
	'332':('Combined Statistical Area-Metropolitan Statistical Area/Micropolitan Statistical Area',),
	'333':('Combined Statistical Area-Metropolitan Statistical Area/Micropolitan Statistical Area-State',),
	'335':('Combined New England City and Town Area',),
	'336':('Combined New England City and Town Area-State',),
	'337':('Combined New England City and Town Area-New England City and Town Area',),
	'338':('Combined New England City and Town Area-New England City and Town Area-State',),
	'340':('State-Combined Statistical Area',),
	'341':('State-Combined Statistical Area-Metropolitan Statistical Area/Micropolitan Statistical Area',),
	'345':('State-Combined New England City and Town Area',),
	'346':('State-Combined New England City and Town Area-New England City and Town Area',),
	'350':('New England City and Town Area',),
	'351':('New England City and Town Area-State',),
	'352':('New England City and Town Area-State-Principal City',),
	'353':('New England City and Town Area-State-County',),
	'354':('New England City and Town Area-State-County-County Subdivision',),
	'355':('New England City and Town Area (NECTA)-NECTA Division',),
	'356':('New England City and Town Area (NECTA)-NECTA Division-State',),
	'357':('New England City and Town Area (NECTA)-NECTA Division-State-County',),
	'358':('New England City and Town Area (NECTA)-NECTA Division-State-County-County Subdivision',),
	'360':('State-New England City and Town Area',),
	'361':('State-New England City and Town Area-Principal City',),
	'362':('State-New England City and Town Area-County',),
	'363':('State-New England City and Town Area-County-County Subdivision',),
	'364':('State-New England City and Town Area (NECTA)-NECTA Division',),
	'365':('State-New England City and Town Area (NECTA)-NECTA Division-County',),
	'366':('State-New England City and Town Area (NECTA)-NECTA Division-County-County Subdivision',),
	'400':('Urban Area',),
	'500':('State-Congressional District',),
	'510':('State-Congressional District-County',),
	'550':('State-Congressional District-American Indian Area/Hawaiian Home Land',),
	'610':('State-State Legislative District (Upper Chamber)',),
	'612':('State-State Legislative District (Upper Chamber)-County',),
	'620':('State-State Legislative District (Lower Chamber)',),
	'622':('State-State Legislative District (Lower Chamber)-County',),
	'795':('State-Public Use Microdata Sample Area (PUMA)',),
	'950':('State-School District (Elementary)/Remainder',),
	'960':('State-School District (Secondary)/Remainder',),
	'970':('State-School District (Unified)/Remainder',),


}


"""
Dicts of Geographies. Dict Keys = Names as defined by Census ex:"Kent County, Rhode Island"
STATES, SUMLEV 040.
MUNIS, SUMLEV 060
TRACTS, SUMLEV 140
BLOCKGROUPS, SUMLEV 150
"""
STATES = {}
MUNIS = {}
TRACTS = {}
BLOCKGROUPS = {}


def read_geo_records(reader):
	"""
		row[49] EX: 'West Warwick town, Kent County, Rhode Island'
	"""
	
	for row in reader:
		geography = {}
		geography['sumlev'] = row[2]
		geography['sumlev_name'] = SUMLEV[row[2]][0]
		geography['logrecno'] = row[4]
		geography['geo_census_name'] = row[49]
		geography['geo_name'] = clean_geo_name(row[49])
		geography['geo_parent'] = get_parent(row[49], row[2])
		yield geography




def clean_geo_name(geography_census_name):
	""" Cleans up things like East Providence city, Providence County, Rhode Island. 
		Returns East Providence
	"""
	p = re.compile('(city|town)')
	return p.sub('',geography_census_name.split(",")[0]).strip()



def get_parent(geography_census_name, sumlev):

	""" 
		Returns the parent geography name of this geography
		Expects:
		geography_census_name: EX: East Providence city, Providence County, Rhode Island (as provided by Census)
		sumlev EX: 060

		NOTE: In our case we call County Subdivision's "Municipalities". We say municipalities' parent is the 
		State --- > {'sumlev': '040', 'logrecno': '0000001', 'geo_census_name': 'Rhode Island', 'geo_name': 'Rhode Island', 'sumlev_name': 'State'}
		but in reality it should be a County. That being said, we have to account for that.

	"""
	if sumlev == '060':
		#munis
		return 'Rhode Island'
	elif sumlev == '140':
		#TRACT
		return "Place Holder"
	elif sumlev =='150':
		#blockgroup 
		parent = geography_census_name.split(',')[1]
		return parent


def sort_geographies(filename):
	f = open(filename, 'rt',)
	try:
		reader = csv.reader(f)
		for row in read_geo_records(reader):
			# place in dictionaries
			if row['sumlev'] == '040':
				STATES[row['geo_census_name']] = row
			elif row['sumlev'] =='060':
				MUNIS[row['geo_census_name']] = row
			elif row['sumlev'] =='140':
				TRACTS[row['geo_census_name']] = row
			elif row['sumlev'] =='150':
				BLOCKGROUPS[row['geo_census_name']] = row

	finally:
		f.close()







