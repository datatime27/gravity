import math

# Define constants based on the Excel Range values you mentioned
# Replace these with the actual values or how you intend to get them
a = 6378137.0  # Example value for 'a' (Equatorial radius in meters)
b = 6356752.314  # Example value for 'b' (Polar radius in meters)
GEq = 9.780325336  # Example value for 'GEq' (Gravity at the Equator in m/s^2)
GPole = 9.832184938  # Example value for 'GPole' (Gravity at the Pole in m/s^2)
GM = 3.99e14
omega = 7.2921e-5 # 2 pi / 24 hour time period
#m = omega**2 * a / 9.780325336 # 0.00344978  # Example value for 'm' (related to Earth's rotation)
m = omega**2 * a**2 * b / GM # 0.0034463177156506715


def gforce(rad: float) -> float:
    """
    Calculates the gravitational force based on the geodetic latitude.

    Args:
        rad: Geodetic latitude in radians.

    Returns:
        The gravitational force.
    """
    cos2 = math.cos(rad) ** 2
    sin2 = math.sin(rad) ** 2
    return (a * GEq * cos2 + b * GPole * sin2) / math.sqrt(a**2 * cos2 + b**2 * sin2)

def gh(rad: float, alt: float) -> float:
    """
    Calculates the gravitational acceleration at a given altitude.

    Args:
        rad: Geodetic latitude in radians.
        alt: Altitude above the reference ellipsoid in meters.

    Returns:
        The gravitational acceleration at the given altitude.
    """
    f = (a - b) / a
    sin2_rad = math.sin(rad) ** 2
    gh_value = gforce(rad) * (1 - (2 / a) * (1 + f + m - 2 * f * sin2_rad) * alt + (3 / (a ** 2)) * (alt ** 2))
    return gh_value

def gravity(latitude_degrees, altitude_meters):
    latitude_radians = math.radians(latitude_degrees)
    gravity_at_altitude = gh(latitude_radians, altitude_meters)
    return gravity_at_altitude

def location(name, latitude_degrees, altitude_meters):
    g = gravity(latitude_degrees, altitude_meters)
    weight = (g/ g_home)  * 1000
    print(f"{name}:\t latitude {latitude_degrees}°: alt: {altitude_meters:.1f}m Gravity: {g:.6f} m/s^2 weight: {weight}")

if __name__ == '__main__':
    # Example usage:

    g_home = gravity(33.97, 9)
    
    location('Seattle',   47.45, 131)
    location('Juneau',    58.3,   17)
    location('Anchorage', 61.1,   31)
    location('Utqiagvik', 71.29,   10)
    location('Santa',     90,      0)
    location('Equator',    0,      0)
    

    
    