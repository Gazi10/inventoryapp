import cv2
import requests
import json
import inventory_db as db
import numpy as np
from pyzbar.pyzbar import decode
from time import sleep
from pygame import mixer

def scan():
    cam = cv2.VideoCapture(0)

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip,deflate',
    }

    cam.set(3,640)
    cam.set(4,480)

    mixer.init() 
    beep=mixer.Sound("beep.wav")

    while True:
        success,img=cam.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',img)
            frame=buffer.tobytes()
            for code in decode(img):
                beep.play()
                myData = code.data.decode('utf-8')
                resp = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc={}'.format(myData), headers=headers)
                data = json.loads(resp.text)
                db.insert([data['items'][0]['title'], 1, data['items'][0]['offers'][0]['price'],
                        data['items'][0]['images'][0], data['items'][0]['offers'][0]['link']])
                sleep(1.5)

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
