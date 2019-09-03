#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys,requests,json
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

logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='epaper_clock.log',
                    filemode='w',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
def getWeather():
    r = requests.get('http://restapi.amap.com/v3/weather/weatherInfo?city=110105&key=446bdde0691cffb14c1aff83a8912467')
    r.encoding = 'utf-8'
    weatherData = json.loads(r.text.encode('utf-8'))
    w = weatherData['lives'][0]
    temperature = str(w['temperature'].encode('utf-8'),'utf-8')
    weather = str(w['weather'].encode('utf-8'),'utf-8')
    return temperature,weather
def getWeatherMore():
    r = requests.get('http://restapi.amap.com/v3/weather/weatherInfo?extensions=all&city=110108&key=446bdde0691cffb14c1aff83a8912467')
    r.encoding = 'utf-8'
    weatherData = json.loads(r.text.encode('utf-8'))
    forecasts = weatherData['forecasts'][0]
    reportTime = str(forecasts['reporttime'].encode('utf-8'),'utf-8')[10:16]
    casts = forecasts['casts']
    tomorrowWeather = casts[1]['dayweather']
    tomorrowNightTemp = casts[1]['nighttemp']
    tomorrowDayTemp = casts[1]['daytemp']
    return reportTime,tomorrowWeather,tomorrowNightTemp,tomorrowDayTemp
	
def digital_to_chinese(digital):
    str_digital = str(digital)
    chinese = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '日', '8': '八', '9': '九', '0': '日'}
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
    for i in range(len(last_str)):
        digital = last_str[i]
        if digital in chinese:
            last_str = last_str.replace(digital, chinese[digital])
    return last_str

try:
    logging.info("epd2in9 Clock")
    
    epd = epd2in9.EPD()
    logging.info("init and Clear")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
   # font24 = ImageFont.truetype(os.path.join(picdir, 'font-f930.ttc'), 18)
    font24 = ImageFont.truetype(os.path.join(picdir, 'font-old.ttc'), 24)
#    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font18 = ImageFont.truetype(os.path.join(picdir, 'font-old.ttc'), 18)
    font = ImageFont.truetype(os.path.join(picdir, 'font-f930.ttc'), 87)
   
    # partial update
    epd.init(epd.lut_partial_update)    
    epd.Clear(0xFF)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    num = 0
    temperature,weather = getWeather()
    reportTime,tomorrowWeather,tomorrowNightTemp,tomorrowDayTemp = getWeatherMore()
    time_draw.text((10,110),u'今:'+temperature+u'°C '+weather+u' 明:'+tomorrowNightTemp+u'~'+tomorrowDayTemp+u'°C '+tomorrowWeather+u' 更:'+reportTime,font = font18,fill = 0)
    while (True):
#每隔半小时更新天气
        num = num + 1
        if(num == 1800):
             temperature,weather = getWeather()
             reportTime,tomorrowWeather,tomorrowNightTemp,tomorrowDayTemp,acquiredWeather,acquiredNightTemp,acquiredDayTemp = getWeatherMore()
             time_draw.text((10,110),u'今:'+temperature+u'°C '+weather+u' 明:'+tomorrowNightTemp+u'~'+tomorrowDayTemp+u'°C '+tomorrowWeather+u' 更:'+reportTime,font = font18,fill = 0)
             num = 0
        time_draw.rectangle((10, 10, 290, 110), fill = 255)
        time_draw.text((10, 5), u' '+time.strftime('%m-%d')+u' 周'+digital_to_chinese(time.strftime('%w'))+u' | 距开资:07天', font = font24, fill = 0)
        time_draw.text((10, 25), time.strftime('%H:%M'), font = font, fill = 0)
        newimage = time_image.crop([10, 10, 120, 150])
        time_image.paste(newimage, (10,10))  
        epd.display(epd.getbuffer(time_image))
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



