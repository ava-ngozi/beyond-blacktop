# Beyond Blacktop
# Version 0.2: Solar energy absorption model

# Assumed material albedo values
materials = {
    "Traditional Asphalt": 0.08,
    "Conventional Concrete": 0.30,
    "Reflective Pavement": 0.50
}

# 1. Reject albedo values outside the 0 to 1 range
for material, albedo in materials.items():
    if not (0 <= albedo <= 1):
        raise ValueError(f"Error: Albedo for {material} is {albedo}. It must be between 0 and 1.")

def absorbed_energy(albedo, irradiance):
    return (1 - albedo) * irradiance

print("BEYOND BLACKTOP")
print("Solar Energy Absorption Analysis")
print("-" * 40)

# 2. User inputs their own solar irradiance with validation for negative values
while True:
    try:
        solar_irradiance = float(input("Enter the solar irradiance in W/m²: "))
        if solar_irradiance < 0:
            print("Error: Irradiance cannot be negative. Please try again.")
        else:
            break
    except ValueError:
        print("Error: Invalid input. Please enter a valid number.")

print("-" * 40)

# Establish the baseline absorption for Traditional Asphalt
asphalt_albedo = materials["Traditional Asphalt"]
asphalt_absorbed = absorbed_energy(asphalt_albedo, solar_irradiance)

# 3. Calculate and display results with percentage comparisons
for material, albedo in materials.items():
    absorbed = absorbed_energy(albedo, solar_irradiance)

    if material == "Traditional Asphalt":
        print(f"{material}: {absorbed:.2f} W/m² (Baseline)")
    else:
        # Prevent ZeroDivisionError if the user inputs 0 for irradiance
        if asphalt_absorbed > 0:
            percent_less = ((asphalt_absorbed - absorbed) / asphalt_absorbed) * 100
        else:
            percent_less = 0.0

        print(f"{material}: {absorbed:.2f} W/m² ({percent_less:.1f}% less than asphalt)")