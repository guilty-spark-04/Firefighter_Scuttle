import Adafruit_BBIO.GPIO as GPIO
import rcpy
import rcpy.motor as motor
import time

IR1 = 'P9_28'
IR2 = 'GP0_5'
IR3 = 'P9_23'
IR4 = 'GP0_3'

GPIO.setup(IR1, GPIO.IN)
GPIO.setup(IR2, GPIO.IN)
GPIO.setup(IR3, GPIO.IN)
GPIO.setup(IR4, GPIO.IN)
spraying = 0
rcpy.set_state(rcpy.RUNNING)

def sparyCan():
{
    try:
    
        while rcpy.get_state() != rcpy.EXITING:
            print(f"{GPIO.input(IR1)} {GPIO.input(IR2)} {GPIO.input(IR3)} {GPIO.input(IR4)}")
            time.sleep(1)
            
            if(not GPIO.input(IR2)):
                if(spraying):
                    pass
                else:
                    motor.set(4,0.6)
                    time.sleep(1)
                    motor.set(4,0)
                    spraying = 1
            else:
                if(spraying):
                    motor.set(4,-0.6)
                    time.sleep(1)
                    motor.set(4,0)
                    spraying = 0
    except KeyboardInterrupt:
        rcpy.set_state(rcpy.EXITING)
        pass
    finally:
        rcpy.set_state(rcpy.EXITING)
        print("exiting program")
}