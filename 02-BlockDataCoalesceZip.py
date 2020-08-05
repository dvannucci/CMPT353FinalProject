import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types, Row

# Run this program with spark-submit 02-BlockDataCoalesceZip.py cleanedBlocks CoalescedBlocks

def main(inputs, output):
    blockData = spark.read.json(inputs)
    # We are able to do a coalesce because there was approximately 4600 rows in the original data set, and we did a filtering (01-CleanBlockOutlines.py) which removed large blocks from the data. For each row in the original data, we only produced one row in 01-CleanBlockOutlines.py, so there is a maximum of around 4600 rows with 5 columns in this input data.
    blockData.coalesce(1).write.json(output, mode='overwrite', compression='gzip')

if __name__ == '__main__':
    inputs = sys.argv[1]
    output = sys.argv[2]
    spark = SparkSession.builder.appName('Coalesce Blocks').getOrCreate()
    assert spark.version >= '2.4' # make sure we have Spark 2.4+
    spark.sparkContext.setLogLevel('WARN')
    #sc = spark.sparkContext

    main(inputs, output)
