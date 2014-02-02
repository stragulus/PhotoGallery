#!/usr/bin/env bash
PATH=/usr/bin:/bin

GALLERY_DIR=/home/brama/opt/gallery

case $1 in
start)
	$GALLERY_DIR/python/bin/uwsgi --ini-paste $GALLERY_DIR/development.ini
	exit $?
	;;
stop)
	kill $(cat $GALLERY_DIR/var/uwsgi.pid)
	;;
restart)
	$0 stop
	sleep 5
	$0 start
	;;
reload)
	kill -1 $(cat $GALLERY_DIR/var/uwsgi.pid)
	;;
*)
	echo "Usage: $0 start | stop | restart"
	exit 1;
	;;
esac
