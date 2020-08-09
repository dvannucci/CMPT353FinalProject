import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# http://jeromyanglim.blogspot.com/2009/03/calculating-composite-scores-of-ability.html
# Common pyschology practice to add zscores.
# Quote from the blog "To provide more stable measures of the underlying abilities, composites were formed with unit-weighted z scores of constituent tests"

# Create the zscores DataFrames with the sum fo the zscores for each amenity column.

listofvalues = ['fitness', 'nightlife','activities', 'leisure', 'family', 'pets', 'safety','car','public','bike']

for each in listofvalues:
    valueData = pd.read_json('Vancouver_blocks_amenity_dataframes/' + each + '_blocks.json.gz')
    file = pd.read_json('raw_amenities_dataframes/' + each + '_data.json')
    variables = file['amenity'].unique().tolist()
    outputdf = valueData.iloc[:, :5]
    tempdf = pd.DataFrame()

    for amen in variables:
        tempdf[amen + '_zscore'] = stats.zscore(valueData[amen + '_distance'])

    outputdf = pd.concat([outputdf, tempdf], axis=1)
    outputdf['sum_zscore'] = tempdf.sum(axis=1)

    outputdf.to_json(each + '_zscores.json.gz', compression='gzip')
