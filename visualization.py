# Beyond Blacktop
# Scientific Visualization Module

import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from materials import MATERIALS
from solver import simulate_day
from environment import solar_irradiance, air_temperature


COLORS = {
    "Traditional Asphalt": "#C65F45",
    "Conventional Concrete": "#D4AA65",
    "Reflective Pavement": "#438E79"
}


def plot_daily_temperatures():

    fig, ax = plt.subplots(figsize=(12, 7))

    for material in MATERIALS.values():

        hours, temperatures = simulate_day(material)

        ax.plot(
            hours,
            temperatures,
            label=material.name,
            color=COLORS[material.name],
            linewidth=2.5
        )

    ax.set_title(
        "24-Hour Pavement Surface Temperature Comparison",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Surface Temperature (°C)")

    ax.set_xlim(0, 24)
    ax.set_xticks(np.arange(0, 25, 3))

    ax.grid(alpha=0.2)
    ax.legend()

    fig.tight_layout()

    fig.savefig(
        "daily_temperatures.png",
        dpi=300
    )

    plt.close(fig)


def plot_peak_temperatures():

    names = []
    peaks = []
    colors = []

    for material in MATERIALS.values():

        hours, temperatures = simulate_day(material)

        names.append(material.name)
        peaks.append(np.max(temperatures))
        colors.append(COLORS[material.name])

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(
        names,
        peaks,
        color=colors,
        width=0.6
    )

    ax.bar_label(
        bars,
        fmt="%.2f°C",
        padding=5
    )

    ax.set_title(
        "Peak Surface Temperature by Pavement Material",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_ylabel("Temperature (°C)")
    ax.set_ylim(0, max(peaks) + 10)

    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)

    fig.tight_layout()

    fig.savefig(
        "peak_temperatures.png",
        dpi=300
    )

    plt.close(fig)


if __name__ == "__main__":

    plot_daily_temperatures()
    plot_peak_temperatures()

    print("Graphs generated successfully!")
