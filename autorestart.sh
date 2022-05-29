#!/bin/bash

myscript(){
    python3 WebScrapperUnited.py
}

while true
do
until myscript; do
    echo "'myscript' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
done