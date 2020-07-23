import csv
import similarity
from geopy.distance import geodesic
from dataclasses import dataclass
from datetime import timedelta,datetime
from pprint import pprint
from numpy import argmax,argmin

@dataclass
class Point:
    user_id: str
    venue_id: str
    venue_category_id: str
    venue_category: str
    latitude: float
    longitude: float
    timezone_offset: str
    utc_timestamp: datetime
    duration: float

def main(name,anonymity_criteria):
    trajectories = return_list(name)
    trajectories = add_duration(trajectories)
    trajectories = split_trajectories(trajectories)
    graph = build_neighbours_graph(trajectories)
    similarity_matrix = create_similarity_matrix(trajectories)
    # anonymized = merge_trajectory(trajectories,similarity_matrix,anonymity_criteria)

def return_list(name):
    trajectories = {}
    with open(name) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            user_id, *data = row
            if user_id not in trajectories:
                trajectories[user_id] = []
            point_created = Point(
                row[0],
                row[1],
                row[2],
                row[3],
                float(row[4]),
                float(row[5]),
                row[6],
                datetime.strptime(row[7],'%a %b %d %H:%M:%S %z %Y'),
                0.)
            trajectories[user_id].append(point_created)
    return trajectories

#merging two spatiotemporal points
def merge_points(point_one,point_two,diversity_criteria,closeness_criteria,graph):
    timestamp1 = point_one.utc_timestamp
    timestamp2 = point_two.utc_timestamp
    #prob gotta turn this one like the utc_timestamp format
    timestamp = min(timestamp1,timestamp2)
    duration = max(timedelta(hours=point_one.duration) + timestamp1,timedelta(hours=point_two.duration) + timestamp2)
    location = get_connected_region(graph,point_one,point_two)

    diversity = get_diversity(location)
    while diversity < diversity_criteria:
        x = get_neighbors(location,graph)
        B = []
        for i in len(x):
            holder = location.append(x[i])
            B.append(get_diversity(holder))
        i = argmax(B)
        location = location.append(x[i])

    closeness = get_closeness(location)
    while closeness > closeness_criteria:
        x = get_neighbors(location,graph)
        for i in len(x):
            holder = location.append(x[i])
            B.append(get_closeness(holder))
        i = argmin(B)
        location = location.append(x[i])
    return location
    
#receives a trajectory list and generates a new one with the duration category updated
def add_duration(trajectories):
    new_dict = {}
    for user_id in trajectories:
        new_dict[user_id] = []
        #iterate in each segment of the trajectory
        point_one = trajectories[user_id][0] #the point that will be used as a comparison
        new_dict[user_id].append(point_one)
        for segment in trajectories[user_id][1:]:
            if point_one.venue_id != segment.venue_id:
                point_one = segment
                new_dict[user_id].append(point_one)
            #if its the same location just update the duration of it
            else:
                timestamp_one = point_one.utc_timestamp
                timestamp_two = segment.utc_timestamp
                new_duration = timestamp_two - timestamp_one
                new_duration = new_duration.total_seconds()/3600
                point_one.duration = new_duration + point_one.duration
    return new_dict

#receives the dictionary which the add_duration method returns
def build_neighbours_graph(trajectories):
    #use venue_id
    neighbors = {}
    for trajectory in trajectories.values():
        last_visited_point = trajectory[0]
        if last_visited_point.venue_id not in neighbors:
                neighbors[last_visited_point.venue_id] = []
        for point in trajectory[1:]:
            if point.venue_id not in neighbors:
                neighbors[point.venue_id] = []
            distance = calculate_distance(point,last_visited_point)
            neighbors[point.venue_id].append((last_visited_point.venue_id,distance))
            neighbors[last_visited_point.venue_id].append((point.venue_id,distance))
            last_visited_point = point
    # pprint(sorted(neighbors['49bbd6c0f964a520f4531fe3']))
    return neighbors

#to know if venue 2 and venue1 are neighbours
def is_neighbour(graph,venue1,venue2):
    if venue2 not in graph[venue1]:
        return False
    return True

def calculate_distance(point_one,point_two):
    coordinate_one =  (point_one.latitude, point_one.longitude)
    coordinate_two = (point_two.latitude,point_two.longitude)
    return geodesic(coordinate_one,coordinate_two).miles

def Dijkstra(graph, source):
    queue = set()
    distances = {}
    previous = {}
    for vertex in graph:
        distances[vertex] = float('inf')
        previous[vertex] = None
        queue.add(vertex)
    distances[source] = 0

    while queue.len() != 0:
        u = min(queue, key=lambda k: distances[k])
        queue.remove(u)

        for neighbor in graph[u]:
            venue_id,distance = neighbor
            alt = distances[u] + distance
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                previous[neighbor] = u

    return distances,previous

def get_connected_region(graph,source, destiny):
    distances,previous = Dijkstra(graph,source)
    path = [destiny]
    while destiny != source:
        path.append(previous[destiny])
        destiny = previous[destiny]
    return reversed(path + [source])

#receives a list of venue_ids and returns a list of neighbors
def get_neighbors(locations,graph):
    neighbors = set()
    for location in locations:
        neighbors.add(*graph[location])
    for location in locations:
        neighbors.remove(location)


#get how many diverse venue_ids we have in a point
def get_diversity(places):
    count = []
    count.append(places[0])
    for place in places[1:]:
        if place.venue_id not in count:
            count.append(place)
    return len(count)


#get how many diverse category_ids we have in a point
def get_closeness(places):
    count = []
    count.append(places[0])
    for place in places[1:]:
        if place.venue_category_id not in count:
            count.append(place)
    return len(count)

#merging trajectories // acho que vou precisar passar o graph tb..
# The algorithm will iterate until all the trajectories in T have been k-anonymized.
def merge_trajectory(dataset,similarity_matrix,anonymity_criteria):
    while: #enquanto tiver duas trajetorias com o k menor que o criterio
        i,j = argmax(similarity_matrix)

#returns a list of trajectories splitted by day
def split_trajectories(trajectories):
    splitted_trajectories = []
    for trajectory in trajectories:
        compare = trajectory[0]
        lista = [compare]
        for point in trajectory[1:]:
            if compare.datetime.day == point.datetime.day:
                lista.append(point)
            else:
                splitted_trajectories.append(lista)
                lista = [point]
            compare = point
    return splitted_trajectories

def create_similarity_matrix(trajectories):
    matrix = []
    for trajectory_one in trajectories:
        lista = []
        for trajectory_two in trajectories:
            if trajectory_one == trajectory_two:
                lista.append(float('-inf'))
            else:
                lista.append(similarity.msm(trajectory_one,trajectory_two))
        matrix.append(lista)
    return matrix


def merge(trajectory_one,trajectory_two):

# if __name__ = '__main__':
#     main()