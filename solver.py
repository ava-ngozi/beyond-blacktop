# Beyond Blacktop
# Numerical Integration Solver

import numpy as np
from scipy.integrate import solve_ivp

from simulation import net_energy, temperature_change_rate

from environment import (
    solar_irradiance,
    air_temperature,
    sky_temperature,
    ground_temperature
)

from materials import MATERIALS


def temperature_derivative(t, y, material):
    """Calculate the instantaneous heating rate."""

    hour = t / 3600
    surface_temp = y[0]

    net_flux = net_energy(
        material,
        solar_irradiance(hour),
        surface_temp,
        air_temperature(hour),
        sky_temperature(hour),
        ground_temperature(hour)
    )

    rate = temperature_change_rate(
        material, net_flux
    )

    return [rate]


def simulate_day(material, initial_temp=28.0):
    """Simulate 24 hours of pavement temperatures."""

    duration = 24 * 3600

    time_points = np.linspace(
        0, duration, 289
    )

    solution = solve_ivp(
        fun=temperature_derivative,
        t_span=(0, duration),
        y0=[initial_temp],
        args=(material,),
        t_eval=time_points,
        method="RK45",
        rtol=1e-6,
        atol=1e-8,
        max_step=300
    )

    if not solution.success:
        raise RuntimeError(solution.message)

    return solution.t / 3600, solution.y[0]


if __name__ == "__main__":
    
    peak_temperatures = {}

    for material in MATERIALS.values():

        hours, temperatures = simulate_day(material)

        print(material.name)

        print(
            f"Maximum: {np.max(temperatures):.2f} C"
        )

        print(
            f"Minimum: {np.min(temperatures):.2f} C"
        )

        print(
            f"Average: {np.mean(temperatures):.2f} C"
        )

        print("-" * 40)
        peak_index = np.argmax(temperatures)
        peak_hour = hours[peak_index]

        print(f"Peak temperature occurs at: {peak_hour:.2f} hours")
        print(
            f"The daily temperature range is: {np.ptp(temperatures):2f} C"
        )
        peak_temperatures[material.name] = np.max(temperatures)
        
    asphalt_peak = peak_temperatures["Traditional Asphalt"]
    reflective_peak = peak_temperatures["Reflective Pavement"]
    
    peak_difference = asphalt_peak - reflective_peak
    
    print("=" * 40)
    print("COMPARATIVE ANALYSIS")
    print(f"Peak temperature reduction: {peak_difference:.2f} C")