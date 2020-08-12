import pandas as pd
import numpy as np
import geopandas as gpd
from scipy import stats
from shapely.geometry import Point

# Data for most location prices from https://www.zumper.com/rent-research/vancouver-bc/kensington-cedar-cottage
# https://vancouver.ca/files/cov/Arbutus-Ridge-census-data.pdf and https://vancouver.ca/files/cov/Shaughnessy-census-data.pdf are the sources for Shaughnessy and Arbutus-Ridge rental prices data.

# Function to return an average rental price for each coordinate in Vancouver.
def locationFind(row):
    # Create a shapely Point object which takes a lon/lat pair, so we must reverse the coordinates
    point = Point(row.thePoint[1], row.thePoint[0] )
    # For each of the 22 neighborhoods, we check if the point is within their bounds
    for i in range(22):
        # If the point is found in one of the polygons, then we locate the row with that has the neighborhood name as index, and take its average rental price, and return that value.
        if(point.within(poly[i])):
            area = bnd_gdf['name'][i]
            val = prices.loc[area, 'Average Rent']
            return val
    # If the point is not within any of the blocks, then return the average price calculated below.
    return averageVancouverPrice

# These two lines gather the neighbourhood names for all 22 neighbourhoods in Vancouver.
bnd_gdf = gpd.read_file('boundary/local-area-boundary.shp')
poly = bnd_gdf['geometry']
# We read the prices data frame that we will use to assign an average price for each point.
prices = pd.read_csv('rental_prices_data/rental_prices_manual.csv', thousands=',', index_col = 'Location')
# Drop columns with no data in them.
prices.dropna(how='all', axis='columns', inplace=True)
# For some few coordinate points, they do not locate into any of the Vancouver neighborhood polygons, therefore to assign them a price, we take the average of all the other neighbourhoods to get a Vancouver general renting price.
averageVancouverPrice = prices['Average Rent'].mean()
# Read the VancouverBlocks data frame with all the points and locations.
priceDataframe = pd.read_json('VancouverBlocks.json.gz', lines=True)
# Create a series from the VancouverBlocks data by applying the function locationFind from above, which will return the average rental price for each row/coordinate.
priceValues = priceDataframe.apply(locationFind, axis = 1)
# For series created, we convert it to a column of z-scores to create a ranking between the prices, and append the z-scores to the end of the VancouverBlocks data frame.
priceDataframe['sum_zscore'] = stats.zscore(priceValues)
# Lastly, we output this data into the Vancouver_blocks_zscores folder.
priceDataframe.to_json('Vancouver_blocks_zscores/price_zscores.json.gz', compression='gzip')
