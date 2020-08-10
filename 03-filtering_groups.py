import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from sklearn.cluster import KMeans

def main():
    data = pd.read_json('amenities-vancouver.json.gz', lines = True)

    # filtered data based on what amenities we thought were related to each of the values (nightlife, fitness
    # activities, leisure, family, pets, safety) + transportation

    nightlife = data[(data['amenity'] == 'pub')|(data['amenity'] == 'bar')|(data['amenity'] == 'restaurant')|
                (data['amenity'] == 'nightclub')|(data['amenity'] == 'stripclub')|(data['amenity'] == 'gambling')|
                (data['amenity'] == 'casino')|(data['amenity'] == 'lounge')|(data['amenity'] == 'smoking_area')|
                (data['amenity'] == 'events_venue')]

    fitness = data[(data['amenity'] == 'gym')|(data['amenity'] == 'park')|
               (data['amenity'] == 'training')|(data['amenity'] == 'community_centre')]

    activities = data[(data['amenity'] == 'theatre') | (data['amenity'] == 'restaurant')| (data['amenity'] == 'cinema')|
                 (data['amenity'] == 'park')| (data['amenity'] == 'events_venue')| (data['amenity'] == 'Observation Platform')]

    leisure = data[(data['amenity'] == 'lounge')| (data['amenity'] == 'cafe')| (data['amenity'] == 'spa')|
              (data['amenity'] == 'meditation_centre')| (data['amenity'] == 'library')| (data['amenity'] == 'leisure')]

    family = data[(data['amenity'] == 'school')| (data['amenity'] == 'kindergarten')| (data['amenity'] == 'family_centre')|
              (data['amenity'] == 'music_school')| (data['amenity'] == 'playground')| (data['amenity'] == 'park')|
              (data['amenity'] == 'marketplace')|(data['amenity'] == 'childcare')|(data['amenity'] == 'library')]

    pets = data[(data['amenity'] == 'veterinary')| (data['amenity'] == 'park')]

    safety = data[(data['amenity'] == 'hospital')| (data['amenity'] == 'police')|(data['amenity'] == 'fire_station')|
             (data['amenity'] == 'doctors')|(data['amenity'] == 'healthcare')| (data['amenity'] == 'clinic')]

    car = data[(data['amenity'] == 'fuel')|(data['amenity'] == 'parking_space')|(data['amenity'] == 'car_wash')]

    public = data[(data['amenity'] == 'bus_station')|(data['amenity'] == 'car_sharing')| (data['amenity'] == 'car_rental')|
             (data['amenity'] == 'bicycle_rental')]

    bike = data[(data['amenity'] == 'bus_station')|(data['amenity'] == 'car_sharing')| (data['amenity'] == 'car_rental')|
             (data['amenity'] == 'bicycle_rental')|(data['amenity'] == 'bicycle_parking') |
            (data['amenity'] == 'bicycle_repair_station')]

    # added column type to specify value type to select dataframe more easily
    nightlife['type'] = 'nightlife'
    fitness['type'] = 'fitness'
    activities['type'] = 'activities'
    leisure['type'] = 'leisure'
    family['type'] = 'family'
    pets['type'] = 'pets'
    safety['type'] = 'safety'
    car['type'] = 'car'
    public['type'] = 'public'
    bike['type'] = 'bike'

    nightlife.to_json('raw_amenities_dataframes/nightlife_data.json')
    fitness.to_json('raw_amenities_dataframes/fitness_data.json')
    activities.to_json('raw_amenities_dataframes/activities_data.json')
    leisure.to_json('raw_amenities_dataframes/leisure_data.json')
    family.to_json('raw_amenities_dataframes/family_data.json')
    pets.to_json('raw_amenities_dataframes/pets_data.json')
    safety.to_json('raw_amenities_dataframes/safety_data.json')
    car.to_json('raw_amenities_dataframes/car_data.json')
    public.to_json('raw_amenities_dataframes/public_data.json')
    bike.to_json('raw_amenities_dataframes/bike_data.json')

if __name__=='__main__':
    main()
