import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Blog post outlining a common pyschology practice to add zscores together to get an overall z-score for a value based on its attributes.
# http://jeromyanglim.blogspot.com/2009/03/calculating-composite-scores-of-ability.html

# Quote from the blog "To provide more stable measures of the underlying abilities, composites were formed with unit-weighted z scores of constituent tests"

# Create the zscores DataFrames with the sum of the z-scores for each amenity column.

# These are all the values that we have created data frames for, except for price as that has already been handled.
listofvalues = ['fitness', 'nightlife','activities', 'leisure', 'family', 'pets', 'safety','car','public','bike']

for each in listofvalues:
    # Read each of the minumum distance holding data frames for each iteration of the for loop
    valueData = pd.read_json('Vancouver_blocks_amenity_dataframes/' + each + '_blocks.json.gz')
    # Also read the raw_amenities_dataframes file for the same value, as we need it to gather the list of amenities for that value.
    file = pd.read_json('raw_amenities_dataframes/' + each + '_data.json')
    # Put those amenities into a list.
    variables = file['amenity'].unique().tolist()
    # Create a new data frame with just the first 5 columns of the Vancouver_blocks_amenity_dataframes, which is just the representative point, and the four address locations from the corners.
    outputdf = valueData.iloc[:, :5]
    # Create an empty data frame to be filled in the for loop.
    tempdf = pd.DataFrame()

    # For each amenity in the data frame, create a new column which calculates the z-score for the minimum distance column computed in 04-create_distance_dataframes.py. The z-scores will help us get a better understanding of the relative differences between each distance.
    for amen in variables:
        tempdf[amen + '_zscore'] = stats.zscore(valueData[amen + '_distance'])
    # Put together the first 5 columns taken from above, and all the z-score columns created.
    outputdf = pd.concat([outputdf, tempdf], axis=1)
    # Create one last column which takes the sum of the z-scores row wise for each representative point.
    outputdf['sum_zscore'] = tempdf.sum(axis=1)
    # Output that data to a new file called Vancouver_blocks_zscores.
    outputdf.to_json('Vancouver_blocks_zscores/' + each + '_zscores.json.gz', compression='gzip')
