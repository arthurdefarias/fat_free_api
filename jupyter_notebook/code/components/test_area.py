import math

pi = math.pi

diameter = 0.3228
steel_thickness = 0.0150
concrete_thickness = 0.0100
coating_thickness = 0.003

diameter_intern_steel = diameter - 2*steel_thickness  # Exemplo
diameter_outer_steel = diameter
diameter_outer = diameter_outer_steel + 2 * concrete_thickness + 2 * coating_thickness  # Confirmar se está correto

# Cálculo das áreas
area_intern = pi * ((diameter_intern_steel / 2) ** 2)
area_steel = pi * ((diameter_outer_steel / 2) ** 2 - (diameter_intern_steel / 2) ** 2)

diameter_outer_concrete = diameter_outer_steel + 2 * concrete_thickness
area_concrete = pi * ((diameter_outer_concrete / 2) ** 2 - (diameter_outer_steel / 2) ** 2)

area_coating = pi * ((diameter_outer / 2) ** 2 - (diameter_outer_concrete / 2) ** 2)

print(f"Área Interna: {area_intern :.6f} m²")
print(f"Área Aço: {area_steel:.6f} m²")
print(f"Área Concreto: {area_concrete:.6f} m²")
print(f"Área Coating: {area_coating:.6f} m²")
print(f"Área Total Externa (soma): {area_steel + area_concrete + area_coating:.6f} m²")