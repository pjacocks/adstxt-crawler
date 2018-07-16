#!/bin/bash

exec >> mongo_log.txt

mongod=/usr/local/bin/mongod
prog=mongod.sh
RETVAL=0

stop(){
    grep_mongo=$(ps aux | grep [m]ongod)
    if [ ${#grep_mongo} -ne 0 ]
    then
	   echo "Stop MongoDB."
	   PID=$(ps ax | grep [m]ongod | awk '{print $1}')
	   kill $PID
	   RETVAL=$?
    else
	   echo "MongoDB is not running."

    fi
}


start(){
    grep_mongo=$(ps aux | grep [m]ongod)
    if [ ${#grep_mongo} -ge 1 ]
    then
	   echo "MongoDB is already running."
    else
	   echo "Start MongoDB."
	   mongod &
	   RETVAL=$?
    fi
}


case "$1" in
    start)
	   start
	   ;;
    stop)
	   stop
	   ;;
*)
	echo $"Usage: $prog {start|stop}"
	exit 1
esac

exit $RETVAL

