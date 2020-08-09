import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd


def main():

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

    firstdf = pd.read_json(value1 + '_data.json')
    seconddf = pd.read_json(value2 + '_data.json')
    thirddf = pd.read_json(value3 + '_data.json')
    transportdf = pd.read_json(transportation + '_data.json')

    # merged the 3 dataframes of the 3 values chosen by user

    group = pd.concat([firstdf,seconddf,thirddf,transportdf])

    # filtered data to just Vancouver, not including Burnaby, Richmond, etc ..
    group = group[(group['lat']>= 49.2 )&(group['lat'] <= 49.3) & (group['lon'] >= -123.225 )&(group['lon'] <= -123.025)]

    # adapted from https://medium.com/python-in-plain-english/mapping-with-pythons-geopandas-2869bb758b08
    # data from https://opendata.vancouver.ca/pages/home/
    bnd_gdf = gpd.read_file('boundary/local-area-boundary.shp')
    ps_gdf = gpd.read_file('public-streets/public-streets.shp')

    poly = bnd_gdf['geometry']

    poly['coords'] = poly.apply(lambda x: x.representative_point().coords[:])
    poly['coords'] = [coords[0] for coords in poly['coords']]

    x,y = poly.exterior[0].xy

    fig, ax = plt.subplots(1, figsize = (30,12))

    bnd_gdf.plot(ax = ax, color = 'black')
    ps_gdf.plot(ax = ax, color = 'white', alpha = 0.4)
    #plt.scatter(group['lon'],group['lat'], color = 'red')

    amen = group['amenity'].unique()
    for x in amen:
        agg = group.loc[group['amenity']==x]
        ax.scatter(agg['lon'],agg['lat'], label = agg['amenity'])
    plt.legend(labels = amen)

    for i in range(len(poly) - 1):
        x,y = poly.exterior[i].xy
        plt.plot(x, y, color='#6699cc', alpha=0.7,
            linewidth=3, solid_capstyle='round', zorder=2)
        plt.annotate(s = bnd_gdf['name'][i], xy = poly['coords'][i], c = 'yellow', horizontalalignment='center')
    

    
    plt.title('Amenities of\n Vancouver, BC', loc = 'left', fontsize = 40)

    ax.axis('off')

    plt.show()


    

if __name__=='__main__':
    main()
