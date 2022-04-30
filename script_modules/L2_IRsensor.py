import Adafruit_BBIO.GPIO as GPIO
import time
import signal
import L2_log as log

IR1 = 'P9_28' # right side
IR2 = 'GP0_5' # front-right side
IR3 = 'P9_23' # front-left side
IR4 = 'GP0_3' # left side

GPIO.setup(IR1, GPIO.IN)
GPIO.setup(IR2, GPIO.IN)
GPIO.setup(IR3, GPIO.IN)
GPIO.setup(IR4, GPIO.IN)

while True:
    input1 = GPIO.input(IR1)
    input2 = GPIO.input(IR2)
    input3 = GPIO.input(IR3)
    input4 = GPIO.input(IR4)
    print("Input 1 (right): ", input1, " / Input 2 (front-right): ", input2, " / Input 3 (front-left): ", input3, " / Input 4 (left): ", input4, )
    time.sleep(0.1)
    
# i wanted to measure distance but this shit is botched