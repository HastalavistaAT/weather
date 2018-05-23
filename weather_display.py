# -*- coding: utf-8 -*-
import Image
import ImageDraw
import ImageFont

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import sys, getopt

def main(argv):
    tdachboden = '??.?'
    taussen = '??.?'
    tgang = '??.?'
    hdachboden = '??.?'
    haussen = '??.?'
    hgang = '??.?'
    

    try:
        opts, args = getopt.getopt(argv,"ha:g:d:A:G:D:",["taussen=","tgang=","tdachboden=","haussen=","hgang=","hdachboden="])
    except getopt.GetoptError:
        print 'weather display.py -a <Temperatur Aussen> -g <Temperatur Gang> -d <Temperatur Dachboden> -A <Luftfeuchte Aussen> -G <Luftfeuchte Gang> -D <LuftfeuchteDachboden>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'weather display.py -a <Temperatur Aussen> -g <Temperatur Gang> -d <Temperatur Dachboden> -A <Luftfeuchte Aussen> -G <Luftfeuchte Gang> -D <LuftfeuchteDachboden>'
            sys.exit()
        elif opt in ("-a", "--taussen"):
            taussen = arg 
        elif opt in ("-g", "--tgang"):
            tgang = arg 
        elif opt in ("-d", "--tdachboden"):
            tdachboden = arg
        elif opt in ("-A", "--haussen"):
            haussen = arg
        elif opt in ("-G", "--hgang"):
            hgang = arg
        elif opt in ("-D", "--hdachboden"):
            hdachboden = arg

    PITFT_2_8 = 18
    PITFT_2_2 = 25

    CURRENT_PITFT = PITFT_2_2

    # Raspberry Pi configuration.
    DC = CURRENT_PITFT
    RST = 23
    SPI_PORT = 0
    SPI_DEVICE = 0

    # BeagleBone Black configuration.
    # DC = 'P9_15'
    # RST = 'P9_12'
    # SPI_PORT = 1
    # SPI_DEVICE = 0

    # Create TFT LCD display class.
    disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

    # Initialize display.
    disp.begin()

    # Clear the display to a red background.
    # Can pass any tuple of red, green, blue values (from 0 to 255 each).
    disp.clear((0, 0, 0))

    # Alternatively can clear to a black screen by calling:
    # disp.clear()

    # Get a PIL Draw object to start drawing on the display buffer.
    draw = disp.draw()

    # Draw some shapes.
    # Draw a blue ellipse with a green outline.
    #draw.ellipse((10, 10, 110, 80), outline=(0,255,0), fill=(0,0,255))

    # Draw a purple rectangle with yellow outline.
    draw.rectangle((0, 320, 115, 220), outline=(204,8,0), fill=(204,8,0))
    draw.rectangle((0, 210, 115, 110), outline=(255,181,0), fill=(255,181,0))
    draw.rectangle((0, 100, 115, 0), outline=(111,0,127), fill=(111,0,127))
    draw.rectangle((125, 320, 240, 220), outline=(0,54,127), fill=(0,54,127))
    draw.rectangle((125, 210, 240, 110), outline=(0,194,255), fill=(0,194,255))
    draw.rectangle((125, 100, 240, 0), outline=(0,204,130), fill=(0,204,130))

    # Draw a white X.
    #draw.line((10, 170, 110, 230), fill=(255,255,255))
    #draw.line((10, 230, 110, 170), fill=(255,255,255))

    # Draw a cyan triangle with a black outline.
    #draw.polygon([(10, 275), (110, 240), (110, 310)], outline=(0,0,0), fill=(0,255,255))

    # Load default font.
    #font = ImageFont.load_default()

    # Alternatively load a TTF font.
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php

    # Define a function to create rotated text.  Unfortunately PIL doesn't have good
    # native support for rotated fonts, but this function can be used to make a 
    # text image and rotate it so it's easy to paste in the buffer.
    def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
        # Get rendered font width and height.
            draw = ImageDraw.Draw(image)
            width, height = draw.textsize(text, font=font)
            # Create a new image with transparent background to store the text.
            textimage = Image.new('RGBA', (width, height), (0,0,0,0))
            # Render the text.
            textdraw = ImageDraw.Draw(textimage)
            textdraw.text((0,0), text, font=font, fill=fill)
            # Rotate the text image.
            rotated = textimage.rotate(angle, expand=1)
            # Paste the text into the image, using it as a mask for transparency.
            image.paste(rotated, position, rotated)

    # Write two lines of white text on the buffer, rotated 90 degrees counter clockwise.
    font = ImageFont.truetype('/home/pi/weather/monofonto.ttf', 36)
    draw_rotated_text(disp.buffer, tdachboden, (15, 10), 90, font, fill=(255,255,255))
    draw_rotated_text(disp.buffer, tgang, (15, 120), 90, font, fill=(0,0,0))
    draw_rotated_text(disp.buffer, taussen, (15, 230), 90, font, fill=(255,255,255))
    draw_rotated_text(disp.buffer, hdachboden, (140, 10), 90, font, fill=(0,0,0))
    draw_rotated_text(disp.buffer, hgang, (140, 120), 90, font, fill=(0,0,0))
    draw_rotated_text(disp.buffer, haussen, (140, 230), 90, font, fill=(255,255,255))

    font = ImageFont.truetype('/home/pi/weather/Quadrit.ttf', 12)
    draw_rotated_text(disp.buffer, 'Temperatur\nDachboden', (70, 10), 90, font, fill=(255,255,255))
    draw_rotated_text(disp.buffer, 'Temperatur\nGang EG', (70, 120), 90, font, fill=(0,0,0))
    draw_rotated_text(disp.buffer, 'Temperatur\nAussen', (70, 230), 90, font, fill=(255,255,255))
    draw_rotated_text(disp.buffer, 'Luftfeuchte\nDachboden', (195, 10), 90, font, fill=(0,0,0))
    draw_rotated_text(disp.buffer, 'Luftfeuchte\nGang EG', (195, 120), 90, font, fill=(0,0,0))
    draw_rotated_text(disp.buffer, 'Luftfeuchte\nAussen', (195, 230), 90, font, fill=(255,255,255))


    #draw_rotated_text(disp.buffer, 'This is a line of text.', (170, 90), 90, font, fill=(255,255,255))

    # Write buffer to display hardware, must be called to make things visible on the
    # display!
    disp.display()

if __name__ == '__main__':
    main(sys.argv[1:])
