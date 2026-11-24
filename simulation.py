# Beyond Blacktop
# Thermal Energy Balance Model

from materials import PavementMaterial, MATERIALS

# Stefan-Boltzmann constant (W/m²/K⁴)
SIGMA = 5.670374419e-8

# Preliminary environmental assumptions
CONVECTION_COEFFICIENT = 10.0  # W/m²/K
PAVEMENT_DEPTH = 0.10          # meters


def solar_absorption(material, irradiance):
    """Calculate absorbed solar radiation."""
    return (1 - material.albedo) * irradiance


def thermal_radiation(material, surface_temp, sky_temp):
    """Calculate net longwave radiation."""

    # Convert Celsius to Kelvin
    surface_kelvin = surface_temp + 273.15
    sky_kelvin = sky_temp + 273.15

    return material.emissivity * SIGMA * (
        surface_kelvin ** 4 - sky_kelvin ** 4
    )


def convection(surface_temp, air_temp):
    """Calculate convective heat transfer."""
    return CONVECTION_COEFFICIENT * (
        surface_temp - air_temp
    )


def conduction(material, surface_temp, ground_temp):
    """Calculate conductive heat transfer."""
    return material.thermal_conductivity * (
        surface_temp - ground_temp
    ) / PAVEMENT_DEPTH


def net_energy(
    material,
    irradiance,
    surface_temp,
    air_temp,
    sky_temp,
    ground_temp
):
    """Calculate the net surface energy flux."""

    solar = solar_absorption(material, irradiance)

    radiation = thermal_radiation(
        material, surface_temp, sky_temp
    )

    convective = convection(surface_temp, air_temp)

    conductive = conduction(
        material, surface_temp, ground_temp
    )

    return solar - radiation - convective - conductive

def temperature_change_rate(material, net_flux):
    """Calculate temperature change in degrees C per second."""

    heat_capacity = material.volumetric_heat_capacity()

    areal_heat_capacity = heat_capacity * PAVEMENT_DEPTH

    return net_flux / areal_heat_capacity