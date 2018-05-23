#!/bin/bash
vals=288
python /home/pi/weather/create_data.py --values $vals --type C --location Aussen --ofile /var/www/html/weather/dataCA.dat
python /home/pi/weather/create_data.py --values $vals --type C --location "Gang EG" --ofile /var/www/html/weather/dataCG.dat
python /home/pi/weather/create_data.py --values $vals --type C --location Dachboden --ofile /var/www/html/weather/dataCD.dat
python /home/pi/weather/create_data.py --values $vals --type % --location Aussen --ofile /var/www/html/weather/dataHA.dat
python /home/pi/weather/create_data.py --values $vals --type % --location "Gang EG" --ofile /var/www/html/weather/dataHG.dat
python /home/pi/weather/create_data.py --values $vals --type % --location Dachboden --ofile /var/www/html/weather/dataHD.dat
