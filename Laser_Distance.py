#!/usr/bin/env python
import RPi.GPIO as GPIO
import requests
import time

from PCF8591 import PCF8591

class Laser_Measure(object):

    def __init__(self, addr=0x48, device_num=0):
        # PCF8591_MODULE SETUP
        self.PCF8591_MODULE = PCF8591.PCF8591()

        # SET GPIO WARNINGS AS FALSE
        GPIO.setwarnings(False)

        # SET DEVICE ID
        self.device_id = device_num

        # SETUP REQUEST DATA
        self.url = 'http://192.168.1.24:52275/data'
        self.datas = {'device_id' : device_num, 'status' : -1}
        self.headers = {'Content-Type' : 'application/json'}

        # CREATE SESSION
        self.sess = requests.Session()

    def get_object_detected(self):
        if (self.PCF8591_MODULE.read(2) > 100):
            return True
        return False

    def update_time_table(self):
        self.datas = {'device_id' : self.device_id, 'status' : 0}
        print(self.datas)

    def send_data(self):
        try:
            request_id = self.sess.post(self.url, json=self.datas, headers=self.headers)
            print(request_id.status_code)
        except requests.exceptions.RequestException as e:
            print(e)

    def destroy(self):
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        Laser_Distancer = Laser_Measure(0x48, 0)
        while True:
            if (Laser_Distancer.get_object_detected()):
                print("DETECTED OBJECT") # Test Print
                try:
                    Laser_Distancer.update_time_table() # Perform Json data setup tasks
                finally:
                    Laser_Distancer.send_data() # Transferring data to the server
            time.sleep(0.1)

    except KeyboardInterrupt:
        Laser_Distancer.destroy()
