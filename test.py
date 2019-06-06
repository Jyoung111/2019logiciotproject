import RPi.GPIO as GPIO
import time
from mq import *
import sys, time
from firebase import firebase



channel = 21
led_left = 20
led_right = 16
led_up = 13
led_down = 19

# Get a database reference to our blog.
firebase = firebase.FirebaseApplication('https://iotcapstone-12374.firebaseio.com/', None)


GPIO.setmode(GPIO.BCM)

GPIO.setup(channel, GPIO.IN)
GPIO.setup(led_left, GPIO.OUT)
GPIO.setup(led_right, GPIO.OUT)
GPIO.setup(led_up, GPIO.OUT)
GPIO.setup(led_down, GPIO.OUT)
GPIO.setup(18, GPIO.IN)
#GPIO.setup(27, GPIO.OUT)

def callback(channel):
    print("flame detected") 

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change



mq = MQ();




try:
    
    while True:
        if GPIO.input(18):
         print('Pas de detection')
         time.sleep(0.2)
        if GPIO.input(18)!=1:
         print('Detection de GAS')
         GPIO.output(led_left,True)
         GPIO.output(led_right,True)
         GPIO.output(led_up,True)
         GPIO.output(led_down,True)
         #GPIO.output(27, False)
         time.sleep(0.1)
         #GPIO.output(27, True)
         

        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm\n" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
        sys.stdout.flush()
        time.sleep(0.1)
        
        firebase.put('/datas/sensor3', 'CHECK' , 1)


#        users_ref.update({
#            'sensor3' : {
#                'LPG': perc["GAS_LPG"],
#                'CO' : perc["CO"],
#               'SMOKE': perc["SMOKE"]
#            }
#        })

except KeyboardInterrupt:
    GPIO.cleanup()