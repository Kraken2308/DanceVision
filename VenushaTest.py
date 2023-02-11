import numpy as np
from scipy.spatial.distance import euclidean

from fastdtw import fastdtw

x = np.array([[1,1], [2,2], [3,3], [4,4], [5,5]])
y = np.array([[2,2], [3,3], [4,4]])
distance, path = fastdtw(x, y, dist=euclidean)
print(distance)





import numpy as np
from scipy.spatial.distance import euclidean

from fastdtw import fastdtw

def get_percent_error(instructor_value, actual_value):
    percentError = abs(((instructor_value[i] - abs(actual_value)) / instructor_value)) * 100
    return percentError

def compare_angle_lists(coach_List, player_List):
    angle_deviation_list = []
    #algorithm for comparing two node angle lists
    for i in coach_List:
        percentError = get_percent_error(coach_List[i], player_List[i])
        angle_deviation_list.append(percentError)    
     # instructor node angles
    return angle_deviation_list

def fast_DTW_sync_mapping(coach_List, player_List):

    #using fast dtw for the dtw algorithm in syncing up videos
    x = np.array(coach_List) #list1's nodes/location of its angles
    y = np.array(player_List) #the same for list 2
    distance, path = fastdtw(x, y, dist=euclidean)
    return path

def SD_List_Creator(coach_List, player_List , path): #path taken from DTW function
    for i in path:
        SD_List = compare_angle_lists(coach_List, player_List)        
    return SD_List


# code not implemented; check with angan for accuracy
    for i in player_List:
        if coach_List[i] == player_List[i]:
            continue
        percentError = abs(((player_List[i] - abs(coach_List)) / coach_List)) * 100

        if percentError >= leewayPercentage:
            timestamp = i * 1/30 # check 30 to make sure its fps
            timestamps.append(timestamp)



