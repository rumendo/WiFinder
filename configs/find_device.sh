#!/bin/bash

while true
do
    netstat -lan | grep 7000 | grep LISTEN > /dev/null
    if [[ $? -eq 0 ]]
    then
        expect -c 'spawn ssh-copy-id root@127.0.0.1 -p 7000 -o "StrictHostKeyChecking no"; expect "assword:"; send "toor\r"; interact'
        MAC=$(ssh root@127.0.0.1 -p 7000 -o "StrictHostKeyChecking no" 'cat /sys/class/net/eth0/address')
        # ADD LOCATION DATA COLLECTION
        PORT=$(psql -qtAX -d wifinder -c "INSERT INTO devices VALUES (DEFAULT, '4', '$MAC', currval('devices_id_seq')+7000, '(0, 0)', NOW()) RETURNING ssh_port;")
        scp -P 7000 -o "StrictHostKeyChecking no" root@127.0.0.1:/etc/cron.d/reverse_ssh /home/controller
        sed -i "s/7000/$PORT/g" /home/controller/reverse_ssh
        scp -P 7000 -o "StrictHostKeyChecking no" /home/controller/reverse_ssh root@127.0.0.1:/etc/cron.d
        ssh root@127.0.0.1 -p 7000 -o "StrictHostKeyChecking no" "kill \$(netstat -lanp | grep 78.130.176 | grep EST | awk '{print substr(\$7, 0, length(\$7) - 3)}')"
    fi
    sleep 10s
done
