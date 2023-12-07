import periodictable as pt

# Water molecule
water = pt.formula("H2O")
sld, xs, penetration = pt.neutron_scattering(water, density=1, energy=25.3e-3)
print(sld)
print(xs)
print(penetration)