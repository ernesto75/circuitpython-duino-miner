{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf610
{\fonttbl\f0\fnil\fcharset0 ComicSansMS;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww12760\viewh9600\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import board, digitalio, time, usb_cdc\
import adafruit_hashlib as hashlib\
\
#initialize the onboard led\
led = digitalio.DigitalInOut(board.LED)\
led.direction = digitalio.Direction.OUTPUT \
\
difficulty = 0\
#Hardcoded DUCO_ID while investigating other methods like str(machine.unique_id())\
DUCO_ID = \'93DUCOID6900690069006900\'94\
\
while True:\
\
    if usb_cdc.data.in_waiting > 0:\
        readjob = usb_cdc.data.readline()\
        job = readjob.decode().strip().split(',')\
        difficulty = job[2]\
        start = int(round(time.time() * 1000)) #start time in milliseconds\
        for result in range(100 * int(difficulty) + 1): # from 0 to assigned difficulty\
            calc = hashlib.sha1((str(job[0])+str(result)).encode()).hexdigest() #calculated hash\
            if (calc == job[1]):\
                break #If calculated hash is equal to expected hash\
        end = int(round(time.time() * 1000)) #endtime in milliseconds\
        hastime = end - start #to be converted in binary\
        binhastime = "\{0:b\}".format(int(hastime)) #elapsedtime in binary\
        binresult = "\{0:b\}".format(int(result)) #result in binary\
        usb_cdc.data.write(bytes(str(binresult)+","+str(binhastime)+","+DUCO_ID+"\\n","utf-8"))\
        #blink the led\
        led.value = True\
        time.sleep(0.025) \
        led.value = False\
}