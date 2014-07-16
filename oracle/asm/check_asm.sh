#########################################################################
# File Name: check_asm.sh
# Author: kerncai
# mail: kernkerncai@gmail.com
# Created Time: 2014年07月16日 星期三 11时02分04秒
#########################################################################
#user:oracle
#!/bin/bash
source /home/oracle/.bash_profile

sqlplus -s /  as sysdba > /usr/local/zabbix-howbuy-agent/var/asm.log <<EOF
set line 150;
select name,nvl(free_mb,0),nvl(total_mb,0),nvl(total_mb,0)-nvl(free_mb,0) from v\$asm_diskgroup where 100-round(nvl(free_mb,0)/total_mb*100,0)> 0;
exit;
EOF

