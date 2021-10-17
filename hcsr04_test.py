#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#cits5506 distance_sensor.py
## using HC-SR04 ultrasonic sensor

S1_PIN_TRIGGER = 11
S1_PIN_ECHO = 7
S2_PIN_TRIGGER = 20
S2_PIN_ECHO = 16

def sensor(S1_PIN_ECHO, S1_PIN_ECHO, S2_PIN_TRIGGER, S2_PIN_ECHO):
    try:
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(S1_PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(S1_PIN_ECHO, GPIO.IN)
        GPIO.setup(S2_PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(S2_PIN_ECHO, GPIO.IN)
        
        GPIO.output(S1_PIN_TRIGGER, GPIO.LOW)
        GPIO.output(S2_PIN_TRIGGER, GPIO.LOW)
        print('waiting for sensor to settle')
        time.sleep(2)
        
        print('calculating distance')
        GPIO.output(S1_PIN_TRIGGER, GPIO.HIGH)
        GPIO.output(S2_PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(S1_PIN_TRIGGER, GPIO.LOW)
        GPIO.output(S2_PIN_TRIGGER, GPIO.LOW)
        
        while GPIO.input(PIN_ECHO) == 0:
            pulse_start_time = time.time()
        
        while GPIO.input(PIN_ECHO) == 1:
            pulse_end_time = time.time()
            
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        print('distance: {:.2f}cm.'.format(distance))
    finally:
        GPIO.cleanup()
    
    
sensor(S1_PIN_ECHO, S1_PIN_ECHO, S2_PIN_TRIGGER, S2_PIN_ECHO)
#sensor(S2_PIN_ECHO,S2_PIN_ECHO)

