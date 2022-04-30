import L2_kinematics as kn
import L2_log as log
import numpy as np
import time


while 1:
    wheel_mo = kn.getPdCurrent()
    motion = kn.getMotion()
    log.tmpFile(wheel_mo[0], "PDL.txt")
    log.tmpFile(wheel_mo[1], "PDR.txt")
    log.tmpFile(motion[0], "x_dot.txt")
    log.tmpFile(motion[1], "theta_dot.txt")
    print(f"PDL and PDR values are: {wheel_mo}")
    print(f"x_dot and theta_dot values are: {motion}")
    time.sleep(0.2)