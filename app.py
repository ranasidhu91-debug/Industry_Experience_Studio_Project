import streamlit as st
import psycopg2
import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine, text  # Import text correctly

# ==== 🔹 1. Connecting to a PostgreSQL Database ====
# Database connection information
DB_HOST = "fit5120-fit5120.e.aivencloud.com"
DB_PORT = "19305"
DB_NAME = "defaultdb"
DB_USER = "avnadmin"
DB_PASS = "AVNS_rEaABFKKIHR8O6Sxp6m"

# ==== 🔹 2. Create a Database Table ====
# Create a database connection using SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = sqlalchemy.create_engine(DATABASE_URL)

# Create data table
def create_table():
    query = sqlalchemy.text("""
        CREATE TABLE IF NOT EXISTS air_quality (
            id SERIAL PRIMARY KEY,
            state TEXT,
            city TEXT,
            date DATE,
            aqi INT
        );
    """)  # Parse SQL statements with sqlalchemy.text()

    with engine.connect() as connection:
        connection.execute(query)  # Execute SQL statement
        connection.commit()  # Submit changes

    # st.success("✅ The data table has been created！")

# Run the create table function
create_table()

# ==== 🔹 3. Importing data from a CSV file to PostgreSQL (run only once) ====
def import_csv_to_db():
    csv_file = "malaysia_predicted_aqi.csv" 
    df = pd.read_csv(csv_file)

    # Make sure the date format is correct
    df["date"] = pd.to_datetime(df["date"])

    with engine.connect() as connection:
        for _, row in df.iterrows():
            # Check whether the same record already exists in the database
            check_query = f"""
            SELECT COUNT(*) FROM air_quality
            WHERE state = '{row['state']}' 
            AND city = '{row['city']}' 
            AND date = '{row['date']}' 
            AND aqi = {row['aqi']};
            """
            result = connection.execute(check_query).scalar()
            
            # Insert this data only if it is not in the database
            if result == 0:
                insert_query = f"""
                INSERT INTO air_quality (state, city, date, aqi) 
                VALUES ('{row['state']}', '{row['city']}', '{row['date']}', {row['aqi']});
                """
                connection.execute(insert_query)

    st.success("✅ Data has been imported and duplicate import is prevented!")

# ==== 🔹 4. Query and present the data in the database ====
def fetch_data():
    query = sqlalchemy.text("SELECT * FROM air_quality ORDER BY date DESC LIMIT 100")
    with engine.connect() as connection:
        result = connection.execute(query)
        return result.fetchall()

# Display query results
st.title("🌍 Air quality query system")
st.write("📊 Recent air quality data:")

data = fetch_data()
df = pd.DataFrame(data, columns=["ID", "State", "City", "Date", "AQI"])
st.dataframe(df)
