from pyspark.sql.types import *
from pyspark.sql.functions import *

def init(spark):
    df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("startingOffsets", "latest") \
    .option("subscribe", "test2") \
    .load()
    schema = StructType([ \
        StructField("server_id",IntegerType(),True),\
        StructField("status",StringType(),True), \
        StructField("method",StringType(),True), \
        StructField("url", StringType(),True), \
        ])
        #StructField("index",IntegerType(),True), \

    df2 = df.selectExpr("CAST(value AS STRING)")
    df2.printSchema()
    schemad = df2.select( from_json(df2.value,schema).alias('value') )
    schemad.printSchema()
    schemad2 = schemad.selectExpr("value.server_id", "value.status","value.method","value.url")
    #schmead2 = schemad2.withColumn("Lat",schemad2.Lat.cast(DoubleType())).withColumn("Lon",schemad2.Lon.cast(DoubleType()))  

    mapdf = schemad2.groupBy("server_id").count()
    statusdf = schemad2.groupBy("status").count()
    topsearchdf = schemad2.groupBy("url").count()
    blockeddf = schemad2.where(schemad2.status=='BLOCKED').groupBy('server_id').count()
    methoddf = schemad2.groupBy("method").count()

    query1 = mapdf \
        .writeStream \
        .format("memory") \
        .queryName("Trial1")\
        .outputMode("Complete")\
        .start()

    query2 = statusdf \
        .writeStream \
        .format("memory") \
        .queryName("Trial2")\
        .outputMode("Complete")\
        .start()

    query3 = topsearchdf \
        .writeStream \
        .format("memory") \
        .queryName("Trial3")\
        .outputMode("Complete")\
        .start()

    query4 = blockeddf \
        .writeStream \
        .format("memory") \
        .queryName("Trial4")\
        .outputMode("Complete")\
        .start()

    query5 = methoddf \
        .writeStream \
        .format("memory") \
        .queryName("Trial5")\
        .outputMode("Complete")\
        .start()

def getMapDF(spark):
    df1 = spark.read.table("Trial1")
    return df1

def getStatusDF(spark):
    df2 = spark.read.table("Trial2")
    return df2

def getSearchDF(spark):
    df3 = spark.read.table("Trial3").orderBy('count',ascending = False)
    return df3

def getBlockedDF(spark):
    df4 = spark.read.table("Trial4")
    return df4

def getMethodDF(spark):
    df5 = spark.read.table("Trial5")
    return df5

#df.limit(3).toPandas()
#fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})