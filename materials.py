# Beyond Blacktop
# Material Property Database
# Preliminary assumptions for model development

from dataclasses import dataclass


@dataclass(frozen=True)
class PavementMaterial:
    name: str
    albedo: float
    emissivity: float
    density: float
    specific_heat: float
    thermal_conductivity: float
    def volumetric_heat_capacity(self):
        """Calculates volumetric heat capacity (J/m³·K)."""
        return self.density * self.specific_heat
    

ASPHALT = PavementMaterial(
    name="Traditional Asphalt",
    albedo=0.08,
    emissivity=0.95,
    density=2300,
    specific_heat=920,
    thermal_conductivity=0.75
)

CONCRETE = PavementMaterial(
    name="Conventional Concrete",
    albedo=0.30,
    emissivity=0.90,
    density=2400,
    specific_heat=880,
    thermal_conductivity=1.40
)

REFLECTIVE = PavementMaterial(
    name="Reflective Pavement",
    albedo=0.50,
    emissivity=0.90,
    density=2300,
    specific_heat=920,
    thermal_conductivity=0.75
)

MATERIALS = {
    "asphalt": ASPHALT,
    "concrete": CONCRETE,
    "reflective": REFLECTIVE
}
