#!/bin/bash

WORKDIR=$PWD
if [ -f .run.lock ]; then
    echo "Server might be already running"
    exit 1
fi
if [ ! -f .run.lock ]; then
    echo "-> Starting"
    cd mbga/web
    npm start &> $WORKDIR/mbga/log/webserver.log &
    #npm start &
    sleep 2
    PID=`pgrep -P $!`
    echo $PID >> $WORKDIR/.run.lock
    echo "-> Webserver started on Port 4000"
    echo "-> URL: http://$HOSTNAME:4000/index"
fi
