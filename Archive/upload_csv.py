from sqlalchemy import create_engine
import pandas as pd

# 🔑 Database Credentials
DB_HOST = "tm01onboarding-tm01onboarding.e.aivencloud.com"
DB_PORT = "13812"
DB_NAME = "defaultdb"
DB_USER = "avnadmin"
DB_PASS = "AVNS_AFmtCZU-RoKIAHPUNUx"

# Create SQLAlchemy engine
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Test connection
try:
    with engine.connect() as conn:
        print("Connected to Aiven PostgreSQL database successfully!")
except Exception as e:
    print(f"Connection failed: {e}")

# # Load CSV file
csv_file = "malaysia_predicted_aqi.csv"
df = pd.read_csv(csv_file)

# # Define table name
table_name = "air_quality"

# # Upload to database
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Data successfully uploaded to {table_name}!")

query = f"SELECT * FROM {table_name} LIMIT 5;"
df = pd.read_sql(query, engine)
print(df)