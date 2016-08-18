### 四、程式運作進入點。

* 進入點

```
 $ ps aux|grep ibus
deanboo+ 12365  0.6  0.0 511136  8676 ?        Ssl  14:01   0:03 /usr/bin/ibus-daemon --daemonize --xim
deanboo+ 12379  0.0  0.0 281252  5884 ?        Sl   14:01   0:00 /usr/lib/ibus/ibus-dconf
deanboo+ 12380  0.2  0.1 462720 18208 ?        Sl   14:01   0:01 /usr/lib/ibus/ibus-ui-gtk3
deanboo+ 12382  0.0  0.0 386904  7396 ?        Sl   14:01   0:00 /usr/lib/ibus/ibus-x11 --kill-daemon
deanboo+ 12395  0.0  0.0 205156  5580 ?        Sl   14:01   0:00 /usr/lib/ibus/ibus-engine-simple
deanboo+ 12398  0.0  0.0 225584  5348 ?        Sl   14:01   0:00 /usr/lib/ibus/ibus-engine-pinyin --ibus
deanboo+ 12422  0.1  0.1 476268 17064 ?        Sl   14:02   0:00 /usr/lib/ibus/ibus-engine-chewing --ibus
deanboo+ 12428  0.0  0.0 226424 11588 ?        Sl   14:02   0:00 /usr/bin/python2 /usr/share/learning-ibus/learning-ibus.py --ibus
deanboo+ 12834  0.0  0.0  15948   920 pts/13   S+   14:12   0:00 grep ibus
```

可看到 ```/usr/bin/python2 /usr/share/learning-ibus/learning-ibus.py --ibus```。我們就以 learning-ibus.py 為程式進入點。
