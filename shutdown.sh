#!/bin/bash

WORKDIR=$PWD
LOGFILE=$WORKDIR/mbga/log/webserver.log

if [ ! -f .run.lock ]; then
    echo "Server might be already shutdown"
    exit 1
fi
if [ -f .run.lock ]; then
    echo "-> Stopping..."
    PID=`cat .run.lock`
    CID=`pgrep -P $PID`
    `kill $PID`
    `kill $CID`
    `rm .run.lock`
    echo "-> Webserver stopped!"
    echo "-> Stop @ `date`" >> $LOGFILE
    echo "" >> $LOGFILE
fi
