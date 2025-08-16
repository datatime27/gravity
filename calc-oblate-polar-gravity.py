import math
G = 6.67430e-11  # Gravitational constant (m³ kg⁻¹ s⁻²)

# (x²+y²)/a² + z²/c² = 1
#(x²+y²)/a²  = 1 - z²/c²
#(x²+y²)  = a²(1 - z²/c²)
#sqrt(x²+y²)  = a * sqrt(1 - z²/c²)
#r  = a * sqrt(1 - z²/c²)


def volume(a,c):
    return (4/3) * math.pi * a**2 * c
  
# V = (4/3) * math.pi * a**2 * c
# a**2 = V / ((4/3) * math.pi * c)
# a = sqrt(V / ((4/3) * math.pi * c))
def find_equator_radius(V_earth, c_pole):
  return math.sqrt(V_earth/((4/3)*math.pi * c_pole))

def disk_gravity(R, z, t, rho):
    """
    Calculate the gravitational acceleration (g_z) due to a uniform disk.
    """
    if z == 0:
        term = 0
    else:
        term = z / math.sqrt(z**2 + R**2)
    return 2 * math.pi * G * rho * t * (1 - term)
  
def disk_mass(R, dz, rho):
    return dz * rho * math.pi * R**2

def ellipsoid_gravity(a, c, rho, num_slices):
    """
    Calculate gravity for an oblate spheroid (ellipsoid)
    a = radius along axis down from where we are standing
    c = radius of perpendicular axis
    """
    total_g = 0.0
    total_m = 0.0
    dz = 2 * c / num_slices  # Integration step along polar axis
   
    for i in range(num_slices):
        # Current z position within ellipsoid (-c to c)
        z_disk = -c + (i + 0.5) * dz
       
        # Distance from observation point to this disk
        distance = c - z_disk
       
        # Radius of the disk at position z_disk (ellipsoid cross-section)
        if abs(z_disk) > c:
            r_disk = 0
        else:
            # Equation for oblate spheroid: (x²+y²)/a² + z²/c² = 1
            r_disk = a * math.sqrt(1 - (z_disk**2 / c**2))
       
        if r_disk > 0:
            g = disk_gravity(r_disk, distance, dz, rho)
            m = disk_mass(r_disk, dz, rho)
            total_g += g
            total_m += m
    
    return total_g, total_m


# Parameters
M_earth = 5.972365357e24 # mass of earth in kg
a_equator = 6378e3  # equatorial radius (m)
c_pole = 6356e3     # polar radius (m)
V_earth = volume(a_equator,c_pole)
print(f"V_earth: {V_earth}")
rho_earth = M_earth / V_earth
#rho_earth = 5515    # kg/m³
print(f"rho_earth: {rho_earth}")


# Compute gravity at North Pole (no centrifugal effect)
g_pole, total_m = ellipsoid_gravity(a_equator, c_pole, rho_earth,num_slices=10_000)
print("Compute gravity at North Pole of Earth (no centrifugal effect)")
print(f"a_equator: {a_equator}")
print(f"c_pole: {c_pole}")
print(f"Gravity at North Pole (pure gravity): {g_pole:.6f} m/s²")
print(f"Total mass {total_m}")
print()
#Mass_ratio = total_m/M_earth
#print(f"Mass_ratio: {Mass_ratio:.12f}")

print("Compute gravity at North Pole of Various Spheriods (no centrifugal effect)")
print("Equatorial radius (m), Polar radius (m), Gravity (m/s²)")
for c_pole in range(3000_000,7000_000,10_000):
  a_equator = find_equator_radius(V_earth, c_pole)
  g_pole, total_m = ellipsoid_gravity(a_equator, c_pole, rho_earth, num_slices=10_000)
  print(a_equator, c_pole, g_pole)
