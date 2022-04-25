import L1_lidar as lidar
import L2_vector as vec
import numpy as np
import csv
import time
print("loading rcpy")
import rcpy
import rcpy.motor as motor
print("finished loading motor libraries")

motor_r = 2
motor_l = 1

print("initializing rcpy...")
rcpy.set_state(rcpy.RUNNING)
print("Successfully set to running state")
# lidarData = lidar.polarScan(54)
# lidarData = vec.getValid(lidarData)
# with open('out.csv', 'w') as doc:
#     for polar in lidarData:
#         writer = csv.writer(doc)
#         coordinate = vec.polar2cart(polar[0],polar[1])
#         writer.writerow(coordinate)
MIN_DISTANCE = 0.2
try:
    while(rcpy.get_state() != rcpy.EXITING):
        lidarData = lidar.polarScan(54)
        lidarData = vec.getValid(lidarData)
        x_c = []
        y_c = []
        for point in lidarData:
            coordinate = vec.polar2cart(point[0],point[1])
            if(coordinate[0] >0 and coordinate[1]< 0.15 and coordinate[1] > -0.15):
                x_c.append(coordinate[0])
                y_c.append(coordinate[1])
        if (any(x <= MIN_DISTANCE for x in x_c)):
            print("stopping. obstacle")
            motor.set(motor_l,0)
            motor.set(motor_r,0)
        else:
            print("moving forward")
            motor.set(motor_l,0.6)
            motor.set(motor_r,0.6)
        time.sleep(0.2)
except KeyboardInterrupt:
    rcpy.set_state(rcpy.EXITING)
    pass
finally:
    rcpy.set_state(rcpy.EXITING)
    print("exiting program")