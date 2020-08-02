# CMPT353FinalProject

OSM data project

Testing.py can be run by: spark-submit testing.py amenities-vancouver.json.gz output

Just a test file that prints out all distinct amenities and has a few comments to how we can select certain tags for data processing.

To run the geolocating based on coordinates, need to install geopy which will allow us to go from coordinates to addresses. To find the representative point of each block section, we must also install shapely.

pip3 install geopy
pip3 install shapely

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
