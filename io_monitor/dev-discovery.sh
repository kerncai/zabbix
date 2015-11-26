#!/bin/bash

num=$(iostat |grep -ni device:|awk '{print $1}'|awk -F\: '{print $1 }')
((num=num+1))
###增加lvm的监控
DEVICES=$(iostat |sed -n "$num,$ p"|awk '{print $1}')
COUNT=`echo "$DEVICES" | wc -l`
INDEX=0
echo '{"data":['
echo "$DEVICES" | while read LINE; do
    echo -n '{"{#DEVNAME}":"'$LINE'"}'
    INDEX=`expr $INDEX + 1`
    if [ $INDEX -lt $COUNT ]; then
        echo ','
    fi
done
echo ']}'

