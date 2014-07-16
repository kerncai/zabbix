#########################################################################
# File Name: check_asm_status.sh
# Author: kerncai
# mail: kernkerncai@gmail.com
# Created Time: 2014年07月16日 星期三 11时03分05秒
#########################################################################
#!/bin/bash
data_free() {
    cat /usr/local/zabbix-howbuy-agent/var/asm.log|grep -i data |awk '{print$2*1024*1024}'
}

data_used() {
    cat /usr/local/zabbix-howbuy-agent/var/asm.log|grep -i data |awk '{print$4*1024*1024}'
}

data_total() {
    cat /usr/local/zabbix-howbuy-agent/var/asm.log|grep -i data |awk '{print$3*1024*1024}'
}

data_used_retio() {
    cat /usr/local/zabbix-howbuy-agent/var/asm.log |grep -i data |awk 'END{printf "%4.2f\n",$4/$3*100}'
}

data_pfree() {
    cat /usr/local/zabbix-howbuy-agent/var/asm.log |grep -i data |awk 'END{printf "%4.2f\n",$2/$3*100}'
}


reco_free() {
    cat /usr/local/zabbix-howbuy-agent/var/asm.log|grep -i reco |awk '{print$2*1024*1024}'
}

reco_used() {
    cat /usr/local/zabbix-howbuy-agent/var/asm.log|grep -i reco |awk '{print$4*1024*1024}'
}

reco_total() {
    cat /usr/local/zabbix-howbuy-agent/var/asm.log|grep -i reco |awk '{print$3*1024*1024}'
}

reco_used_retio() {
    cat /usr/local/zabbix-howbuy-agent/var/asm.log |grep -i reco |awk 'END{printf "%4.2f\n",$4/$3*100}'
}

reco_pfree() {
    cat /usr/local/zabbix-howbuy-agent/var/asm.log |grep -i reco |awk 'END{printf "%4.2f\n",$2/$3*100}'
}

$1
