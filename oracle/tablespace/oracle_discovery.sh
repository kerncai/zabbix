#########################################################################
# File Name: oracle_discovery.sh
# Author: kerncai
# mail: kernkerncai@gmail.com
# Created Time: 2014年07月16日 星期三 11时05分00秒
#########################################################################
#!/bin/bash

PACE=`cat /usr/local/zabbix-howbuy-agent/var/tablespace.log |awk '{print$1}'|awk 'NR>3{print}'`

COUNT=`echo "$TABLESPACE" |wc -l`
INDEX=0
echo '{"data":['
echo "$TABLESPACE" | while read LINE; do
    echo -n '{"{#TABLENAME}":"'$LINE'"}'
    INDEX=`expr $INDEX + 1`
    if [ $INDEX -lt $COUNT ]; then
        echo ','
    fi
done
echo ']}'
