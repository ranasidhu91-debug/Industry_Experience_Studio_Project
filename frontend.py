import streamlit as st

def get_geolocation():
    """Injects JavaScript to get the user's latitude & longitude and ensures Streamlit receives it."""
    html_code = """
        <script>
        function getLocation() {
            navigator.geolocation.getCurrentPosition(
                function (position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;

                    // Store location in session storage (to persist across refresh)
                    sessionStorage.setItem("latitude", lat);
                    sessionStorage.setItem("longitude", lon);

                    // Inject location values into form and submit automatically
                    document.getElementById("lat").value = lat;
                    document.getElementById("lon").value = lon;
                    document.getElementById("geo-form").submit();
                },
                function (error) {
                    document.getElementById("manual-input").style.display = "block";  // Show manual input fields if permission denied
                }
            );
        }

        // If location was previously stored, reuse it
        window.onload = function () {
            if (sessionStorage.getItem("latitude") && sessionStorage.getItem("longitude")) {
                document.getElementById("lat").value = sessionStorage.getItem("latitude");
                document.getElementById("lon").value = sessionStorage.getItem("longitude");
                document.getElementById("geo-form").submit();
            } else {
                getLocation();
            }
        };
        </script>

        <form id="geo-form" action="" method="post">
            <input type="hidden" id="lat" name="lat">
            <input type="hidden" id="lon" name="lon">
        </form>

        <div id="manual-input" style="display:none;">
            <p>🔴 Location access denied. Please enter ZIP code & country:</p>
            <input type="text" id="zip_code" placeholder="ZIP Code">
            <input type="text" id="country_code" placeholder="Country Code (e.g., US, MY)">
            <button onclick="submitManualLocation()">Submit</button>
        </div>

        <script>
        function submitManualLocation() {
            let zip = document.getElementById("zip_code").value;
            let country = document.getElementById("country_code").value;
            if (zip && country) {
                document.getElementById("lat").value = "manual";
                document.getElementById("lon").value = zip + "," + country;
                document.getElementById("geo-form").submit();
            }
        }
        </script>
    """
    st.components.v1.html(html_code, height=250)
