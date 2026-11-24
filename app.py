# Beyond Blacktop
# Interactive Scientific Dashboard

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from materials import MATERIALS
from solver import simulate_day
from environment import air_temperature


st.set_page_config(
    page_title="Beyond Blacktop",
    page_icon="🌡️",
    layout="wide"
)

COLORS = {
    "Traditional Asphalt": "#C65F45",
    "Conventional Concrete": "#D4AA65",
    "Reflective Pavement": "#438E79"
}

st.caption("COMPUTATIONAL MATERIALS SCIENCE")

st.title("Beyond Blacktop")

st.subheader(
    "Rethinking the surfaces beneath our cities."
)

st.write(
    "An interactive computational investigation "
    "of pavement materials and urban heat."
)

st.sidebar.header("Simulation Settings")

initial_temp = st.sidebar.slider(
    "Initial pavement temperature (°C)",
    min_value=15.0,
    max_value=45.0,
    value=28.0,
    step=0.5
)

material_names = list(MATERIALS.keys())

selected = st.sidebar.multiselect(
    "Select pavement materials",
    options=material_names,
    default=material_names,
    format_func=lambda key: MATERIALS[key].name
)

show_air = st.sidebar.checkbox(
    "Show ambient air temperature",
    value=True
)

st.sidebar.info(
    "Environmental conditions represent "
    "a hypothetical summer day in Houston."
)

if not selected:
    st.warning("Please select at least one material.")
    st.stop()

results = []
export_data = {}

fig, ax = plt.subplots(figsize=(12, 6))

st.header("Peak Surface Temperatures")

columns = st.columns(len(selected))

for i, key in enumerate(selected):

    material = MATERIALS[key]

    hours, temperatures = simulate_day(
        material,
        initial_temp=initial_temp
    )

    peak = float(np.max(temperatures))
    minimum = float(np.min(temperatures))
    average = float(np.mean(temperatures))

    peak_hour = float(
        hours[np.argmax(temperatures)]
    )

    columns[i].metric(
        material.name,
        f"{peak:.2f} °C"
    )

    ax.plot(
        hours,
        temperatures,
        label=material.name,
        color=COLORS[material.name],
        linewidth=2.5
    )

    results.append({
        "Material": material.name,
        "Maximum (°C)": peak,
        "Minimum (°C)": minimum,
        "Average (°C)": average,
        "Peak Hour": peak_hour,
        "Daily Range (°C)": peak - minimum
    })

    export_data["Hour"] = hours
    export_data[material.name] = temperatures

if show_air:

    air_temps = [
        air_temperature(h) for h in hours
    ]

    ax.plot(
        hours,
        air_temps,
        label="Ambient Air Temperature",
        color="gray",
        linestyle="--",
        linewidth=1.8
    )

    export_data["Ambient Air Temperature"] = air_temps

ax.set_title(
    "24-Hour Surface Temperature Comparison"
)

ax.set_xlabel("Hour of Day")
ax.set_ylabel("Temperature (°C)")

ax.set_xlim(0, 24)
ax.set_xticks(np.arange(0, 25, 3))

ax.grid(alpha=0.2)
ax.legend()

fig.tight_layout()

st.header("Daily Thermal Behavior")

st.pyplot(fig)

plt.close(fig)

st.header("Comparative Analysis")

df = pd.DataFrame(results)

st.dataframe(
    df.round(2),
    hide_index=True
)

if "asphalt" in selected and "reflective" in selected:

    asphalt_peak = df.loc[
        df["Material"] == "Traditional Asphalt",
        "Maximum (°C)"
    ].iloc[0]

    reflective_peak = df.loc[
        df["Material"] == "Reflective Pavement",
        "Maximum (°C)"
    ].iloc[0]

    reduction = asphalt_peak - reflective_peak

    st.metric(
        "Peak Temperature Reduction",
        f"{reduction:.2f} °C"
    )

st.header("Export Simulation Results")

export_df = pd.DataFrame(export_data)

st.download_button(
    label="Download Temperature Data (CSV)",
    data=export_df.to_csv(index=False),
    file_name="beyond_blacktop_results.csv",
    mime="text/csv"
)

with st.expander("Scientific Methodology"):

    st.write(
        "This simulation uses a simplified surface "
        "energy balance accounting for solar "
        "absorption, thermal radiation, convection "
        "and conduction."
    )

    st.latex(
        r"C_A\frac{dT}{dt}"
        r"=Q_{solar}-Q_{rad}-Q_{conv}-Q_{cond}"
    )

    st.write(
        "The differential equation is solved using "
        "SciPy's adaptive RK45 numerical integration "
        "algorithm."
    )

with st.expander("Model Limitations"):

    st.write(
        "The environmental conditions are synthetic "
        "and the material properties are preliminary "
        "assumptions. This model has not been "
        "validated against experimental measurements. "
        "It does not account for evaporative cooling, "
        "traffic, shading, or changes in wind speed."
    )

st.divider()

st.caption(
    "Beyond Blacktop | Independent Computational "
    "Materials Science Project | Ava Williams"
)