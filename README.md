zabbix
======

The template of apache.memcached.redis.squid and varnish what the zabbix haved

通过zabbix的自定义脚本监控web的中间件服务，强大的zabbix，只要脚本能写出来，就能做到监控！

上面提到的监控，仓库内都是有脚本和模板的.例子：监控squid

[root@monitor_test /]# cat check_squid_status.sh 

#!/bin/bash

five_min(){
    squidclient -h localhost -p 3128 mgr:info |grep 'Request Hit Ratios:' |awk '{print$5/100}' #5分钟的命中率
}

six_min(){
    squidclient -h localhost -p 3128 mgr:info |grep 'Request Hit Ratios:' |awk '{print$7/100}' #60分钟内的命中率
}

objects(){
    squidclient -h localhost -p 3128 mgr:info |grep 'on-disk objects' |awk '{print$1}'  #缓存的数量
}

space(){
    cat /var/log/squid.txt |grep 'Filesystem Space in use:' |awk -F '/' '{print$1}'|awk '{s+=$5};END{printf "%4.2f\n",s/1024/1024}'#缓存的大小，已经换算成G.
}

$1

