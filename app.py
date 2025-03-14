import streamlit as st
import psycopg2
import os

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

st.title("📊 My Streamlit App with PostgreSQL")

# Query Example
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT 'Hello from PostgreSQL!'")
result = cursor.fetchone()
st.write(result[0])

cursor.close()
conn.close()

if __name__ == "__main__":
    import os
    # Make sure the Streamlit listens to 0.0.0.0
    port = int(os.getenv("PORT", 8501))
    os.system(f"streamlit run app.py --server.address 0.0.0.0 --server.port {port}")
