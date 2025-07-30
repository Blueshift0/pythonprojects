import math

planets = {
#- PERIAPSIS // APOAPSIS // ARG. OF PERICENTRE // LONG. OF ASC. NODE // INCLINATION -
    'Mercury': (0.307, 0.467, 29.124, 48.331, 7.005),
    'Venus': (0.718, 0.728, 54.884, 76.680, 3.395),
    'Terra': (0.983, 1.017, 114.207, -11.260, 0.000),
    'Mars': (1.381, 1.666, 286.502, 49.578, 1.850),
    'Ceres': (2.552, 2.978, 73.597, 80.393, 10.593),
    'Jupiter': (4.950, 5.457, 273.867, 100.556, 1.303),
    'Saturn': (9.041, 10.124, 339.392, 113.665, 2.489),
    'Uranus': (18.375, 20.063, 96.998, 74.006, 0.773),
    'Neptune': (29.767, 30.441, 273.249, 131.784, 1.770),
    'Fortuna': (266.122, 494.029, 344.493, 1.601, 0.993),
}

def distancebetween(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5

def orbitaldistance(peri, apo, ecc, theta):
    return (((peri + apo) / 2) * (1 - (ecc ** 2))) / (1 + ecc * math.cos(theta))

def findposition(dist, argperi, longasc, inc, anomaly):
    argperi = math.radians(argperi)
    longasc = math.radians(longasc)
    inc = math.radians(inc)
    anomaly = math.radians(anomaly)

    # True anomaly + argument of periapsis
    theta = anomaly + argperi

    # Position in orbital plane
    x_orb = dist * math.cos(theta)
    y_orb = dist * math.sin(theta)
    z_orb = 0

    # Rotate by inclination
    x1 = x_orb
    y1 = y_orb * math.cos(inc)
    z1 = y_orb * math.sin(inc)

    # Rotate by longitude of ascending node
    x = x1 * math.cos(longasc) - y1 * math.sin(longasc)
    y = x1 * math.sin(longasc) + y1 * math.cos(longasc)
    z = z1

    return (x, y, z)

def finddistances(a, b):
    peri1, apo1, argperi1, longasc1, inc1 = planets[a]
    peri2, apo2, argperi2, longasc2, inc2 = planets[b]
    ecc1 = (apo1 - peri1) / (apo1 + peri1)
    ecc2 = (apo2 - peri2) / (apo2 + peri2)
    min_dist = float('inf')
    max_dist = 0.0
    for anomaly1 in range(0, 360, 5):
        rad1 = orbitaldistance(peri1, apo1, ecc1, anomaly1)
        pos1 = findposition(rad1, argperi1, longasc1, inc1, anomaly1)
        for anomaly2 in range(0, 360, 5):
            rad2 = orbitaldistance(peri2, apo2, ecc2, anomaly2)
            pos2 = findposition(rad2, argperi2, longasc2, inc2, anomaly2)
            dist = distancebetween(pos1, pos2)  
            if dist < min_dist:
                min_dist = dist
            if dist > max_dist:
                max_dist = dist
    return (min_dist, max_dist)

def format_time(seconds):
    days = seconds // 86400
    hours = (seconds - (days * 86400)) // 3600
    minutes = (seconds - ((days * 86400) + (hours * 3600))) // 60
    return f"{days:.0f}d {hours:.0f}h {minutes:.0f}m"

def generate_all_distances():
    names = list(planets.keys())
    results = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = names[i]
            b = names[j]
            min_dist, max_dist = finddistances(a, b)
            results.append((a, b, min_dist, max_dist))
    return results

def main():
    distances = generate_all_distances()
    acc = 1
    print("Planet Pair\t\tMin Distance (AU)\tMin Travel Time\t\tMax Distance (AU)\tMax Travel Time")
    print("-" * 120)
    for planet1, planet2, min_dist, max_dist in distances:
        min_time = (((min_dist * 1.49e11) / (acc * 9.81)) ** 0.5) * 2
        min_time_str = format_time(min_time)
        max_time = (((max_dist * 1.49e11) / (acc * 9.81)) ** 0.5) * 2
        max_time_str = format_time(max_time)
        print(f"{planet1}-{planet2}\t\t{min_dist:.3f}\t\t\t{min_time_str}\t\t{max_dist:.3f}\t\t\t{max_time_str}")

main()