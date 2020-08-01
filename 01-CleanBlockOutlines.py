import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types, Row
from pyspark.sql.window import Window

from geopy.geocoders import Nominatim
from shapely.geometry import Polygon

def main(inputs, output):

# Function to convert a coordinate pair into an address
    def finder(val):
        locator = Nominatim(user_agent='353 Final')
        spot = locator.reverse( (val[1], val[0]) )
        return spot[0]
# Make the function into a udf.
    locationFinder = functions.udf(finder, returnType=types.StringType())
# Function to take a set of coordinates, and turn it into a polygon object from shapely package.
    def poly(val):
        thePoly = Polygon(val)
# If the area of the shape is larger than approximately 30,000 m^2, then we will exclude that neighbourhood as it is too large, and most likely a park/not a residential area. The value of 0.0000024 is due to a conversion which will be explained in the document.
        if thePoly.area >= 0.0000024:
            return None
# Find a representative point within the polygon, and return that coordinate pair
        thePoint = thePoly.representative_point()
        thePoint = [thePoint.y, thePoint.x]

        return thePoint
# Create a udf funciton.
    pointFinder = functions.udf(poly, returnType=types.ArrayType(types.DoubleType()))



# PROGRAM START

# Read the block data into a spark datframe
    blockData = spark.read.json(inputs)
# For testing, take a very small sample of the blockData.
    #blockData = blockData.sample(withReplacement=False, fraction=0.001)

# This creates just two columns, 'recordid' and 'fields', and changes the column 'fields' into an array of coordinate pairs.
    blockData = blockData.select('recordid', 'fields').withColumn('fields', functions.explode(blockData.fields.geom.coordinates))
# Add this to the end of the above statement to only take two rows for testing.
    # .limit(2)

# Use the function above to add a column to the dataframe called 'thePoint' which will have one representative point that is within the polygon shape.
    blockData = blockData.select('recordid','fields', pointFinder('fields').alias('thePoint'))
# Some values will be null if the area is too large as specified above, so we remove these rows.
    blockData = blockData.dropna()
# Now we create a new row for every coordinate pair. So every previous row looked like recordid, thePoint, [a bunch of coordinate pairs], now we create a row for each coordinate pair. So the new dataframe will be much longer and will have each row being recordid, thePoint, [lat,lon] for every coordinate pair.
    blockData = blockData.select('recordid', 'thePoint', functions.explode('fields').alias('coords'))
# We then call our second udf on every row which return an address for every coordinate pair and calls it 'spots'.
    blockData = blockData.select('recordid', 'thePoint', locationFinder(blockData.coords).alias('spots'))
# Next we group by all the columns to get a count of every distinct recordid, thePoint, address, as we will use this data to find the most common address that appeared when converting coordinates to locations from a particular block outline.
    grouped = blockData.groupBy('recordid', 'thePoint', 'spots').count()

# This creates a ranking system for the next function to use which will rank the most commonly appeared address for every polygon
# Adapted from https://stackoverflow.com/questions/38397796/retrieve-top-n-in-each-group-of-a-dataframe-in-pyspark
    window = Window.partitionBy(grouped['recordid']).orderBy(grouped['count'].desc())
# A new dataframe is returned which will have all the previous columns as well as a new column called 'rank', which will give order to the 'count' values from the groupBy function above.

#For example, if we had rows, Row(recordid 1, thePoint 1, vancouver), Row(recordid 1, thePoint 1, vancouver), Row(recordid 1, thePoint 1, Burnaby), the groupBy function above would return,
# Row(recordid 1, thePoint 1, vancouver, count(2)), Row(recordid 1, thePoint 1, Burnaby, count(1)), as now the rows that had the same location are counted. Then the line below with the ranking would create a new dataframe that would be,
# Row(recordid 1, thePoint 1, vancouver, count(2), rank(1)), Row(recordid 1, thePoint 1, Burnaby, count(1), rank(2)). Since the location vancouver had more instances, it was ranked first, and burnaby was ranked second.
    grouped = grouped.select('*', functions.rank().over(window).alias('rank'))
# This now takes only the top two rankings of each recordid. (It may return more if there is a tie, but that will be handled below.)
    grouped = grouped.filter(grouped.rank <= 2)
# We now collect each distinct point, and put together into one list the top two locations.
# For example, if we had rows like above,
# Row(recordid 1, thePoint 1, vancouver, count(2), rank(1)), Row(recordid 1, thePoint 1, Burnaby, count(1), rank(2)), this would be aggregated into one row with values,
# Row(thePoint 1, [vancouver, burnaby])
    grouped2 = grouped.groupBy('thePoint').agg(functions.collect_list('spots').alias('spots'))
# To handle when more than just two locations are returned because of counting ties, we make our final dataframe which has columns, thePoint, location1, location2.
# For example, the dataframe with row,
# Row(thePoint 1, [vancouver, burnaby]) would be turned into Row(thePoint 1, vancouver, burnaby).
# If a tie happened and we had,
# Row(thePoint 1, [vancouver, burnaby, surrey]), this would become Row(thePoint 1, [vancouver, burnaby]) as well as it just takes the first two locations.
    cleanedData = grouped2.select(grouped2.thePoint, grouped2.spots[0].alias('location1'), grouped2.spots[1].alias('location2'))
# Write the data to a json file.
    cleanedData.write.json(output, mode='overwrite')


if __name__ == '__main__':
    inputs = sys.argv[1]
    output = sys.argv[2]
    spark = SparkSession.builder.appName('example code').getOrCreate()
    assert spark.version >= '2.4' # make sure we have Spark 2.4+
    spark.sparkContext.setLogLevel('WARN')
    #sc = spark.sparkContext

    main(inputs, output)
