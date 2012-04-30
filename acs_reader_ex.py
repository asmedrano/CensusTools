#!/usr/bin/python
from acs_geo_file_reader import reader



def main():
	 reader.sort_geographies('census_src/g20105ri.csv')

	 print reader.STATES
	 print reader.MUNIS
	 print reader.TRACTS
	 print reader.BLOCKGROUPS


if __name__ == '__main__':
	main()