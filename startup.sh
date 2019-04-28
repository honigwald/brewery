#!/bin/bash

WORKDIR=$PWD
if [ -f .run.lock ]; then
    echo "Server might be already running"
    exit 1
fi
if [ ! -f .run.lock ]; then
    cd mbga/web
    npm start &
    echo $! >> $WORKDIR/.run.lock
fi
