# Beyond Blacktop
# Material Sensitivity Analysis

from dataclasses import replace

import numpy as np
import pandas as pd

from materials import ASPHALT
from solver import simulate_day


def albedo_sensitivity(initial_temp=28.0):
    """Investigate the effect of albedo on pavement temperature."""

    albedo_values = np.linspace(0, 1, 21)

    results = []

    for albedo in albedo_values:

        modified_material = replace(
            ASPHALT,
            albedo=float(albedo)
        )

        hours, temperatures = simulate_day(
            modified_material,
            initial_temp=initial_temp
        )

        peak = float(np.max(temperatures))
        average = float(np.mean(temperatures))

        results.append({
            "Albedo": albedo,
            "Peak Temperature": peak,
            "Average Temperature": average
        })

    return pd.DataFrame(results)


if __name__ == "__main__":
    print(albedo_sensitivity().round(2))
