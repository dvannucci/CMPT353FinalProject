import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types, Row

from geopy.geocoders import Nominatim
from shapely.geometry import Polygon
from collections import Counter

def main(inputs, output):
    print('\n\n')
    # Used this part to read the amenities file that we were given using: spark-submit testing.py amenities-vancouver.json.gz out

    # data = spark.read.json(inputs)
    # data.printSchema helpful to pick which tags we want to keep.
    # possibly 'explode' to expand the nested json.
    # data = data.select(data.amenity, data.tags['addr:city'])
    # data = data.select(data.amenity).distinct().sort(data.amenity)

    #new = data.filter(data.amenity == 'university')

    # data.write.json(output, mode='overwrite')

    # data.show(130, truncate = False)


    # Testing out the block coordinates data with: spark-submit testing.py block-outlines.json out

    # This test creates the dataframe, and makes a small sample to work with.

    blockData = spark.read.json(inputs)

    blockData = blockData.sample(withReplacement=False, fraction=0.001)


    def best_point(row):
        # Create a polygon object using the shapely import.
        thePoly = Polygon(row.fields)
        # If the area of the shape is larger than 30,000 m^2, then we will exclude that neighbourhood as it is too large, and most likely a park/not a residential area. The values of 0.0000024 is due to a conversion which will be explained in the document.

        if thePoly.area >= 0.0000024:
            return None

        # This creates the locator which we use to convert coordinates to addresses.
        locator = Nominatim(user_agent='353 Final')
        # Using shapely again, we ask for a representative point from the polygon, which is guaranteed to be within the polygon shape as shapely docs confirm.
        thePoint = thePoly.representative_point()
        # We must switch the order of the coordinates as Nominatim needs them in lat/lon pairs, and the amenities file also has them this way.
        thePoint = [thePoint.y, thePoint.x]
        # Empty list to hold the addresses of the coordinates we will be searching.
        addresses = []
        # For every coordinate pair in the shape, we search for the closest address to it, and add each of them to a list.
        for x in row.fields:
            test = locator.reverse( (x[1], x[0]) )
            addresses.append(test[0])

        # Upon completion of the search, we use Counter to tell us the number of occurences of each address, and leave us only the top two most common.
        top2Locations = Counter(addresses).most_common(2)
        # We extract the addresses from the counter object, and pass them into a new list which we will be returning as a row.
        locations = [top2Locations[0][0], top2Locations[1][0]]

        # Return a new row object with the representative point found, and the top two locations from that particular blocks polygon.
        return Row(representativePoint = thePoint, locations = locations)




    # This creates just two columns, and changes the column 'fields' into an array of coordinate pairs.

    blockData = blockData.select('recordid', 'fields').withColumn('fields', functions.explode(blockData.fields.geom.coordinates))

    blockDataRDD = blockData.rdd

    blockDataRDD = blockDataRDD.map(best_point)

    blockDataRDD.take(5)

    # Write to a file after ***********




if __name__ == '__main__':
    inputs = sys.argv[1]
    output = sys.argv[2]
    spark = SparkSession.builder.appName('example code').getOrCreate()
    assert spark.version >= '2.4' # make sure we have Spark 2.4+
    spark.sparkContext.setLogLevel('WARN')
    #sc = spark.sparkContext

    main(inputs, output)
