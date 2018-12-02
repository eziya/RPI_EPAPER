# -*- coding: utf-8 -*-
# 128 x 250 E-PAPER

import epd2in13
import Image
import ImageDraw
import ImageFont
from time import localtime, strftime
import Adafruit_DHT
import os

TIME_X_POS = 105
TIME_Y_POS = 10
TEMP_X_POS = 20
TEMP_Y_POS = 10
HUMID_X_POS = 20
HUMID_Y_POS = 150

def main():
    # To fix the path issue when script runs by crontab
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # initialize e-paper device
    epd = epd2in13.EPD()

    # draw background image
    epd.init(epd.lut_full_update)
    image = Image.open('resize_background_empty.bmp')

    epd.set_frame_memory(image, 0, 0)
    epd.display_frame()
    epd.set_frame_memory(image, 0, 0)
    epd.display_frame()

    # draw time, temperature, humidity
    epd.init(epd.lut_partial_update)

    # set image size
    time_image = Image.new('1', (200, 17), 255)
    temp_image = Image.new('1', (100, 50), 255)
    humid_image = Image.new('1', (76, 38), 255)

    drawTime = ImageDraw.Draw(time_image)
    drawTemp = ImageDraw.Draw(temp_image)
    drawHumid = ImageDraw.Draw(humid_image)

    # select 7-segment like font
    fontTime = ImageFont.truetype('/usr/share/fonts/truetype/lcd/DS-DIGIB.TTF', 20)
    fontTemp = ImageFont.truetype('/usr/share/fonts/truetype/lcd/DS-DIGIB.TTF', 60)
    fontHumid = ImageFont.truetype('/usr/share/fonts/truetype/lcd/DS-DIGIB.TTF', 45)

    time_width, time_height = time_image.size
    temp_width, temp_height  = temp_image.size
    humid_width, humid_height = humid_image.size

    while (True):
        # clear drawing area
        drawTime.rectangle((0, 0, time_width, time_height), fill=255)
        drawTemp.rectangle((0, 0, temp_width, temp_height), fill = 255)
        drawHumid.rectangle((0, 0, humid_width, humid_height), fill=255)

        # retrieve temperature & humidity data
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)

        # draw text
        drawTime.text((0, 0), strftime('%Y-%m-%d %H:%M:%S', localtime()), font=fontTime, fill=0)
        drawTemp.text((0, 0), '{0:0.1f}'.format(temperature), font = fontTemp, fill = 0)
        drawHumid.text((0, 0), '{0:0.1f}'.format(humidity), font = fontHumid, fill = 0)

        # copy image data to buffer
        epd.set_frame_memory(time_image.transpose(Image.ROTATE_270), TIME_X_POS, TIME_Y_POS)
        epd.set_frame_memory(temp_image.transpose(Image.ROTATE_270), TEMP_X_POS, TEMP_Y_POS)
        epd.set_frame_memory(humid_image.transpose(Image.ROTATE_270), HUMID_X_POS, HUMID_Y_POS)

        # update e-paper
        epd.display_frame()

if __name__ == '__main__':
    main()
