# only really known to work on ubuntu, if you're using anything else, hopefully
# it should at least give you a clue how to install it by hand
# TODO: parameterize this and the xml file (maybe scons?)
install:
	mkdir -p /usr/share/learning-ibus /etc/xdg/learning-ibus
	cp learning-ibus.py engine.py ibus-lung.svg /usr/share/learning-ibus
	chmod a+x /usr/share/learning-ibus/learning-ibus.py
	cp learning-ibus.xml /usr/share/ibus/component

uninstall:
	rm -rf /usr/share/learning-ibus
	rm -rf /etc/xdg/learning-ibus
	rm -f /usr/share/ibus/component/learning-ibus.xml
