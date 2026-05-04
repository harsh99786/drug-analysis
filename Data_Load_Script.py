# Creating spark session
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("CSV to PostgreSQL") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
    .getOrCreate()

# JDBC connection properties
jdbc_url = "jdbc:postgresql://localhost:5432/Clinical_Trial"

properties = {
    "user": "postgres",
    "password": "387162",
    "driver": "org.postgresql.Driver"
}

# List of CSV files to load
files = ["status.csv", "studypopulation.csv", "sponsor.csv", "medicalcondition.csv", "drugproduct.csv", "protocol.csv"]

# Python loop to read each CSV and write to PostgreSQL
for file in files:
    table_name = file.replace(".csv", "")  # remove extension
    
    df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .option("multiLine", True) \
    .option("quote", '"') \
    .option("escape", '"') \
    .option("lineSep", "\n") \
    .csv(f"/Users/manat/Desktop/projects/ClinicalTrialData/{file}")
    
    df.write.jdbc(
        url=jdbc_url,
        table=table_name,
        mode="overwrite",
        properties=properties)
    
