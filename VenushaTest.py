import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

def get_percent_error(instructor_value, actual_value):
    percentError = abs(((instructor_value - (actual_value)) / instructor_value)) * 100
    return percentError

def compare_angle_lists(coach_List, player_List, path):
    percent_error_list = []
    #algorithm for comparing two node angle lists
    for i in path:
        percent_error = get_percent_error(coach_List[path[i][0]], player_List[path[i][1]]) 
        percent_error_list.append(percent_error)    
    leeway_Percentage = 15
    flagged_timestamps = []
    for j in percent_error_list:
        if percent_error_list[j] >= leeway_Percentage:
            timestamp = j * 1/30 # check 30 to make sure its fps
            flagged_timestamps.append(timestamp)
#flagged_timestamps is the list of timestamps that don't meet the threshold
# percent_error_list is the list of deviations linked through path    

