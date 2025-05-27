import streamlit as st
from datetime import datetime, timedelta

resources = ["Supplies", "Components", "Fuel", "Electronics", "Rare Material", "ManPower", "Money"]

st.title("Game Resource Planner")
st.markdown("*Only fill in applicable resources. Leave others blank.*")

current = {}
production = {}
cost = {}

for res in resources:
    st.markdown(f"### {res}")
    current[res] = st.number_input(f"{res} - Current", value=0.0, key=f"{res}_current")
    production[res] = st.number_input(f"{res} - Hourly Production", value=0.0, key=f"{res}_prod")
    cost[res] = st.number_input(f"{res} - Cost to Buy Unit", value=0.0, key=f"{res}_cost")

if st.button("Calculate Time"):
    max_time = 0.0
    for res in resources:
        if cost[res] > current[res]:
            needed = cost[res] - current[res]
            if production[res] > 0:
                time_needed = needed / production[res]
                max_time = max(max_time, time_needed)
            else:
                max_time = float('inf')

    if max_time == float('inf'):
        st.error("Some resources cannot be produced — infinite wait.")
    else:
        hrs = int(max_time)
        mins = int((max_time - hrs) * 60)
        eta = datetime.now() + timedelta(hours=max_time)
        eta_str = eta.strftime("%b %d, %I:%M %p").lstrip('0')
        st.success(f"Time until unit affordable: {hrs}h {mins}m\nAvailable at: {eta_str}")
