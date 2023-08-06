#!/bin/bash

if [ -z "$1" ]; then
    echo 'No target provided !'
    echo "Usage: ./$0 target"
    exit 1
fi

#echo
#echo "msf> auxiliary/scanner/redis/redis_server"
#msfconsole -q -x "use auxiliary/scanner/redis/redis_server; set RHOSTS $1; run; exit" | sed 's/\\x0d\\x0a/\n/g'

echo
echo "$ nmap --script redis-info -sV -p 6379 $1"
nmap --script redis-info -sV -p 6379 "$1"

