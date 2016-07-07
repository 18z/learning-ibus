# only really known to work on ubuntu, if you're using anything else, hopefully
# it should at least give you a clue how to install it by hand
# TODO: parameterize this and the xml file (maybe scons?)
install:
	mkdir -p /usr/share/ibus-uniemoji /etc/xdg/uniemoji
	cp learning-ibus.py engine.py ibus-lung.svg /usr/share/ibus-uniemoji
	chmod a+x /usr/share/ibus-uniemoji/learning-ibus.py
	cp learning-ibus.xml /usr/share/ibus/component

uninstall:
	rm -rf /usr/share/ibus-uniemoji
	rm -rf /etc/xdg/uniemoji
	rm -f /usr/share/ibus/component/learning-ibus.xml
