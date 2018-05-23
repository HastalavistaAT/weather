#!/usr/bin/python -u

import serial
import sys
import os
import mysql.connector as mariadb

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
                    if (i == 8):
                        cursor.execute("INSERT INTO measurements (location,type,value) VALUES (%s,%s,%s)", ("Dachboden", "C", val));
                    if (i == 15):
                        cursor.execute("INSERT INTO measurements (location,type,value) VALUES (%s,%s,%s)", ("Aussen", "%", val));
                    if (i == 16):
                        cursor.execute("INSERT INTO measurements (location,type,value) VALUES (%s,%s,%s)", ("Dachboden", "%", val));
            mariadb_connection.commit()
        sys.exit(1)
if __name__ == '__main__':
    main()
