import streamlit as st

def get_geolocation():
    """Injects JavaScript to get the user's latitude & longitude and allows manual input if denied."""
    html_code = """
        <script>
        function getLocation() {
            navigator.geolocation.getCurrentPosition(
                function (position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    document.getElementById("lat").value = lat;
                    document.getElementById("lon").value = lon;
                    document.getElementById("geo-form").submit();
                },
                function (error) {
                    if (error.code === error.PERMISSION_DENIED) {
                        document.getElementById("manual-input").style.display = "block";  // Show manual input fields
                    }
                }
            );
        }
        getLocation();
        </script>
        <form id="geo-form" action="" method="post">
            <input type="hidden" id="lat" name="lat">
            <input type="hidden" id="lon" name="lon">
        </form>

        <div id="manual-input" style="display:none;">
            <p>🔴 Location access denied. Please enter manually:</p>
            <input type="text" id="manual_address" placeholder="Enter City, Address, or Lat,Lon">
            <button onclick="submitManualLocation()">Submit</button>
        </div>

        <script>
        function submitManualLocation() {
            let address = document.getElementById("manual_address").value;
            if (address) {
                document.getElementById("lat").value = "manual";
                document.getElementById("lon").value = address;
                document.getElementById("geo-form").submit();
            }
        }
        </script>
    """
    st.components.v1.html(html_code, height=200)