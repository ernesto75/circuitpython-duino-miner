import board, digitalio, time, usb_cdc
import adafruit_hashlib as hashlib

#setup the onboard led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

#Hardcoded DUCO_ID while investigating other methods like str(machine.unique_id())
DUCO_ID = "DUCOID6900690069006900"

while True:
    if usb_cdc.data.in_waiting > 0:
        readjob = usb_cdc.data.readline()
        job = readjob.decode().strip().split(',')
        difficulty = job[2]
        start = int(round(time.time() * 1000)) #start time in milliseconds
        for result in range(100 * int(difficulty) + 1): # from 0 to assigned difficulty
            calc = hashlib.sha1((str(job[0])+str(result)).encode()).hexdigest() #calculated hash
            if (calc == job[1]):
                break #If calculated hash is equal to expected hash
        end = int(round(time.time() * 1000)) #endtime in milliseconds
        hastime = end - start #to be converted in binary
        binhastime = "{0:b}".format(int(hastime)) #elapsedtime in binary
        binresult = "{0:b}".format(int(result)) #result in binary
        usb_cdc.data.write(bytes(str(binresult)+","+str(binhastime)+","+DUCO_ID+"\n","utf-8"))
        #blink the led
        led.value = True
        time.sleep(0.025)
        led.value = False
        
