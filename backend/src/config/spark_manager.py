from constant.environment.variable_key import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from pyspark.sql import SparkSession

spark_session:SparkSession= None

spark_session= SparkSession.builder.appName("Finance").config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem").config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID).config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY).getOrCreate()
