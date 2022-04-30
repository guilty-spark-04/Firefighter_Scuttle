import Adafruit_BBIO.GPIO as GPIO
import time
import signal
import L2_log as log

IR1 = 'P9_23'
#IR2 = 'P9_28'
tempIR = 'GP0_5'

GPIO.setup(IR1, GPIO.IN)
#GPIO.setup(IR2, GPIO.IN)
GPIO.setup(tempIR, GPIO.IN)

while True:
    input1 = GPIO.input(IR1)
    print("Input 1: ", input1)
    #input2 = GPIO.input(IR2)
    #print("Input 2: ", input2)
    input3 = GPIO.input(tempIR)
    print("Input temp: ", input3)
    time.sleep(0.1)
    
# i wanted to measure distance but this shit is botched