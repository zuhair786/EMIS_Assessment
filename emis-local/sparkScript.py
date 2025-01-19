import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode

spark = SparkSession.builder \
    .appName("Flatten JSON") \
    .getOrCreate()

file_path = "hdfs://namenode:9870/data/patients/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json"
s3_df = spark.read.option("multiline", "true").json(file_path)

df_exploded = s3_df.select(explode(col("entry")).alias("entry"))

flattened_df = df_exploded.select(
    col("entry.resource.resourceType").alias("ResourceType"),
    col("entry.resource.id").alias("ResourceID"),
    col("entry.resource.text.div").alias("TextDiv")
)

flattened_df.show(truncate=False)
flattened_df = flattened_df.fillna("null")

mysql_url = "jdbc:mysql://mysql:3306/testdb"
mysql_table = "flattened_data"
mysql_properties = {
    "user": "spark",
    "password": "sparkpassword",
    "driver": "com.mysql.cj.jdbc.Driver"
}

flattened_df.write \
    .jdbc(url=mysql_url, table=mysql_table, mode="overwrite", properties=mysql_properties)

print("Data successfully written to MySQL!")
spark.stop()
