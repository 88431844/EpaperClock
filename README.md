# epaperClock
a epaper project,driver by raspberry zero w,show on epaper.
##
supervisor配置中增加：
```
[program:epaperClock]
command=python3 /root/epaperclock/code/c.py
autorestart=true ;程序退出自动重启
```

![avatar](https://github.com/88431844/epaperClock/blob/master/IMG_4922.JPG)
