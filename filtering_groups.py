#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd

def main():
    data = pd.read_json('amenities-vancouver.json.gz', lines = True)
    
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
    
    print("List of values in neighbourhood: \n(nightlife, outdoor/fitness, activities, leisure, family, pets, safety)")
    listofvalues = ['nightlife','outdoor/fitness','activities', 'leisure', 'family', 'pets', 'safety']
    
    value1 = input("Enter first value: ")
    value2 = input("Enter second value: ")
    value3 = input("Enter third value: ")
    
    if(value1 not in listofvalues or value2 not in listofvalues or value3 not in listofvalues):
        print("ERROR not a value")
        return
    
    print("List of transportation: \n(car, bike, public)")
    listoftransport = ['car','bike','public']
    transportation = input("Enter main mode of transportation: ")
    
    if(transportation not in listoftransport):
        print("ERROR incorrect transportation")
        return
    

if __name__=='__main__':
    main()


# In[ ]:




