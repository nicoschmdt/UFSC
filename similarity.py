import numpy as np

#space dimension
#preciso passar as coordenadas certinho
def einsum(a, b):
    coordinate_one = (a.latitude,a.longitude)
    coordinate_two = (b.latitude,b.longitude)
    z = v - u
    return np.sqrt(np.einsum('i,i->', z, z))

#time dimension
#arrumar a questao do diam
def time(a,b):
    tempo2_a = a.utc_timestamp + datetime.timedelta(hours=a.duration)
    tempo2_b = b.utc_timestamp + datetime.timedelta(hours=b.duration)
    if tempo2_a < b.utc_timestamp:
        return 0
    numerador = diam(max(a.utc_timestamp,tempo2_a),min(b.utc_timestamp,tempo2_b))
    divisor = diam(min(a.utc_timestamp,b.utc_timestamp),max(tempo2_a,tempo2_b))
    return 1 - (numerador/divisor)

def diam(a,b):
    return abs(b-a)


#semantic dimension
def semantics(a,b):
    if a.venue_id == b.venue_id:
        return 0
    return 1