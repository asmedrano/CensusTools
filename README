#Some Tools for working with Census related Items
#### This mainly is for my use so its not all packaged nicely. Maybe a better starting point than an actually use full package.


### acs_geo_file_reader
Helps you work with this type of geography file: http://www2.census.gov/acs2010_5yr/summaryfile/2006-2010_ACSSF_By_State_By_Sequence_Table_Subset/RhodeIsland/Tracts_Block_Groups_Only/g20105ri.csv

##### Example Usage

```python
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
```