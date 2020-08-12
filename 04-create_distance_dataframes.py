import pandas as pd
import numpy as np

def distanceCalculate(row, df):
    # Haversine formula
    leftSide = ( np.sin( ( row.thePoint[0] - df.lat ) * ((np.pi)/180)/2 ) ) ** 2
    # This is the left side of the equation on the wikipedia formula.
    rightSide = np.cos(df.lat * ((np.pi)/180)) * np.cos(row.thePoint[0] * ((np.pi)/180)) * ( np.sin( (row.thePoint[1] - df.lon) * ((np.pi)/180)/2 ) ) ** 2
    # This is the last step of the formula, combing the two sides and carrying out the last few calculations assuming the earth's radius is 6,371,000 metres on average.
    distance = np.arcsin(np.sqrt(leftSide + rightSide)) * 2 * 6371000
    # Return only the shortest distance, since when someone is purchasing a home, they don't need the smallest average distance to a gas station for instance, they only need the closest one to give them that value.
    return min(distance)


def main():
    # These are the values which there are seperate dataframes for each. We will need to go through each file, so we will iterate over this list.
    listofvalues = ['nightlife','fitness','activities', 'leisure', 'family', 'pets', 'safety','car','public','bike']

    for each in listofvalues:
        # Each iteration, we will open a new version of the Vancouver Blocks data.
        blocksData = pd.read_json('VancouverBlocks.json.gz', lines=True)
        # We read the current data frame file for the particular iteration of the for loop.
        file = pd.read_json('raw_amenities_dataframes/' + each + '_data.json')
        # We then create a list of the unique amenities within that file. For example, in fitness, this creates a list like [gym, community_centre, ...]
        vars = file['amenity'].unique().tolist()

        for amen in vars:
            # For each of the amenities, we work through each of them in turn. So for fitness, we begin with only the the gym amenities.
            data = file[file.amenity == amen]
            # For gym amenities for example, we create a new column that will be applying the distanceCalculate function to each row. This formula calculates the distance from the point to every gym, and then returns only the closest one.
            blocksData[amen + '_distance'] = blocksData.apply(distanceCalculate, df = data, axis = 1)
        # Upon going through each amenity of the particular data frame, we output the new data frame with the distance columns to a new folder Vancouver_blocks_amenity_dataframes.
        blocksData.to_json('Vancouver_blocks_amenity_dataframes/' + each + '_blocks.json.gz', compression='gzip')

if __name__=='__main__':
    main()
