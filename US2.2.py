import streamlit as st
import pandas as pd
import psycopg2
import sqlalchemy

# 🔑 Database Credentials
DB_HOST = "fit5120-fit5120.e.aivencloud.com"
DB_PORT = "19305"
DB_NAME = "defaultdb"
DB_USER = "avnadmin"
DB_PASS = "AVNS_rEaABFKKIHR8O6Sxp6m"

# 📌 Function to Establish a Database Connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Create a database connection using SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = sqlalchemy.create_engine(DATABASE_URL)

def fetch_data(query_text):
    query = sqlalchemy.text(query_text)
    with engine.connect() as connection:
        result = connection.execute(query)
        data = pd.DataFrame(result, columns=["ID", "State", "City", "Date", "AQI"])
        return data

# 🔄 Load AQI Data from PostgreSQL
@st.cache_data
def load_data():
    conn = get_db_connection()
    query = "SELECT * FROM air_quality ORDER BY date DESC;"  # 确保数据库中存在该表
    df = fetch_data(query)
    # 格式化日期
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df

df = load_data()

# Title
st.title("🌍 Malaysia AQI Prediction for Asthmatic Travelers 🏥")
st.write("Check the air quality before planning your trip!")

# Select travel date
selected_date = st.date_input("📅 Select travel date")



# Filter data based on date
filtered_data = df[df["Date"] == selected_date]


print(filtered_data)
# Select cities (default: empty)
all_cities = filtered_data["City"].unique()
selected_cities = st.multiselect("🏙️ Select cities", all_cities, default=[])
print(selected_cities)

# Filter by selected cities
if selected_cities:
    filtered_data = filtered_data[filtered_data["City"].isin(selected_cities)]
else:
    st.warning("⚠️ Please select at least one city to view AQI data.")

# Sort cities by AQI (best to worst) and add ranking
if not filtered_data.empty:
    sorted_data = filtered_data.sort_values(by="AQI").reset_index(drop=True)
    sorted_data.insert(0, "Rank", range(1, len(sorted_data) + 1))  # Add ranking column
else:
    sorted_data = pd.DataFrame()

# User input: child's asthma severity
asthma_severity = st.radio(
    "🏥 Select your child's asthma severity:",
    ["Mild", "Moderate", "Severe"],
    index=0
)

# Display AQI sorted list with ranking
if not sorted_data.empty:
    st.subheader("📊 Recommended Cities (Best Air Quality First)")

    # Apply AQI color coding
    def highlight_aqi(val):
        if val <= 50:
            return 'background-color: lightgreen; color: black; font-weight: bold;'
        elif val <= 100:
            return 'background-color: yellow; color: black; font-weight: bold;'
        return 'background-color: red; color: white; font-weight: bold;'


    # Show styled table
    st.dataframe(
        sorted_data[["Rank", "State", "City", "AQI"]]
        .style.applymap(highlight_aqi, subset=['AQI'])
        .set_properties(**{'text-align': 'center'})
    )

    # Personalized recommendation
    st.subheader("🌟 Personalized Recommendation")
    best_city = sorted_data.iloc[0]["City"]
    st.write(f"✅ Based on the air quality, we recommend visiting **{best_city}**.")

    # Travel advice based on asthma severity
    if asthma_severity == "Severe":
        st.warning("⚠️ High risk: Always carry an inhaler, wear a mask, and avoid high AQI areas.")
    elif asthma_severity == "Moderate":
        st.info("🟡 Medium risk: Prefer indoor activities and check AQI frequently.")
    else:
        st.success("✅ Low risk: Outdoor activities are fine, but avoid pollution hotspots.")
else:
    st.info("📍 No cities selected yet. Please choose a city to see recommendations.")

# Asthma travel tips
st.subheader("🚀 Asthma Travel Tips")
st.markdown("""
- 🌿 **Check the AQI before traveling** and avoid high pollution areas.
- 💊 **Carry asthma medication**, including an inhaler.
- 🚗 **Use air-conditioned transport** to reduce dust exposure.
- 🏨 **Stay in non-smoking hotels** to prevent asthma triggers.
- 🕶️ **Wear a mask** in crowded or polluted areas.
""")

# Download AQI data
st.download_button(
    label="📥 Download AQI Data",
    data=df.to_csv(index=False),
    file_name="Malaysia_AQI_Prediction.csv",
    mime="text/csv"
)
