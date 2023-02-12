import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

def get_percent_error(instructor_value, actual_value):
    percentError = abs(((instructor_value[i] - abs(actual_value)) / instructor_value)) * 100
    return percentError

def compare_angle_lists(coach_List, player_List, path):
    angle_deviation_list = []
    #algorithm for comparing two node angle lists
    for i in path:
        angle_standard_deviation = get_percent_error(coach_List[path[i][0]], player_List[path[1]]) 
        angle_deviation_list.append(angle_standard_deviation)    
    leeway_Percentage = 15
    flagged_timestamps = []
    for j in angle_deviation_list:
        if angle_deviation_list[j] >= leeway_Percentage:
            timestamp = j * 1/30 # check 30 to make sure its fps
            flagged_timestamps.append(timestamp)
#flagged_timestamps is the list of timestamps that don't meet the threshold
# angle_deviation_list is the list of deviations linked through path    

