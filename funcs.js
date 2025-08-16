const G = 6.67430e-11; // Gravitational constant (m³ kg⁻¹ s⁻²)
const omega_earth = 7.292115e-5; // Earth's angular velocity (rad/s)

function volume(a, c) {
  return (4 / 3) * Math.PI * Math.pow(a, 2) * c;
}

function find_equator_radius(V_earth, c_pole) {
  return Math.sqrt(V_earth / ((4 / 3) * Math.PI * c_pole));
}

function disk_gravity(R, z, t, rho) {
  /**
   * Calculate the gravitational acceleration (g_z) due to a uniform disk.
   */
  let term;
  if (z === 0) {
    term = 0;
  } else {
    term = z / Math.sqrt(Math.pow(z, 2) + Math.pow(R, 2));
  }
  return 2 * Math.PI * G * rho * t * (1 - term);
}

function disk_mass(R, dz, rho) {
  return dz * rho * Math.PI * Math.pow(R, 2);
}

function ellipsoid_gravity(a, c, rho, num_slices = 10000) {
  /**
   * Calculate gravity for an oblate spheroid (ellipsoid)
   * a = radius along axis down from where we are standing
   * c = radius of perpendicular axis
   */
  let total_g = 0.0;
  let total_m = 0.0;
  const dz = (2 * c) / num_slices; // Integration step along polar axis

  for (let i = 0; i < num_slices; i++) {
    // Current z position within ellipsoid (-c to c)
    const z_disk = -c + (i + 0.5) * dz;

    // Distance from observation point to this disk
    const distance = c - z_disk;

    // Radius of the disk at position z_disk (ellipsoid cross-section)
    let r_disk;
    if (Math.abs(z_disk) > c) {
      r_disk = 0;
    } else {
      // Equation for oblate spheroid: (x²+y²)/a² + z²/c² = 1
      r_disk = a * Math.sqrt(1 - (Math.pow(z_disk, 2) / Math.pow(c, 2)));
    }

    if (r_disk > 0) {
      total_g += disk_gravity(r_disk, distance, dz, rho);
      total_m += disk_mass(r_disk, dz, rho);
    }
  }

  return total_g;
}

// Parameters
const M_earth = 5.972365357e24; // mass of earth in kg
const a_earth = 6378e3;
const c_earth = 6356e3;
const V_earth = volume(a_earth, c_earth);
console.log(`V_earth: ${V_earth}`);
const rho_earth = M_earth / V_earth;
console.log(`rho_earth: ${rho_earth}`);

/*
Max:
Equatorial Radius: 7109436.41 m
Polar Radius: 5115435 m
Gravity at Pole: 10.038083320303 m/s²
*/


