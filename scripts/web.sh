#!/bin/bash

if [ -z "$1" ]; then
    echo 'No target provided !'
    echo "Usage: ./$0 target port"
    exit 1
elif [ -z "$2" ]; then
    echo 'No port provided !'
    echo "Usage: ./$0 target port"
    exit 2
fi

echo
echo "$ davtest $1:$2"
davtest $1:$2

