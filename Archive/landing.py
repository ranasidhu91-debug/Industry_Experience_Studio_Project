import streamlit as st

# Set a predefined password (consider using environment variables for security)
PASSWORD = "tm01"

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Show login screen if not authenticated
if not st.session_state.authenticated:
    st.sidebar.header("🔒 Login Required")
    password = st.sidebar.text_input("Enter Password", type="password")

    if st.sidebar.button("Login"):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.sidebar.success("✅ Access Granted!")
            st.rerun()
        else:
            st.sidebar.error("❌ Incorrect Password")

# If authenticated, run the main app
if st.session_state.authenticated:
    # --- PAGE SETUP ---
    about_page = st.Page(
        "pages/about_me.py",
        title="About Us",
        icon="🏠",
        default=True,
    )
    project_1_page = st.Page(
        "pages/US1.2.py",
        title="Real Time Monitoring",
        icon="📊",
    )
    project_2_page = st.Page(
        "pages/US2.2.py",
        title="Route Planning",
        icon="🗺️",
    )

    # --- NAVIGATION SETUP ---
    pg = st.navigation(
        {
            "Info": [about_page],
            "Projects": [project_1_page, project_2_page],
        }
    )

    # --- SHARED ON ALL PAGES ---
    st.logo("Lungs_of_Tomorrow_with_logo.png", size="large")
    # st.sidebar.markdown("Lungs of Tomorrow - TM01")

    # with st.sidebar:
    #     country = st.selectbox("Country", ["Malaysia"], index=0)


    # --- RUN NAVIGATION ---
    pg.run()
