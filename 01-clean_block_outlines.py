import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types, Row

from geopy.geocoders import Nominatim
from shapely.geometry import Polygon

def main(inputs, output):

# Function to convert a coordinate pair into an address
    def finder(val):
        locator = Nominatim(user_agent='353 Final')
        spot = locator.reverse( (val[0], val[1]) )
        return spot[0]
# Make the function into a udf.
    locationFinder = functions.udf(finder, returnType=types.StringType())
# Function to take a set of coordinates, and turn it into a polygon object from shapely package.
    def poly(val):
        thePoly = Polygon(val)
# If the area of the shape is larger than approximately 30,000 m^2, then we will exclude that neighbourhood as it is too large, and most likely a park/not a residential area. The value of 0.0000024 was calculated from a conversion between length in metres, to latitude or longitude degrees. 0.0000024 is roughly equal to 30,000 square metres of area.
        if thePoly.area >= 0.0000024:
            return None
# Find a representative point within the polygon.
        thePoint = thePoly.representative_point()
# Find the minX, minY, maxX, maxY values of the polygon's shape.
        corners = thePoly.bounds
# Create a variable that holds the representative point, and the created coordinates of the four corners of the polygon.
        allCoords = [[[thePoint.y, thePoint.x]], [[corners[1], corners[0]], [corners[3], corners[0]], [corners[1], corners[2]], [corners[3], corners[2]]]]

        return allCoords

# Create a udf funciton for the function poly.
    pointFinder = functions.udf(poly, returnType=types.ArrayType(types.ArrayType(types.ArrayType(types.DoubleType()))))

# Define the nested schema for the input file.
    coordinatesType = types.StructType([
        types.StructField('coordinates', types.ArrayType(types.ArrayType(types.ArrayType(types.DoubleType()))), nullable = False),
        types.StructField('type', types.StringType(), nullable = True)
    ])

    geomType = types.StructType([
        types.StructField('geom', coordinatesType, nullable = False)
    ])

    blockDataSchema = types.StructType([
        types.StructField('datasetid', types.StringType(), nullable=False),
        types.StructField('fields', geomType, nullable=False),
        types.StructField('record_timestamp', types.TimestampType(), nullable=True),
        types.StructField('recordid', types.StringType(), nullable=False),

    ])

# PROGRAM START

# Read the block data into a spark datframe
    blockData = spark.read.json(inputs, schema=blockDataSchema)
# For testing, take a very small sample of the blockData.
    #blockData = blockData.sample(withReplacement=False, fraction=0.001)

# This creates just two columns, 'recordid' and 'fields', and changes the column 'fields' into an array of coordinate pairs.
    blockData = blockData.select('recordid', 'fields').withColumn('fields', functions.explode(blockData.fields.geom.coordinates))
# Add this to the end of the above statement to only take two rows for testing.
    # .limit(2)

# Use the function above to add a column to the dataframe called 'repPoint and corners' which will have one representative point that is within the polygon shape, and the four corners of the polygon region.
    blockData = blockData.select('recordid', pointFinder('fields').alias('repPoint and corners'))
# Some values will be null if the area is too large as specified above, so we remove these rows.
    blockData = blockData.dropna()
# Seperate the 'repPoint and corners' column into two columns. One with the point called 'thePoint', and one with the corners coordinates called 'coords'.
    blockData = blockData.select('recordid', blockData['repPoint and corners'][0][0].alias('thePoint'), blockData['repPoint and corners'][1].alias('coords'))

# Now we create a new row for every coordinate pair. So every previous row looked like recordid, thePoint, [a bunch of coordinate pairs], now we create a row for each coordinate pair. So the new dataframe will be much longer and will have each row being recordid, thePoint, [lat,lon] for every coordinate pair.
    blockData = blockData.select('recordid', 'thePoint', functions.explode('coords').alias('coords'))
# We then call our second udf on every row which return an address for every coordinate pair and calls it 'spots'.

    blockData = blockData.select('recordid', 'thePoint', locationFinder(blockData.coords).alias('spots'))

# We now collect each location that cooresponds to the corners of each point and put together into one list with the four found locations.
    groupedData = blockData.groupBy('thePoint').agg(functions.collect_list('spots').alias('spots'))
# We now seperate the grouped list into four different columns to create the final dataframe. This dataframe will have the first column being the coordinate of the representative point, and the next four columns will be the addresses found by each of the corners coordinates.
    cleanedData = groupedData.select(groupedData.thePoint, groupedData.spots[0].alias('location1'), groupedData.spots[1].alias('location2'), groupedData.spots[2].alias('location3'), groupedData.spots[3].alias('location4'))
# Write the data to a json file.
    cleanedData.write.json(output, mode='overwrite')


if __name__ == '__main__':
    inputs = sys.argv[1]
    output = sys.argv[2]
    spark = SparkSession.builder.appName('Clean Blocks').getOrCreate()
    assert spark.version >= '2.4' # make sure we have Spark 2.4+
    spark.sparkContext.setLogLevel('WARN')
    #sc = spark.sparkContext

    main(inputs, output)
