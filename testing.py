import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types


def main(inputs, output):
    print('\n\n')
    data = spark.read.json(inputs)
    # data.printSchema helpful to pick which tags we want to keep.
    # possibly 'explode' to expand the nested json.
    # data = data.select(data.amenity, data.tags['addr:city'])
    data = data.select(data.amenity).distinct().sort(data.amenity)

    data.show(130, truncate = False)

if __name__ == '__main__':
    inputs = sys.argv[1]
    output = sys.argv[2]
    spark = SparkSession.builder.appName('example code').getOrCreate()
    assert spark.version >= '2.4' # make sure we have Spark 2.4+
    spark.sparkContext.setLogLevel('WARN')
    #sc = spark.sparkContext

    main(inputs, output)
