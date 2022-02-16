import serial
import datetime
from time import sleep
import RPi.GPIO as GPIO
from procees_push_cloud import process_input
from multiprocessing import Process

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH)

GPIO.output(4, GPIO.LOW)
sleep(0.005)
GPIO.output(4, GPIO.HIGH)

ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1 , parity = serial.PARITY_NONE, rtscts = 0)
ser.flush()
countr = 0
head = 'TimeStamp,Voltage,Current,RealPower,PowerFactor,ApparantPower,Reactivepower,Frequency'

with open('/home/pi/single_phase_log.csv','a') as fp:
    fp.write(head+'\n')
fp.close()

def write_to_csv(data) :
    with open('/home/pi/single_phase_log.csv','a') as fp:
            fp.write(data)
        #fp.close()

def create_job(target, *args):
    p = multiprocessing.Process(target=target, args=args)
    p.start()
    return p


while True:
    
    t = datetime.datetime.now()
    ct = str(t)

    try:
        line = ser.readline()
        print(line)
        line1 = line.decode()
        data = ct+','+line1 
        print(line1)
        ps = create_job(process_input, data)
        #p1 = Process(target=process_input, args=(str(data)))
        #p2 = Process(target=write_to_csv, args=(data))
        #p1.start()
        with open('/home/pi/single_phase_log.csv','a') as fp:
            fp.write(data)
        #fp.close()
        p1.join()
        #p2.join()
        

    except Exception as e:
        fp.close()
        #print(e)
