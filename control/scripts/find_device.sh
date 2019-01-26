#!/bin/bash

while true
do
    netstat -lan | grep 7000 > /dev/null
    if [[ $? -eq 0 ]]
    then
        expect -c 'spawn ssh-copy-id rumen@127.0.0.1 -p 7000 -o "StrictHostKeyChecking no"; expect "assword:"; send "root\r"; interact'
        ssh rumen@localhost -p 7000 -o "StrictHostKeyChecking no" 'cat /sys/class/net/eth0/address'
    fi
    sleep 5s
done