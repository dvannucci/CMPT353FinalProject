import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types


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

    new = spark.read.json(inputs)

    new = new.sample(withReplacement=False, fraction=0.001)

    # This creates just two columns, and changes the column 'fields' into an array of coordinate pairs.

    new = new.select('recordid', 'fields').withColumn('fields', functions.explode(new.fields.geom.coordinates))

    new.show()




if __name__ == '__main__':
    inputs = sys.argv[1]
    output = sys.argv[2]
    spark = SparkSession.builder.appName('example code').getOrCreate()
    assert spark.version >= '2.4' # make sure we have Spark 2.4+
    spark.sparkContext.setLogLevel('WARN')
    #sc = spark.sparkContext

    main(inputs, output)
