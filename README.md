# CMPT353FinalProject

OSM data project

Files and how to run them:

-01-CleanBlockOutlines.py can be run by: spark-submit 01-CleanBlockOutlines.py block-outlines.json output : Was used to create the directory cleanedBlocks.

02-blockDataCoalesceZip.py can be run by: spark-submit 02-blockDataCoalesceZip.py cleanedBlocks output : was used to create the directory CoalescedBlocks.

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
