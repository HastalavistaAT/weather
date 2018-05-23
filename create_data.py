#!/usr/bin/python -u

import sys, getopt
import os
import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='pi', password='katzerl ich bin!', database='weather')
cursor = mariadb_connection.cursor()

# MAIN
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hv:t:l:o:",["values=","type=","location=","ofile="])
    except getopt.GetoptError:
        print 'create_data.py -v <values> -t <type> -l <location> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'create_data.py -v <values> -t <type> -l <location> -o <outputfile>'
            sys.exit()
        elif opt in ("-v", "--values"):
            values = arg 
        elif opt in ("-t", "--type"):
            typearg = arg 
        elif opt in ("-l", "--location"):
            location = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    cursor.execute("SELECT datetime, value FROM measurements where type='"+typearg+"' AND location='"+location+"' order by measure_id DESC limit "+values)
    data = "data: ["
    for row in cursor.fetchall() :
        #data from rows
        datetime = str(row[0])
        value = str(row[1])
        data = data + "{x: '" + datetime + "',y: " + value + "},"
    data = data[:-1]
    data = data + "]"
    f = open(outputfile, 'w')
    f.write(data)
    f.close()  # you can omit in most cases as the destructor will call it
    mariadb_connection.commit()
    sys.exit(1)
if __name__ == '__main__':
    main(sys.argv[1:])
