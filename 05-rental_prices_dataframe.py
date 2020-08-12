import pandas as pd
import numpy as np
import geopandas as gpd
from scipy import stats
from shapely.geometry import Point

# Data for most location prices from https://www.zumper.com/rent-research/vancouver-bc/kensington-cedar-cottage
# https://vancouver.ca/files/cov/Arbutus-Ridge-census-data.pdf and https://vancouver.ca/files/cov/Shaughnessy-census-data.pdf sources for Shaughnessy and Arbutus-Ridge rental prices data.

def locationFind(row):
    point = Point(row.thePoint[1], row.thePoint[0] )
    for i in range(22):
        if(point.within(poly[i])):
            area = bnd_gdf['name'][i]
            val = prices.loc[area, 'Average Rent']
            return val

    return averageVancouverPrice


bnd_gdf = gpd.read_file('boundary/local-area-boundary.shp')

poly = bnd_gdf['geometry']

prices = pd.read_csv('rental_prices_data/rental_prices_manual.csv', thousands=',', index_col = 'Location')

prices.dropna(how='all', axis='columns', inplace=True)

averageVancouverPrice = prices['Average Rent'].mean()

priceDataframe = pd.read_json('VancouverBlocks.json.gz', lines=True)

priceValues = priceDataframe.apply(locationFind, axis = 1)

priceDataframe['sum_zscore'] = stats.zscore(priceValues)

priceDataframe.to_json('Vancouver_blocks_zscores/price_zscores.json.gz', compression='gzip')
