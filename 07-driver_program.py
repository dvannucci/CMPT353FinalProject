import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry.polygon import LinearRing, Polygon, Point

def main():

    print("Please select three different values in buying a house from the list below,\n-nightlife \n-fitness \n-activities \n-leisure \n-family \n-pets \n-safety")
    listofvalues = ['nightlife','fitness','activities', 'leisure', 'family', 'pets', 'safety']

    while True:
        value1 = input("Enter your first value: ")
        if value1 not in listofvalues:
            print("That is not a value in the list! Try again.")
            continue
        else:
            break

    while True:
        value2 = input("Enter your second most important value: ")
        if (value2 not in listofvalues or value2 == value1):
            print("That is not a value in the list, or has already been inputted.")
            continue
        else:
            break

    while True:
        value3 = input("Lastly, your third most important value: ")
        if (value3 not in listofvalues or value3 == value1 or value3 == value2):
            print("That is not a value in the list, or has already been inputted.")
            continue
        else:
            break


    print("\nPlease select your primary mode of transportation between, \n-car \n-bike \n-public (as in public transit)")
    listoftransport = ['car','bike','public']

    while True:
        transportation = input("Enter main mode of transportation: ")
        if(transportation not in listoftransport):
            print("That is not a value in the list! Try again.")
            continue
        else:
            break

    print("\nAnd last, when it comes to price, what describes you best,\n (1) Price is not an issue\n (2) I would prefer cheaper, but not the largest deal breaker\n (3) I am very price sensitive (i.e less expensive the better)")
    sensitive = ['1','2','3']

    while True:
        priceweight = input("Enter 1, 2 or 3 based on the criteria above: ")
        if (priceweight not in sensitive):
            print("That is not either 1, 2 or 3.")
            continue
        else:
            break

    # Read the appropriate dataframes.
    firstdf = pd.read_json('Vancouver_blocks_zscores/' + value1 + '_zscores.json.gz')
    seconddf = pd.read_json('Vancouver_blocks_zscores/' + value2 + '_zscores.json.gz')
    thirddf = pd.read_json('Vancouver_blocks_zscores/' + value3 + '_zscores.json.gz')
    transportdf = pd.read_json('Vancouver_blocks_zscores/' + transportation + '_zscores.json.gz')
    pricedf = pd.read_json('Vancouver_blocks_zscores/price_zscores.json.gz')

    # Create a new dataframe with just the first five columns of the original dataframes. The columns location1, location2, location3, location4, and the point.
    newframe = firstdf.iloc[: , :5]

    # Formula for changing range of values onto a new range
    # https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio

    # The new range that we are going to convert it to with a max value of 10 and a min of 1. This is an arbitrary range, the importance is that all the values will be greater than 0.
    new_range = 10 - 1
    # For each dataframe, make a new column with the converted sum_zscore normalized from 1 to 10.
    for i, df in enumerate(['firstdf', 'seconddf', 'thirddf', 'transportdf', 'pricedf'], start=1):
        df = vars()[df]
        old_range = max(df.sum_zscore) - min(df.sum_zscore)
        newframe['score' + str(i)] = (((df.sum_zscore - min(df.sum_zscore)) * new_range) / old_range) + 1

    # Calculation of the weighted score. The values in the exponents, 2, 1.4 and 1.2, were just guesses to be tested out.
    # https://pubsonline.informs.org/doi/pdf/10.1287/ited.2013.0124
    # Article for multiplicative scoring function with weight.
    newframe['score'] = 1 / ( (newframe.score1 ** 2.5) * (newframe.score2 ** 2) * (newframe.score3 ** 1.5) * (newframe.score4 ** 2) * (newframe.score5 ** int(priceweight))  )

    # Find the index of the row with the max score
    index = newframe.score.idxmax()

    theRow = newframe.iloc[index]

    print(theRow)

    print("\n\nYour ideal living location is within the addresses of,\n\n 1. %s \n 2. %s \n 3. %s \n 4. %s.\n\nThis location has the best overall %s, %s, and %s score in that order of importance, while taking into account your primary transportation mode, %s." %(theRow.location1, theRow.location2, theRow.location3, theRow.location4, value1, value2, value3, transportation))

    listofvalues = ['nightlife','fitness','activities', 'leisure', 'family', 'pets', 'safety','car','public','bike']
    
    group = pd.DataFrame()
    
    for val in listofvalues:
        group = pd.concat([group,pd.read_json('raw_amenities_dataframes/'+val+'_data.json')])
    
    for x in listofvalues:
        if value1 == x:
            firstdf = group[group['type'] == x]
        if value2 == x:
            seconddf = group[group['type'] == x]
        if value3 == x:
            thirddf = group[group['type'] == x]
        if transportation == x:
            transportdf = group[group['type'] == x]
    
    con = pd.concat([firstdf,seconddf,thirddf,transportdf])

    con = con[(con['lat']>= 49.2 )&(con['lat'] <= 49.3) & (con['lon'] >= -123.225 )&(con['lon'] <= -123.025)]
    #con = con.reset_index()

    bnd_gdf = gpd.read_file('boundary/local-area-boundary.shp')
    ps_gdf = gpd.read_file('public-streets/public-streets.shp')

    poly = bnd_gdf['geometry']


    poly['coords'] = poly.apply(lambda x: x.representative_point().coords[:])
    poly['coords'] = [coords[0] for coords in poly['coords']]


    fig, ax = plt.subplots(1, figsize = (30,12))

    bnd_gdf.plot(ax = ax, color = 'black')
    ps_gdf.plot(ax = ax, color = 'white', alpha = 0.4)


    amen = con['amenity'].unique()
    for x in amen:
        agg = con.loc[con['amenity']==x]
        ax.scatter(agg['lon'],agg['lat'], label = x)
    ax.legend()

    # https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html
    point = Point(theRow.thePoint[1],theRow.thePoint[0])
    for i in range(len(poly) - 1):
        x,y = poly.exterior[i].xy
        #print(x,y)
        if poly[i].contains(point):
            plt.plot(x, y, color='red', alpha=0.7,
            linewidth=3, solid_capstyle='round', zorder=2)
            neighbourhoodname = bnd_gdf['name'][i]
        else:
            plt.plot(x, y, color='#6699cc', alpha=0.7,
            linewidth=3, solid_capstyle='round', zorder=2)
        plt.annotate(s = bnd_gdf['name'][i], xy = poly['coords'][i], c = 'yellow',
                     horizontalalignment='center', fontsize = 15)


    plt.scatter(x = theRow.thePoint[1], y = theRow.thePoint[0], s = 1000,c = 'red',marker = (5,1))

    plt.title('Amenities of\n Vancouver, BC', loc = 'left', fontsize = 40)

    ax.axis('off')

    plt.show()

if __name__ == '__main__':
    main()
