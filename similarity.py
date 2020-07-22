from datetime import timedelta,datetime
import numpy as np

#10 and 0.5 are threasholds
def msm(trajectory_a,trajectory_b):
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
    ab,ba = score(results)
    result = (ab + ba)/(len(trajectory_a)+len(trajectory_b))

def score(matrix):
    sum_max_line = 0
    sum_max_column = 0
    for line in matrix:
        sum_max_line += max(line)
    for i in range(len(matrix[0])):
        max_column = matrix[0][i]
        for line in matrix[1:]:
            max_column = max(max_column,line[i])
        sum_max_column += max_column
    return sum_max_line,sum_max_column

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