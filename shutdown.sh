#!/bin/bash

WORKDIR=$PWD
if [ ! -f .run.lock ]; then
    echo "Server might be already shutdown"
    exit 1
fi
if [ -f .run.lock ]; then
    PID=`cat .run.lock`
    `kill $PID`
    `rm .run.lock`
fi
