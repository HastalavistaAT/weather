#!/usr/bin/python -u

import serial
import sys
import os
import mysql.connector as mariadb
import Adafruit_DHT

# serial port of USB-WDE1
port = '/dev/ttyUSB0'


mariadb_connection = mariadb.connect(user='pi', password='katzerl ich bin!', database='weather')
cursor = mariadb_connection.cursor()

# MAIN
def main():
    # open serial line
    ser = serial.Serial(port, 9600)
    if not ser.isOpen():
        print "Unable to open serial port %s" % port
        sys.exit(1)

    while(1):
        taussen = '??.?'
        haussen = '??%'
        tdachboden = '??.?'
        hdachboden = '??%'
        # read line from WDE1
        line = ser.readline()
        line = line.strip()
        print line
        data = line.split(';')
        if (len(data) == 25 and data[0] == '$1' and data[24] == '0'):
            # data is valid 
            # re-format data into an update string for rrdtool
            for i, val in enumerate(data):
                if (val != ''):
                    val = val.replace(',','.')
                    if (i == 7):
                        cursor.execute("INSERT INTO measurements (location,type,value) VALUES (%s,%s,%s)", ("Aussen", "C", val));
                        taussen = val
                    if (i == 8):
                        cursor.execute("INSERT INTO measurements (location,type,value) VALUES (%s,%s,%s)", ("Dachboden", "C", val));
                        tdachboden = val
                    if (i == 15):
                        cursor.execute("INSERT INTO measurements (location,type,value) VALUES (%s,%s,%s)", ("Aussen", "%", val));
                        haussen = val
                    if (i == 16):
                        cursor.execute("INSERT INTO measurements (location,type,value) VALUES (%s,%s,%s)", ("Dachboden", "%", val));
                        hdachboden = val
        
            hgang, tgang = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, '4')

            if hgang is not None and tgang is not None:
                cursor.execute("INSERT INTO measurements (location,type,value) VALUES (%s,%s,%s)", ("Gang EG", "C", '{0:0.1f}'.format(tgang)));
                cursor.execute("INSERT INTO measurements (location,type,value) VALUES (%s,%s,%s)", ("Gang EG", "%", '{0:0.1f}'.format(hgang)));
        
            mariadb_connection.commit()
            call = 'python /home/pi/weather/weather_display.py -a ' + str(taussen) + ' -g ' + '{0:0.1f}'.format(tgang) + ' -d ' + str(tdachboden) + ' -A ' + str(haussen) + '% -G ' + '{0:0.0f}'.format(hgang) + '% -D ' +str(hdachboden) + '%'
            print call
            file = open("/home/pi/weather/display_call","w")
            file.write(call)
            file.close()
            values = open("/home/pi/weather/temp","w")

            values.write(str(tdachboden) + "\n")
            values.write('{0:0.1f}'.format(tgang) + "\n")
            values.write(str(taussen) + "\n")
            values.write(str(hdachboden) + "%\n")
            values.write('{0:0.0f}'.format(hgang) + "%\n")
            values.write(str(haussen) + "%\n")
            
            values.close()
            #os.system(call)
            sys.exit(1)
if __name__ == '__main__':
    main()
