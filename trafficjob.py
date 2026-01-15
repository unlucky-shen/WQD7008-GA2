from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, round

# Initialize Spark Session 
spark = SparkSession.builder \
    .appName("Group16_TrafficPrototype") \
    .getOrCreate()

# Load Data from S3
s3_input_path = "s3://wqd7008group16/raw/traffic.csv"
traffic_df = spark.read.csv(s3_input_path, header=True, inferSchema=True)
  
# Parallel Data Processing
processed_df = traffic_df.groupBy("local_authority_name", "year") \
    .agg(
        sum("all_motor_vehicles").alias("total_traffic_volume"),
        round(avg("link_length_km"), 2).alias("avg_road_length_km")
    ) \
    .filter(col("total_traffic_volume") > 0) \
    .orderBy(col("total_traffic_volume").desc())

# Storage & Output
s3_output_path = "s3://wqd7008group16/processed/analysis_results"
processed_df.write.mode("overwrite").parquet(s3_output_path)

processed_df.show(10)

spark.stop()
