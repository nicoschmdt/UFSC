from datetime import timedelta,datetime
import numpy as np

def similarity(trajectory_a,trajectory_b):
    results = []
    for point_a in trajectory_a:
        line = []
        for point_b in trajectory_b:
            variable = 0
            if einsum(point_a,point_b) <= 10:
                variable = 1
            if time(point_a,point_b) <= 0.5:
                variable += 1
            if semantics(point_a,point_b) <= 0.5:
                variable += 1
            line.append(variable/3)
        results.append(line)

#space dimension
#verificar se o metodo funciona# a parte do z = a - b ta confusa#
def einsum(a, b):
    coordinate_one = (a.latitude,a.longitude)
    coordinate_two = (b.latitude,b.longitude)
    z = a - b
    return np.sqrt(np.einsum('i,i->', z, z))

#time dimension
def time(a,b):
    tempo2_a = a.utc_timestamp + timedelta(hours=a.duration)
    tempo2_b = b.utc_timestamp + timedelta(hours=b.duration)
    if tempo2_a < b.utc_timestamp:
        return 0
    numerador = diam(max(a.utc_timestamp,tempo2_a),min(b.utc_timestamp,tempo2_b))
    divisor = diam(min(a.utc_timestamp,b.utc_timestamp),max(tempo2_a,tempo2_b))
    return 1 - (numerador/divisor)

def diam(a,b):
    return abs(b-a)

#semantic dimension
def semantics(a,b):
    if a.venue_category_id == b.venue_category_id:
        return 0
    return 1