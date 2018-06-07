import time, datetime
import os

while True:
    file = open("display_call","r")
    os.system(file.read())
    file.close()
    time.sleep(5)
