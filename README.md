# CMPT353FinalProject

OSM data project

Testing.py can be run by: spark-submit testing.py amenities-vancouver.json.gz output

Just a test file that prints out all distinct amenities and has a few comments to how we can select certain tags for data processing.

To run the geolocating based on coordinates, need to install geopy which will allow us to go from coordinates to addresses. To find the representative point of each block section, we must also install shapely.

pip3 install geopy
pip3 install shapely
