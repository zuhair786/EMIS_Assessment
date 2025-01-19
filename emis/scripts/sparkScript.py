import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode
from awsglue.utils import getResolvedOptions

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Flatten JSON") \
    .getOrCreate()

args = getResolvedOptions(sys.argv, ['S3_Loc'])
# Load the JSON file
file_path = args['S3_Loc']
s3_df = spark.read.option("multiline", "true").json(file_path)

# Explode the `entry` array
df_exploded = s3_df.select(explode(col("entry")).alias("entry"))

# Extract fields from the JSON
flattened_df = df_exploded.select(
    col("entry.resource.resourceType").alias("ResourceType"),
    col("entry.resource.id").alias("ResourceID"),
    col("entry.resource.text.div").alias("TextDiv"),
    col("entry.resource.meta.profile").alias("Profile")
)

# Show the flattened DataFrame
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

# Stop the Spark session
spark.stop()
