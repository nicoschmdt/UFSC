import csv

def return_list(name):
    trajectories = {}
    with open(name) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            user_id, *data = row
            if user_id not in lista:
                trajectories[user_id] = []
            trajectories[user_id].append(row)
    # print(trajectories['470'])
    return trajectories

#merging two spatiotemporal points
def merge_points(point_one,point_two,diversity_criteria,closeness_criteria):
    #preciso 

#recebe uma lista de trajetorias e gera uma nova lista com a categoria de duration (quanto tempo a trajetoria permaneceu naquele lugar)
def add_duration(trajectories):
    #iterar em cada trajetoria
    for user_id in trajectories:
        #iterar em cada segmento da trajetoria
        for segment in trajectories[user_id]:
            


# def trajectory_reconstruction():

# def get_connected_region():

# def get_neighbors():

# #merging trajectories
# def merge_trajectory():

# def Dijkstra():

return_list('dataset_TSMC2014_NYC.csv')
# print(return_list('dataset_TSMC2014_NYC.csv'))
