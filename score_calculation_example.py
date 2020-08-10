import pandas as pd
import numpy as np
from scipy import stats

pd.set_option('display.max_columns', None)

# https://pubsonline.informs.org/doi/pdf/10.1287/ited.2013.0124
# Article for multiplicative scoring function with weight

# Formula for changing range of values onto a new range
# https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio

# Read 3 of the values files, for example, fitness, leisure, and safety
data1 = pd.read_json('Vancouver_blocks_zscores/fitness_zscores.json.gz')
data2 = pd.read_json('Vancouver_blocks_zscores/leisure_zscores.json.gz')
data3 = pd.read_json('Vancouver_blocks_zscores/safety_zscores.json.gz')

# The old range of the values for sum_zscore.
old_range = max(data1.sum_zscore) - min(data1.sum_zscore)

# The new range that we are going to convert it to with a max value of 10 and a min of 1
new_range = 10 - 1

# New column in the first dataframe with the converted sum_zscore column.
data1['converted_zscores'] = (((data1.sum_zscore - min(data1.sum_zscore)) * new_range) / old_range) + 1

# The old range of the values for sum_zscore.
old_range = max(data2.sum_zscore) - min(data2.sum_zscore)

# Same for the second dataframe
data2['converted_zscores'] = (((data2.sum_zscore - min(data2.sum_zscore)) * new_range) / old_range) + 1

# The old range of the values for sum_zscore.
old_range = max(data3.sum_zscore) - min(data3.sum_zscore)

# Same for the last.
data3['converted_zscores'] = (((data3.sum_zscore - min(data3.sum_zscore)) * new_range) / old_range) + 1

# Create a new dataframe with just the first five columns of the original dataframes. The columns location1, location2, location3, location4, and the point.
newframe = data1.iloc[: , :5]

# Add each of the converted z scores to the end of the new dataframe.
newframe['score1'] = data1['converted_zscores']
newframe['score2'] = data2['converted_zscores']
newframe['score3'] = data3['converted_zscores']

# Calculation of the weighted score. The values in the exponents, 2, 1.4 and 1.2, were just guesses to be tested out.
newframe['score'] = 1 / ( (newframe.score1 ** 2) * (newframe.score2 ** 1.4) * (newframe.score3 ** 1.2)    )

# Find the index of the row with the max score
index = newframe.score.idxmax()

theRow = newframe.iloc[index]
# Print the row with the max score.
print(theRow)
print('\n\n')

print("Your ideal living location is within the blocks of,\n\n 1. %s \n 2. %s \n 3. %s \n 4. %s.\n\nThis location has the best overall fitness, leisure, and safety score in that order of importance." %(theRow.location1, theRow.location2, theRow.location3, theRow.location4))
