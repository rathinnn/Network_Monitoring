from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, TimestampType, DoubleType
#spark = SparkSession.builder.appName("local").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
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
schemad2.printSchema()
query = schemad2 \
    .writeStream \
    .format("memory") \
    .queryName("Trial")\
    .outputMode("Append")\
    .start()

mapdf = schemad2.groupBy("server_id").count()
piedf = schemad2.groupBy("status").count()
topsearchdf = schemad2.groupBy("url").count()
blockeddf = schemad2.where(schemad2.status=='BLOCKED').groupBy('server_id').count()

query2 = mapdf \
    .writeStream \
    .format("memory") \
    .queryName("Trial1")\
    .outputMode("Complete")\
    .start()

query3 = piedf \
    .writeStream \
    .format("memory") \
    .queryName("Trial2")\
    .outputMode("Complete")\
    .start()

query4 = topsearchdf \
    .writeStream \
    .format("memory") \
    .queryName("Trial3")\
    .outputMode("Complete")\
    .start()

query5 = blockeddf \
    .writeStream \
    .format("memory") \
    .queryName("Trial4")\
    .outputMode("Complete")\
    .start()

df = spark.read.table("Trial")
df1 = spark.read.table("Trial1")
df2 = spark.read.table("Trial2")
df3 = spark.read.table("Trial3").orderBy('count',ascending = False)
df4 = df.where(df.status=='BLOCKED').groupBy('server_id').count()



#query.awaitTermination()

#df.select(df.key, get_json_object(df.jstring, '$.f1').alias("c0"), get_json_object(df.jstring, '$.f2').alias("c1") ).collect()
#spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 trial.pydf1.