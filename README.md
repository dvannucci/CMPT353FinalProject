# CMPT353FinalProject

OSM data project

Files and how to run them:

-01-clean_block_outlines.py can be run by: spark-submit 01-clean_block_outlines.py block-outlines.json output : Was used to create the directory cleanedBlocks.

-02-block_data_coalesce_zip.py can be run by: spark-submit 02-block_data_coalesce_zip.py cleanedBlocks output : was used to create the directory CoalescedBlocks.

-03-filtering_groups.py can be run by: python3 03-filtering_groups.py : creates all the relevant dataframes

05-plot_data.py can be run by: python3 05-plot_data.py : outputs the maps showing where the points are.

Required Packages:

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
