import csv
from geopy.distance import geodesic
from dataclass import dataclass

@dataclass
class Point:
    user_id: str
    venue_id: str
    venue_category_id: str
    venue_category: str
    latitude: float
    longitude: float
    timezone_offset: str
    utc_timestamp: str
    duration: float

def return_list(name):
    trajectories = {}
    with open(name) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            user_id, *data = row
            if user_id not in lista:
                trajectories[user_id] = []
            point_created = Point(row[0],row[1],row[2],row[3],float(row[4]),float(row[5]),row[6],row[7],0.)
            trajectories[user_id].append(point_created)
    # print(trajectories['470'])
    return trajectories

#merging two spatiotemporal points
def merge_points(point_one,point_two,diversity_criteria,closeness_criteria):
    timestamp1 = datetime.strptime(point_one,'%a %b %d %H:%M:%S %z %Y')
    timestamp2 = datetime.strptime(point_two,'%a %b %d %H:%M:%S %z %Y')
    timestamp = min(timestamp1,timestamp2)


#recebe uma lista de trajetorias e gera uma nova lista com a categoria de duration (quanto tempo a trajetoria permaneceu naquele lugar)
def add_duration(trajectories):
    #iterar em cada trajetoria
    new_dict = {}
    for user_id in trajectories:
        new_dict[user_id] = []
        #iterar em cada segmento da trajetoria
        point_one = trajectories[user_id][0] #the point that will be used as a comparison
        new_dict[user_id].append(point_one)
        for segment in trajectories[user_id][1:]:
            point_two = segment
            coordinate_one =  (point_one.latitude, point_one.longitude)
            coordinate_two = (point_two.latitude,point_two.longitude)
            distance = geodesic(coordinate_one,coordinate_two).miles
            #if its a different location
            if distance > 2:
                point_one = segment
                new_dict[user_id].append(point_one)
            #if its the same location just add the duration of it
            else:
                timestamp_one = datetime.strptime(point_one,'%a %b %d %H:%M:%S %z %Y')
                timestamp_two = datetime.strptime(point_two,'%a %b %d %H:%M:%S %z %Y')
                new_duration = timestamp_two - timestamp_one
                new_duration = new_duration.total_seconds()/3600
                duration = new_duration + duration
                new_dict[user_id][-1].duration = duration1
    return new_dict
                

                



# def trajectory_reconstruction():

# def get_connected_region():

# def get_neighbors():

# #merging trajectories
# def merge_trajectory():

# def Dijkstra():

return_list('dataset_TSMC2014_NYC.csv')
# print(return_list('dataset_TSMC2014_NYC.csv'))
