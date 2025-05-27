import streamlit as st
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # For accurate timezone handling

# List of all resource types used in the game
resources = ["Supplies", "Components", "Fuel", "Electronics", "Rare Material", "ManPower", "Money"]

# Web app title and instructions for the user
st.title("Game Resource Planner")
st.markdown("*Only fill in applicable resources. Leave others blank if resource is enough.*")

# Dictionaries to hold user input
current = {}     # Current amount of each resource
production = {}  # Hourly production rate
cost = {}        # Cost needed to buy the unit

# Input fields for each resource
for res in resources:
    st.markdown(f"### {res}")
    current[res] = st.number_input(f"{res} - Current", value=0.0, key=f"{res}_current")
    production[res] = st.number_input(f"{res} - Hourly Production", value=0.0, key=f"{res}_prod")
    cost[res] = st.number_input(f"{res} - Cost to Buy Unit", value=0.0, key=f"{res}_cost")

# Button to trigger calculation
if st.button("Calculate Time"):
    max_time = 0.0  # Will hold the longest time needed among all resources

    # Loop through each resource to compute needed time
    for res in resources:
        if cost[res] > current[res]:  # If we need more than we have
            needed = cost[res] - current[res]
            if production[res] > 0:
                time_needed = needed / production[res]
                max_time = max(max_time, time_needed)
            else:
                max_time = float('inf')  # Cannot produce this resource at all

    # Output result to the user
    if max_time == float('inf'):
        st.error("Some resources cannot be produced — infinite wait.")
    else:
        # Convert float hours into hrs and mins
        hrs = int(max_time)
        mins = int((max_time - hrs) * 60)

        # Get estimated local time when the unit can be bought
        your_zone = ZoneInfo("Asia/Kuala_Lumpur")  # Change this to your time zone if needed
        eta = datetime.now(tz=your_zone) + timedelta(hours=max_time)
        eta_str = eta.strftime("%b %d, %I:%M %p")  # Friendly format

        # Display the result
        st.success(f"Time until unit affordable: {hrs}h {mins}m\nAvailable at: {eta_str}")
