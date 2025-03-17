import streamlit as st

# --- HERO SECTION ---
col1, col2 = st.columns([0.5, 0.5], gap="medium", vertical_alignment="center")
with col1:
    st.image("Lungs_of_Tomorrow_with_logo.png", width=None)

with col2:
    st.title("Lungs of Tomorrow", anchor=False)
    st.write("Lungs of Tomorrow helps parents keep their families safe by providing real-time air quality monitoring "
    "and smart route planning. Whether you're heading to school, "
    "the park, or just out for a walk, our app ensures you choose the healthiest path. "
    "Stay informed, avoid pollution hotspots, and protect your little ones with ease"
    )


st.write("\n")

co3, col4 = st.columns([0.7, 0.3], gap="medium", vertical_alignment="center")
with co3:
    st.subheader("Team TM01", anchor=False)
    st.image("team_photo.jpg", width=None)

with col4:
    st.write("\n")
    st.subheader("Members:", anchor=False)
    st.write(
        """
        1. Tan Chien Yuan
        2. 
        3.
        4.
        5.
        6.
        """
    )

