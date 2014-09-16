#########################################################################
# File Name: port-discovery.sh
# Author: kerncai
# mail: kernkerncai@gmail.com
# Created Time: 2014年07月16日 星期三 11时23分40秒
#########################################################################
#!/bin/bash

portarray=(`netstat -tnlp|egrep -i "$1"|awk {'print $4'}|awk -F':' '{if ($NF~/^[0-9]*$/) print $NF}'|sort |uniq   2>/dev/null`)
length=${#portarray[@]}
printf "{\n"
printf  '\t'"\"data\":["
for ((i=0;i<$length;i++))
do
        printf '\n\t\t{'
        printf "\"{#TCP_PORT}\":\"${portarray[$i]}\"}"
        if [ $i -lt $[$length-1] ];then
                printf ','
        fi
done
printf  "\n\t]\n"
printf "}\n"
