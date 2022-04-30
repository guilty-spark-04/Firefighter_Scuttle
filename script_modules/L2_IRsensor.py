import Adafruit_BBIO.GPIO as GPIO
import time
import signal
import L2_log as log

IR1 = 'P9_23'
IR2 = 'P9_28'

GPIO.setup(IR1, GPIO.IN)
GPIO.setup(IR2, GPIO.IN)

while True:
    input1 = GPIO.input(IR1)
    print("Input: ", input1, " cm")
    input2 = GPIO.input(IR2)
    print("Input: ", input2, " cm")
    time.sleep(0.1)
    
# i wanted to measure distance but this shit is botched