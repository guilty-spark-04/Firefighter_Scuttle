import L1_lidar as lidar
import L2_vector as vec
import numpy as np
import csv
import time

# lidarData = lidar.polarScan(54)
# lidarData = vec.getValid(lidarData)
# with open('out.csv', 'w') as doc:
#     for polar in lidarData:
#         writer = csv.writer(doc)
#         coordinate = vec.polar2cart(polar[0],polar[1])
#         writer.writerow(coordinate)
MIN_DISTANCE = 0.2
while(1):
    lidarData = lidar.polarScan(54)
    lidarData = vec.getValid(lidarData)
    x_c = []
    y_c = []
    for point in lidarData:
        coordinate = vec.polar2cart(point[0],point[1])
        if(coordinate[0] >0 and coordinate[1]< 0.3 and coordinate[1] > -0.3):
            x_c.append(coordinate[0])
            y_c.append(coordinate[1])
    if (any(x <= MIN_DISTANCE for x in x_c)):
        print("stopping. obstacle")
    else:
        print("moving forward")
    time.sleep(0.2)