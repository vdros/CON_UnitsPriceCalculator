import streamlit as st
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # For accurate timezone handling

# List of all resource types used in the game
resources = ["Supplies", "Components", "Fuel", "Electronics", "Rare Material", "ManPower", "Money"]

# Web app title and instructions for the user
st.title("Game Resource Planner")
st.markdown("*Only fill in applicable resources. Leave others blank if resource is enough.*")

# 🌍 Let user pick a timezone from a list of common zones
st.markdown("### 🌍 Select Your Time Zone")
timezones = [
    "UTC", "Asia/Kuala_Lumpur", "Asia/Jakarta", "Asia/Tokyo",
    "Europe/London", "Europe/Berlin", "America/New_York", "America/Los_Angeles"
]
selected_zone = st.selectbox("Choose your time zone:", timezones, index=timezones.index("Asia/Kuala_Lumpur"))
your_zone = ZoneInfo(selected_zone)

# Dictionaries to hold user input
current = {}
production = {}
cost = {}

# Resource input fields
for res in resources:
    st.markdown(f"### {res}")
    current[res] = st.number_input(f"{res} - Current", value=0.0, key=f"{res}_current")
    daily_total = st.number_input(f"{res} - Daily Production (optional)", value=0.0, key=f"{res}_daily")
    
    if daily_total > 0:
        production[res] = daily_total / 24
        st.markdown(f"➡️ Using {production[res]:.2f} per hour from daily total")
    else:
        production[res] = st.number_input(f"{res} - Hourly Production", value=0.0, key=f"{res}_prod")

    cost[res] = st.number_input(f"{res} - Cost to Buy Unit", value=0.0, key=f"{res}_cost")

# Button to trigger the calculation
if st.button("Calculate Time"):
    max_time = 0.0  # Track the longest wait time among all needed resources

    for res in resources:
        if cost[res] > current[res]:
            needed = cost[res] - current[res]
            if production[res] > 0:
                time_needed = needed / production[res]
                max_time = max(max_time, time_needed)
            else:
                max_time = float('inf')  # Can't be produced at all

    if max_time == float('inf'):
        st.error("Some resources cannot be produced — infinite wait.")
    else:
        # Convert hours to readable format
        hrs = int(max_time)
        mins = int((max_time - hrs) * 60)

        eta = datetime.now(tz=your_zone) + timedelta(hours=max_time)
        eta_str = eta.strftime("%b %d, %I:%M %p")

        # Show current time info
        current_time = datetime.now(tz=your_zone)
        current_time_str = current_time.strftime("%b %d, %I:%M %p")
        st.info(f"🕒 Current system time used: {current_time_str} ({your_zone.key})")

        # Final result
        st.success(f"Time until unit affordable: {hrs}h {mins}m\nAvailable at: {eta_str}")
