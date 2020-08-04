#!/usr/bin/env python
# coding: utf-8

# In[27]:

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

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
    
    print("List of values in neighbourhood: \n(nightlife, fitness, activities, leisure, family, pets, safety)")
    listofvalues = ['nightlife','fitness','activities', 'leisure', 'family', 'pets', 'safety']
    
    value1 = input("Enter first value: ")
    value2 = input("Enter second value: ")
    value3 = input("Enter third value: ")
    
    # included error messages in case typo in input
    
    if(value1 not in listofvalues or value2 not in listofvalues or value3 not in listofvalues):
        print("ERROR not a value")
        return
    
    print("List of transportation: \n(car, bike, public)")
    listoftransport = ['car','bike','public']
    transportation = input("Enter main mode of transportation: ")
    
    if(transportation not in listoftransport):
        print("ERROR incorrect transportation")
        return
    
    # conditions for reading inputs and selecting the dataframe for that specific input/value
    
    if(value1 == 'nightlife'):
        firstdf = nightlife
    elif(value1 == 'fitness'):
        firstdf = fitness
    elif(value1 == 'activities'):
        firstdf = activities
    elif(value1 == 'leisure'):
        firstdf = leisure
    elif(value1 == 'family'):
        firstdf = family
    elif(value1 == 'pets'):
        firstdf = pets
    else:
        firstdf = safety
        
    if(value2 == 'nightlife'):
        seconddf = nightlife
    elif(value2 == 'fitness'):
        seconddf = fitness
    elif(value2 == 'activities'):
        seconddf = activities
    elif(value2 == 'leisure'):
        seconddf = leisure
    elif(value2 == 'family'):
        seconddf = family
    elif(value2 == 'pets'):
        seconddf = pets
    else:
        seconddf = safety
        
    if(value3 == 'nightlife'):
        thirddf = nightlife
    elif(value3 == 'fitness'):
        thirddf = fitness
    elif(value3 == 'activities'):
        thirddf = activities
    elif(value3 == 'leisure'):
        thirddf = leisure
    elif(value3 == 'family'):
        thirddf = family
    elif(value3 == 'pets'):
        thirddf = pets
    else:
        thirddf = safety
    
    # merged the 3 dataframes of the 3 values chosen by user
    
    group = pd.concat([firstdf,seconddf,thirddf])
    
    # filtered data to just Vancouver, not including Burnaby, Richmond, etc .. 
    group = group[(group['lat']>= 49.2 )&(group['lat'] <= 49.3) & (group['lon'] >= -123.225 )&(group['lon'] <= -123.025)]
    
    # adapted from https://medium.com/python-in-plain-english/mapping-with-pythons-geopandas-2869bb758b08

    bnd_gdf = gpd.read_file('boundary/local-area-boundary.shp')
    ps_gdf = gpd.read_file('public-streets/public-streets.shp')
    
    fig, ax = plt.subplots(1, figsize = (16,8))

    bnd_gdf.plot(ax = ax, color = 'black')
    ps_gdf.plot(ax = ax, color = 'white', alpha = 0.4)
    plt.scatter(group['lon'],group['lat'], color = 'red')

    plt.title('Amenities of\n Vancouver, BC', loc = 'left', fontsize = 20)

    ax.axis('off')

    plt.show()
    
if __name__=='__main__':
    main()



