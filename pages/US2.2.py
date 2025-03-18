import streamlit as st
import pandas as pd
import psycopg2
import sqlalchemy
import pydeck as pdk

# 🔑 Database Credentials
# DB_HOST = "fit5120-fit5120.e.aivencloud.com"
# DB_PORT = "19305"
# DB_NAME = "defaultdb"
# DB_USER = "avnadmin"
# DB_PASS = "AVNS_rEaABFKKIHR8O6Sxp6m"

DB_HOST = "tm01onboarding-tm01onboarding.e.aivencloud.com"
DB_PORT = "13812"
DB_NAME = "defaultdb"
DB_USER = "avnadmin"
DB_PASS = "AVNS_AFmtCZU-RoKIAHPUNUx"


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
        data = pd.DataFrame(result, columns=["State", "City", "Date", "AQI"]) #"ID", 
        return data


# 🔄 Load AQI Data from PostgreSQL
@st.cache_data
def load_data():
    conn = get_db_connection()
    query = "SELECT * FROM air_quality ORDER BY date DESC;"
    df = fetch_data(query)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df

df = load_data()

# Load predicted Data city locations
@st.cache_data
def load_city_cords():
    city_df = pd.read_csv("perdicted_city_lat_lon.csv")  # Update with your file path
    return city_df

city_df = load_city_cords()


# Title
st.title("🌍 Malaysia AQI Prediction for Asthmatic Travelers 🏥")
st.write("Check the air quality before planning your trip!")

# Select travel date
selected_date = st.date_input("📅 **Select Travel Date**")

# Filter data based on date
filtered_data = df[df["Date"] == selected_date]

# Select state
all_states = filtered_data["State"].unique()
selected_states = st.multiselect("🌏 **Select State(s)**", all_states)

# Filter by selected states
filtered_data = filtered_data[filtered_data["State"].isin(selected_states)]

# Select cities dynamically based on selected states
all_cities = filtered_data["City"].unique()
selected_cities = st.multiselect("🏙️ **Select City(ies)**", all_cities)

# Filter by selected cities
city_df_select = city_df[city_df["City"].isin(selected_cities)]
# st.write(city_df_select)

filtered_data = filtered_data[filtered_data["City"].isin(selected_cities)]
# st.write(filtered_data)

# merge aqi dataframe and coordinate dataframe
df_merged = pd.merge(city_df_select, filtered_data, on=["State", "City"], how="left")
st.write(df_merged)

# Sort cities by AQI (best to worst) and add ranking
if not filtered_data.empty:
    sorted_data = filtered_data.sort_values(by="AQI").reset_index(drop=True)
    sorted_data.insert(0, "Rank", range(1, len(sorted_data) + 1))
else:
    sorted_data = pd.DataFrame()
    st.warning("⚠️ No data available for the selected date, state, or city!")

# User input: child's asthma severity
asthma_severity = st.radio(
    "🏥 **Select Your Child's Asthma Severity**:",
    ["Mild", "Moderate", "Severe"],
    index=0
)

# Display AQI sorted list with ranking
if not sorted_data.empty:
    st.subheader("📊 **Recommended Cities (Best Air Quality First)**")


    def highlight_aqi(val):
        if val <= 50:
            return 'background-color: lightgreen; color: black; font-weight: bold;'
        elif val <= 100:
            return 'background-color: yellow; color: black; font-weight: bold;'
        return 'background-color: red; color: white; font-weight: bold;'


    st.dataframe(
        sorted_data[["Rank", "State", "City", "AQI"]]
        .style.applymap(highlight_aqi, subset=['AQI'])
        .set_properties(**{'text-align': 'center'})
    )

    # Personalized recommendation
    st.subheader("🌟 **Personalized Recommendation**")
    best_city = sorted_data.iloc[0]["City"]
    st.write(f"✅ Based on the air quality, we recommend visiting **{best_city}**.")

    # Travel advice based on asthma severity
    if asthma_severity == "Severe":
        st.warning("⚠️ High risk: Always carry an inhaler, wear a mask, and avoid high AQI areas.")
    elif asthma_severity == "Moderate":
        st.info("🟡 Medium risk: Prefer indoor activities and check AQI frequently.")
    else:
        st.success("✅ Low risk: Outdoor activities are fine, but avoid pollution hotspots.")

# Asthma travel tips
st.subheader("🚀 **Asthma Travel Tips**")
st.markdown("""
- 🌿 **Check the AQI before traveling** and avoid high pollution areas.
- 💊 **Carry asthma medication**, including an inhaler.
- 🚗 **Use air-conditioned transport** to reduce dust exposure.
- 🏨 **Stay in non-smoking hotels** to prevent asthma triggers.
- 🕶️ **Wear a mask** in crowded or polluted areas.
""")

# Define Pydeck layer
print(df_merged)
print(type(df_merged))

df_merged_2 = pd.DataFrame({
    "state": df_merged["State"].tolist(),
    "city": df_merged["City"].tolist(),
    "latitude": df_merged["Latitude"].tolist(),
    "longitude": df_merged["Longitude"].tolist(),
    "aqi": df_merged["AQI"].tolist()
})


# Define Pydeck Layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_merged_2,
    get_position=["longitude", "latitude"],  # Ensure correct order
    get_color=["aqi * 2", "255 - (aqi * 2)", "0", "180"],  # Example color mapping
    get_radius=10000,
    pickable=True
)

# Define View
view_state = pdk.ViewState(
    latitude=df_merged_2["latitude"].mean(),
    longitude=df_merged_2["longitude"].mean(),
    zoom=7,
    pitch=0
)

# Render Pydeck Map
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "City: {city}\nAQI: {aqi}"}
))

