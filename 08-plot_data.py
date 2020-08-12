import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib.cm as cm
from shapely.geometry.polygon import LinearRing, Polygon
import seaborn as sns


def main():

    nightlife = pd.read_json('raw_amenities_dataframes/nightlife_data.json')
    fitness = pd.read_json('raw_amenities_dataframes/fitness_data.json')
    activities = pd.read_json('raw_amenities_dataframes/activities_data.json')
    leisure = pd.read_json('raw_amenities_dataframes/leisure_data.json')
    family = pd.read_json('raw_amenities_dataframes/family_data.json')
    pets = pd.read_json('raw_amenities_dataframes/pets_data.json')
    safety = pd.read_json('raw_amenities_dataframes/safety_data.json')
    car = pd.read_json('raw_amenities_dataframes/car_data.json')
    public = pd.read_json('raw_amenities_dataframes/public_data.json')
    bike = pd.read_json('raw_amenities_dataframes/bike_data.json')


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

    listofvalues = ['family','fitness','activities', 'leisure', 'nightlife', 'pets', 'safety','car','public','bike']

    group = pd.concat([family,fitness,activities,leisure,nightlife,pets,safety,car,public,bike])

    group = group[(group['lat']>= 49.2 )&(group['lat'] <= 49.3) & (group['lon'] >= -123.225 )&(group['lon'] <= -123.025)]

    # adapted from https://medium.com/python-in-plain-english/mapping-with-pythons-geopandas-2869bb758b08

    bnd_gdf = gpd.read_file('boundary/local-area-boundary.shp')
    ps_gdf = gpd.read_file('public-streets/public-streets.shp')

    poly = bnd_gdf['geometry']

    poly['coords'] = poly.apply(lambda x: x.representative_point().coords[:])
    poly['coords'] = [coords[0] for coords in poly['coords']]

    x,y = poly.exterior[0].xy

    fig, ax = plt.subplots(1, figsize = (30,12))

    bnd_gdf.plot(ax = ax, color = 'black')
    ps_gdf.plot(ax = ax, color = 'white', alpha = 0.4)

    # https://matplotlib.org/3.3.0/tutorials/colors/colormaps.html
    # https://stackoverflow.com/questions/12236566/setting-different-color-for-each-series-in-scatter-plot-on-matplotlib

    amen = group['amenity'].unique()
    twcolours = cm.twilight(np.linspace(0, 1, len(amen)))

    for x,colour in zip(amen,twcolours):
        agg = group.loc[group['amenity']==x]
        ax.scatter(agg['lon'],agg['lat'], c = colour, label = x)
    plt.legend()

    for i in range(len(poly) - 1):
        x,y = poly.exterior[i].xy
        plt.plot(x, y, color='#6699cc', alpha=0.7,
            linewidth=3, solid_capstyle='round', zorder=2)
        plt.annotate(s = bnd_gdf['name'][i], xy = poly['coords'][i], c = 'yellow', 
                 horizontalalignment='center', fontsize = 15)
    

    
    plt.title('Amenities of\n Vancouver, BC', loc = 'left', fontsize = 40)

    ax.axis('off')

    plt.show()
    
    nightlife = pd.read_json('Vancouver_blocks_amenity_dataframes/nightlife_blocks.json.gz')
    fitness = pd.read_json('Vancouver_blocks_amenity_dataframes/fitness_blocks.json.gz')
    activities = pd.read_json('Vancouver_blocks_amenity_dataframes/activities_blocks.json.gz')
    leisure = pd.read_json('Vancouver_blocks_amenity_dataframes/leisure_blocks.json.gz')
    family = pd.read_json('Vancouver_blocks_amenity_dataframes/family_blocks.json.gz')
    pets = pd.read_json('Vancouver_blocks_amenity_dataframes/pets_blocks.json.gz')
    safety = pd.read_json('Vancouver_blocks_amenity_dataframes/safety_blocks.json.gz')
    car = pd.read_json('Vancouver_blocks_amenity_dataframes/car_blocks.json.gz')
    public = pd.read_json('Vancouver_blocks_amenity_dataframes/public_blocks.json.gz')
    bike = pd.read_json('Vancouver_blocks_amenity_dataframes/bike_blocks.json.gz')

    listofdf = [nightlife,fitness,activities,leisure,family,pets,safety,car,public,bike]

    for df in listofdf:
        df.drop(columns = ['location1','location2','location3','location4', 'thePoint'], inplace = True)
        for col in df:
            sns.kdeplot(df[col], label = col, shade = True)
            plt.xlabel('Distances')
            plt.ylabel('Density')
            plt.title('Density Plot of Minimum '+col+'s')
            plt.show()

if __name__=='__main__':
    main()
