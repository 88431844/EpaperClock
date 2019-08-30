#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in9
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def digital_to_chinese(digital):
    str_digital = str(digital)
    chinese = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '0': '零'}
    chinese2 = ['拾', '佰', '仟', '万', '厘', '分', '角']
    jiao = ''
    bs = str_digital.split('.')
    yuan = bs[0]
    if len(bs) > 1:
        jiao = bs[1]
    r_yuan = [i for i in reversed(yuan)]
    count = 0
    for i in range(len(yuan)):
        if i == 0:
            r_yuan[i] += ''
            continue
        r_yuan[i] += chinese2[count]
        count += 1
        if count == 4:
            count = 0
            chinese2[3] = '亿'

    s_jiao = [i for i in jiao][:3]  # 去掉小于厘之后的

    j_count = -1
    for i in range(len(s_jiao)):
        s_jiao[i] += chinese2[j_count]
        j_count -= 1
    last = [i for i in reversed(r_yuan)] + s_jiao

    last_str = ''.join(last)
    print(str_digital)
    print(last_str)
    for i in range(len(last_str)):
        digital = last_str[i]
        if digital in chinese:
            last_str = last_str.replace(digital, chinese[digital])
    print(last_str)
    return last_str

try:
    logging.info("epd2in9 Demo")
    
    epd = epd2in9.EPD()
    logging.info("init and Clear")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font100 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 100)
   
    # partial update
    logging.info("5.show time")
    epd.init(epd.lut_partial_update)    
    epd.Clear(0xFF)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    num = 0
    while (True):
        time_draw.rectangle((10, 10, 290, 120), fill = 255)
        time_draw.text((40, 5), time.strftime('%Y-%m-%d')+u'   星期'+digital_to_chinese(time.strftime('%w')), font = font24, fill = 0)
        time_draw.text((25, 20), time.strftime('%H:%M'), font = font100, fill = 0)
        # time_draw.text((30, 30), time.strftime('%A'), font = font24, fill = 0)
        # time_draw.text((60, 60), time.strftime('%Y-%m-%d-%A'), font = font24, fill = 0)
        # time_draw.text((5, 70), u'一二三四五六日星期年月日时分秒', font = font18, fill = 0)
        
       # time_draw.text((30, 30), u'12:12', font = font46, fill = 0)
        newimage = time_image.crop([10, 10, 120, 150])
        time_image.paste(newimage, (10,10))  
        epd.display(epd.getbuffer(time_image))
        
        # num = num + 1
        # if(num == 10):
        #     break
            
    logging.info("Clear...")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in9.epdconfig.module_exit()
    exit()



