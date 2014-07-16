#########################################################################
# File Name: oracle_check.sh
# Author: kerncai
# mail: kernkerncai@gmail.com
# Created Time: 2014年07月16日 星期三 11时07分09秒
#########################################################################
#!/bin/bash
EQ_DATA="$2"
ZBX_REQ_DATA_TAB="$1"

SOURCE_DATA=/usr/local/zabbix-howbuy-agent/var/tablespace.log

ERROR_NO_DATA_FILE="-0.9900"
ERROR_OLD_DATA="-0.9901"
ERROR_WRONG_PARAM="-0.9902"
ERROR_MISSING_PARAM="-0.9903"

# No data file to read from
if [ ! -f "$SOURCE_DATA" ]; then
  echo $ERROR_NO_DATA_FILE
  exit 1
fi

# Missing device to get data from
if [ -z "$ZBX_REQ_DATA_TAB" ]; then
  echo $ERROR_MISSING_PARAM
  exit 1
fi

device_count=$(grep -Ec $ZBX_REQ_DATA_TAB $SOURCE_DATA)
if [ $device_count -eq 0 ]; then
  exit 1
fi

case $ZBX_REQ_DATA in
#case $2 in
  totalused)        grep -E "$ZBX_REQ_DATA_TAB" $SOURCE_DATA |awk '{print $4*1024*1024}';;
  maxmb)        grep -E "$ZBX_REQ_DATA_TAB" $SOURCE_DATA |awk '{print $3}'| awk -F '.' '{print ($1-2048)*1024*1024}';;
  curpercent)   grep -E "$ZBX_REQ_DATA_TAB" $SOURCE_DATA |awk '{print $6}';;
  autopercent)  grep -E "$ZBX_REQ_DATA_TAB" $SOURCE_DATA |awk '{print $7}';;
  *) echo $ERROR_WRONG_PARAM; exit 1;;
esac

exit 0 
