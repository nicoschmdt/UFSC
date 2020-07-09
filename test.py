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
        userId,venueId,venueCategoryId,venueCategory,latitude1,longitude1,timezoneOffset,utcTimestamp1 = trajectories[user_id][0] #the point that will be used as a comparison
        duration = 0
        new_dict[user_id].append([userId,venueId,venueCategoryId,venueCategory,latitude1,longitude1,timezoneOffset,utcTimestamp1,duration])
        for segment in trajectories[user_id][1:]:
            userId2,venueId2,venueCategoryId2,venueCategory2,latitude2,longitude2,timezoneOffset2,utcTimestamp2 = segment
            coordinates1 = (latitude1,longitude1)
            coordinates2 = (latitude2,longitude2)
            distance = geodesic(coordinates1,coordinates2).miles
            #if its a different location
            if distance > 2:
                duration = 0
                userId,venueId,venueCategoryId,venueCategory,latitude1,longitude1,timezoneOffset,utcTimestamp1 = segment
                new_dict[user_id].append([userId,venueId,venueCategoryId,venueCategory,latitude1,longitude1,timezoneOffset,utcTimestamp1,duration])
            #if its the same location just add the duration of it
            else:
                timestamp1 = datetime.strptime(utcTimestamp1,'%a %b %d %H:%M:%S %z %Y')
                timestamp2 = datetime.strptime(utcTimestamp2,'%a %b %d %H:%M:%S %z %Y')
                new_duration = timestamp2 - timestamp1
                new_duration = new_duration.total_seconds()/3600
                duration = new_duration + duration
                new_dict[user_id][-1][-1] = duration
            #if the distance greater than 2 miles then the point should be taken into account
            #now is calculated how much time a point stayed at a certain location
            #preciso refazer esse if
            # if distance > 2:
            #     timestamp1 = datetime.strptime(utcTimestamp1,'%a %b %d %H:%M:%S %z %Y')
            #     timestamp2 = datetime.strptime(utcTimestamp2,'%a %b %d %H:%M:%S %z %Y')
            #     duration = timestamp2 - timestamp1
            #     duration = duration.total_seconds()/3600
            #     new_dict[user_id].append((userId,venueId,venueCategoryId,venueCategory,latitude1,longitude1,timezoneOffset,utcTimestamp1,duration))
            #     userId,venueId,venueCategoryId,venueCategory,latitude1,longitude1,timezoneOffset,utcTimestamp1 = segment
    return new_dict
                

                



# def trajectory_reconstruction():

# def get_connected_region():

# def get_neighbors():

# #merging trajectories
# def merge_trajectory():

# def Dijkstra():

return_list('dataset_TSMC2014_NYC.csv')
# print(return_list('dataset_TSMC2014_NYC.csv'))
