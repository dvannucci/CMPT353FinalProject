# CMPT353FinalProject
# Group: osm
# Daniel Vannucci (301291575)
# Benson Ou-Yang ()

Required libraries commands:

pip3 install geopy
pip3 install shapely
pip3 install geopandas

Files and how to run them:

-01-clean_block_outlines.py can be run by: spark-submit 01-clean_block_outlines.py block-outlines.json cleanedBlocks : Was used to create the directory cleanedBlocks. This takes the raw block data and outputs a data frame with each row containing 4 location addresses corresponding to the four corners of a Vancouver block, as well as a representative coordinate point which is within the block outline.

-02-block_data_coalesce_zip.py can be run by: spark-submit 02-block_data_coalesce_zip.py cleanedBlocks CoalescedBlocks : was used to create the directory CoalescedBlocks. This program coalesced the cleanedBlocks directory of 200 files into one (explanation why that was safe is in the file). From this created directory, we moved out the single file, and renamed it to be VancouverBlocks.json.gz

-03-filtering_groups.py can be run by: python3 03-filtering_groups.py : creates a new data frame for each value (nightlife, fitness etc.) with the appropriate amenities from the original file amenities-vancouver.json.gz. Outputs all the data frames created into a new folder called raw_amenities_dataframes.

-04-create_distance_dataframes.py can be run by: python3 04-create_distance_dataframes.py : This takes the raw_amenities_dataframes from the last step and all the VancouverBlocks.json.gz data as inputs. This program adds new columns to the VancouverBlocks data frame and outputs all the data frames into a new directory Vancouver_blocks_amenity_dataframes. One new column per amenity is added to the VancouverBlocks data frames, each column holding the minimum distance from each coordinate point to each relevant amenity. For example with the fitness dataframe,
   coordinate    |  gym_distance  |  community_centre_distance  |  ...
 [49.1, -123.2]       1900.22               1633.33
The column gym_distance would be the distance from the coordinate [49.1, -123.2] to nearest gym.

-05-rental_prices_dataframe.py can be run by: python3 05-rental_prices_dataframe.py : This takes the file rental_prices_manual.csv, and creates a data frame with all points from the VancouverBlocks data with a new column for rental price's z-scores. This is created by taking each coordinate point and mapping it to a Vancouver neighborhood to give an average apartment rental price. These prices are then converted to a z-score and outputted with the original data into the new folder Vancouver_blocks_zscores.

-06-append_zscores.py can be run by: python3 06-append_zscores.py : This program takes the data frames created from 04-create_distance_data frames.py, which have the 4 locations, the representative point coordinate and the minimum distance from each coordinate to each relevant entity. The program then calculates the z-score for each amenity column to create a ranking for the distances. It creates a new column for each amenity with the z-scores, and then creates one additional column with the sum of the z-scores for every coordinate. It then outputs this data into the directory Vancouver_blocks_zscores.

-07-driver_program.py can be run by: python3 07-driver_program.py : This is the driver program which takes inputs from the user, calculates the optimal real estate location based on the user's preferences, and outputs this data along with a map of the location.

08-plot_data.py can be run by: python3 08-plot_data.py : outputs the maps showing where the locations are.

Each values relevant amenities:

-main transportation:
car:
fuel
parking_space
car_wash

public:
bus_station
car_sharing
car_rental
bicycle_rental

bike:
bus_station
car_sharing
car_rental
bicycle_rental
bicycle_parking
bicycle_repair_station

-Nightlife:
pub
bar
restaurant
nightclub
stripclub
gambling
casino
lounge
smoking_area
events_venue

-fitness:
gym
park
training
community_centre

-activities:
theatre
restaurant
cinema
park
events_venue
Observation Platform

-leisure
lounge
cafe
spa
meditation_centre
library
leisure

-family life:
school
kindergarten
family_centre
music_school
playground
park
marketplace
childcare
library

-pet owner
veterinary
park

-safety:
hospital
police
fire_station
doctors
healthcare
clinic
