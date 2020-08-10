# CMPT353FinalProject

OSM data project

Files and how to run them:

-01-clean_block_outlines.py can be run by: spark-submit 01-clean_block_outlines.py block-outlines.json output : Was used to create the directory cleanedBlocks. This outputs a dataframe with 4 locations coordesponding to the four corners of a Vancouver block, as well as a coordinate point which is between the four corner locations.

-02-block_data_coalesce_zip.py can be run by: spark-submit 02-block_data_coalesce_zip.py cleanedBlocks output : was used to create the directory CoalescedBlocks. From this directory, we moved out the single file, and renamed it to be VancouverBlocks.json.gz

-03-filtering_groups.py can be run by: python3 03-filtering_groups.py : creates all the relevant dataframes from the original file amenities-vancouver.json.gz. Outputs all the dataframes used into a new folder called raw_amenities_dataframes.

-04-create_distance_dataframes.py can be run by: python3 04-create_distance_dataframes.py : This takes the raw_amenities_dataframes from the last step and all the VancouverBlocks.json.gz data, and adds new columns to that dataframe. One new column for the minimum distance from each coordinate point to each relevant amenity for each purchasing value.

05-plot_data.py can be run by: python3 05-plot_data.py : outputs the maps showing where the points are.

-06-append_zscores.py can be run by: python3 06-append_zscores.py : This program takes the dataframes created from 04-create_distance_dataframes.py, which have the 4 locations, the representative point coordinate and the minimum distance from each coordinate to each relatant entity. The program then calculates the z-score for each amenity column to create a ranking for the distances. It creates a new column for each amenity with the z-scores, and then creates one additional column with the sum of the z-scores for every coordinate. Outputs this data into the directory Vancouver_blocks_zscores.

-07-driver_program.py can be run by: python3 07-driver_program.py : This is the driver program which takes inputs from the user, and outputs the optimal location to look for real estate.

Required libraries commands:

pip3 install geopy
pip3 install shapely
pip3 install geopandas

amenities notes:

-main transportation (car, public, biking):
car sharing
bicycle repair
car rental
bus station
car sharing
fuel
parking space

-Nightlife:
pub/bar
restaurant
nightclub
strip club
gambling
casino
lounge
smoking area
events venue

-Outdoor/fitness:
gyms
parks
training
community centre

-activities:
theatre
restaurant
cinema
parks
events venue
observation platform

-leisure
lounge
cafe
spa
meditiation centre
library

-family life:
school
kindergarden
family centre
music school
playground
park
marketplace
childcare
library

-pet owner
vet
parks

-safety:
hospital
police
fire station
doctors
healthcare
