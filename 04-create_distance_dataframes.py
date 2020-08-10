import pandas as pd
import numpy as np

def distanceCalculate(row, df):
    # Haversine formula
    leftSide = ( np.sin( ( row.thePoint[0] - df.lat ) * ((np.pi)/180)/2 ) ) ** 2
    # This is the left side of the equation on the wikipedia formula.
    rightSide = np.cos(df.lat * ((np.pi)/180)) * np.cos(row.thePoint[0] * ((np.pi)/180)) * ( np.sin( (row.thePoint[1] - df.lon) * ((np.pi)/180)/2 ) ) ** 2
    # This is the last step of the formula, combing the two sides and carrying out the last few calculations assuming the earth's radius is 6,371,000 metres on average.
    distance = np.arcsin(np.sqrt(leftSide + rightSide)) * 2 * 6371000

    return min(distance)


def main():

    listofvalues = ['nightlife','fitness','activities', 'leisure', 'family', 'pets', 'safety','car','public','bike']

    for each in listofvalues:
        blocksData = pd.read_json('VancouverBlocks.json.gz', lines=True)
        file = pd.read_json('raw_amenities_dataframes/' + each + '_data.json')
        vars = file['amenity'].unique().tolist()

        for amen in vars:
            data = file[file.amenity == amen]
            blocksData[amen + '_distance'] = blocksData.apply(distanceCalculate, df = data, axis = 1)

        blocksData.to_json('Vancouver_blocks_amenity_dataframes/' + each + '_blocks.json.gz', compression='gzip')
        

if __name__=='__main__':
    main()
