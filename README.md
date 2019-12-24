# epaperClock
基于微雪2.9寸墨水屏和树莓派zero w，制作的墨水屏时钟。其中天气基于高德天气API：https://lbs.amap.com/

## 目前功能
- 日期
- 星期
- 距离开资日期（默认为每月十日，目前不太智能，后续会修改，如果有后续）
- 今日温度
- 今日天气
- 明日气温（低温/高温）
- 明日天气
- 明日天气更新时间


## 需要优化点/增加功能
- 星期刷新时候可能会重叠，应该定期刷新
- 明天天气更新时间重叠，解决方法同上
- 增加温度/湿度等传感器，在页面上显示
- 增加MQTT支持，显示推送信息
- 接入智能家居homeassistant
- 增加开关控制页面切换，比如：天气4天显示和时间切换

## 1.安装库

    sudo apt-get update
    sudo apt-get install python-pip
    sudo apt-get install python-pil
    sudo apt-get install python-numpy
    sudo pip install RPi.GPIO
    
 
## 2.打开树莓派SPI
![avatar](https://github.com/88431844/epaperClock/blob/master/img/raspi-config.JPG)
![avatar](https://github.com/88431844/epaperClock/blob/master/img/spi.JPG)

通过raspi-config ,打开SPI后重启。

## 3.supervisor配置


supervisor配置中增加：
```
[program:epaperClock]
command=python3 /root/epaperclock/code/c.py
autorestart=true ;程序退出自动重启
```
## 显示效果


![avatar](https://github.com/88431844/epaperClock/blob/master/img/clockImg.JPG)
