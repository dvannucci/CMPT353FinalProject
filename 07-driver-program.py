import pandas as pd
import numpy as np

def main():
    pd.set_option('display.max_columns', None)

    print("Please select your most important value in buying a house from the list below,\n-nightlife \n-fitness \n-activities \n-leisure \n-family \n-pets \n-safety")
    listofvalues = ['nightlife','fitness','activities', 'leisure', 'family', 'pets', 'safety']

    value1 = input("Enter your first value: ")
    value2 = input("Enter your second most important value: ")
    value3 = input("Lastly, your third most important value: ")

    # included error messages in case typo in input

    if(value1 not in listofvalues or value2 not in listofvalues or value3 not in listofvalues):
        print("ERROR not a value")
        return

    print("\nPlease select your primary mode of transportation between, \n-car \n-bike \n-public (as in public transit)")
    listoftransport = ['car','bike','public']
    transportation = input("Enter main mode of transportation: ")

    if(transportation not in listoftransport):
        print("ERROR incorrect transportation")
        return

    # Read the appropriate dataframes.
    firstdf = pd.read_json('Vancouver_blocks_zscores/' + value1 + '_zscores.json.gz')
    seconddf = pd.read_json('Vancouver_blocks_zscores/' + value2 + '_zscores.json.gz')
    thirddf = pd.read_json('Vancouver_blocks_zscores/' + value3 + '_zscores.json.gz')
    transportdf = pd.read_json('Vancouver_blocks_zscores/' + transportation + '_zscores.json.gz')

    # Create a new dataframe with just the first five columns of the original dataframes. The columns location1, location2, location3, location4, and the point.
    newframe = firstdf.iloc[: , :5]

    # Formula for changing range of values onto a new range
    # https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio

    # The new range that we are going to convert it to with a max value of 10 and a min of 1. This is an arbitrary range, the importance is that all the values will be greater than 0.
    new_range = 10 - 1
    # For each dataframe, make a new column with the converted sum_zscore normalized from 1 to 10.
    for i, df in enumerate(['firstdf', 'seconddf', 'thirddf', 'transportdf'], start=1):
        df = vars()[df]
        old_range = max(df.sum_zscore) - min(df.sum_zscore)
        newframe['score' + str(i)] = (((df.sum_zscore - min(df.sum_zscore)) * new_range) / old_range) + 1

    # Calculation of the weighted score. The values in the exponents, 2, 1.4 and 1.2, were just guesses to be tested out.
    # https://pubsonline.informs.org/doi/pdf/10.1287/ited.2013.0124
    # Article for multiplicative scoring function with weight.
    newframe['score'] = 1 / ( (newframe.score1 ** 2) * (newframe.score2 ** 1.6) * (newframe.score3 ** 1.2) * (newframe.score4 ** 1.4)  )

    # Find the index of the row with the max score
    index = newframe.score.idxmax()

    theRow = newframe.iloc[index]
    # Print the row with the max score.
    print(theRow)
    print('\n\n')

    print("Your ideal living location is within the addresses of,\n\n 1. %s \n 2. %s \n 3. %s \n 4. %s.\n\nThis location has the best overall %s, %s, and %s score in that order of importance, while taking into account your primary transportation mode, %s." %(theRow.location1, theRow.location2, theRow.location3, theRow.location4, value1, value2, value3, transportation))


if __name__ == '__main__':
    main()
