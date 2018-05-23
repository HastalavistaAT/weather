#!/usr/bin/python -u

import Adafruit_MCP9808.MCP9808 as MCP9808
import sys
import os
import mysql.connector as mariadb


sensor = MCP9808.MCP9808()
sensor.begin()

mariadb_connection = mariadb.connect(user='pi', password='katzerl ich bin!', database='weather')
cursor = mariadb_connection.cursor()

# MAIN
def main():

    while(1):
        temp = sensor.readTempC()
        cursor.execute("INSERT INTO measurements (location,type,value) VALUES (%s,%s,%s)", ("Gang EG", "C", '{0:0.1F}'.format(temp)));
        mariadb_connection.commit()
        sys.exit(1)
if __name__ == '__main__':
    main()
