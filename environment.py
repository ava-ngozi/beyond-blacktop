# Beyond Blacktop
# Environmental Conditions Model
# Hypothetical summer day in Houston

import numpy as np


def solar_irradiance(hour):
    """Simulate sunlight throughout a 24-hour day."""

    if 6 <= hour <= 18:
        return 1000 * np.sin(
            np.pi * (hour - 6) / 12
        )

    return 0.0


def air_temperature(hour):
    """Simulate daily air temperature in Celsius."""

    return 31 + 6 * np.cos(
        2 * np.pi * (hour - 15) / 24
    )


def sky_temperature(hour):
    """Estimate effective radiative sky temperature."""

    return air_temperature(hour) - 10


def ground_temperature(hour):
    """Assume constant subsurface temperature."""

    return 28.0