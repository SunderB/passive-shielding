import periodictable as pt

# Water molecule
water = pt.formula("H2O")
sld, xs, penetration = pt.neutron_scattering(water, density=0.997)

print(water)
print(sld)
print(xs)
print(penetration)