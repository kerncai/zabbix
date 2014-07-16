#########################################################################
# File Name: oracle_cron.sh
# Author: kerncai
# mail: kernkerncai@gmail.com
# Created Time: 2014年07月16日 星期三 11时05分47秒
#########################################################################
#user:oracle
#!/bin/bash

ource /home/oracle/.bash_profile

sqlplus -s / as sysdba > /usr/local/zabbix-howbuy-agent/var/tablespace.log<<EOF

set feed off
set linesize 100
set pagesize 200
select
a.tablespace_name,
SUM(a.bytes)/1024/1024 "CurMb",
SUM(decode(b.maxextend, null, A.BYTES/1024/1024, b.maxextend*8192/1024/1024)) "MaxMb",
(SUM(a.bytes)/1024/1024 - round(c."Free"/1024/1024)) "TotalUsed",
(SUM(decode(b.maxextend, null, A.BYTES/1024/1024, b.maxextend*8192/1024/1024)) - (SUM(a.bytes)/1024/1024 - round(c."Free"/1024/1024))) "TotalFree",
round(100*(SUM(a.bytes)/1024/1024 - round(c."Free"/1024/1024))/(SUM(a.bytes)/1024/1024)) "CURPercent",
round(100*(SUM(a.bytes)/1024/1024 - round(c."Free"/1024/1024))/(SUM(decode(b.maxextend, null, A.BYTES/1024/1024, b.maxextend*8192/1024/1024)))) "AUTOPercent"
from
dba_data_files a,
sys.filext$ b,
(SELECT d.tablespace_name , sum(nvl(c.bytes,0)) "Free" FROM dba_tablespaces d,DBA_FREE_SPACE c where d.tablespace_name = c.tablespace_name(+) group by d.tablespace_name) c
where a.file_id = b.file#(+)
and a.tablespace_name = c.tablespace_name
GROUP by a.tablespace_name, c."Free"/1024
having round(100*(SUM(a.bytes)/1024/1024 - round(c."Free"/1024/1024))/(SUM(a.bytes)/1024/1024)) >0
and round(100*(SUM(a.bytes)/1024/1024 - round(c."Free"/1024/1024))/(SUM(decode(b.maxextend, null, A.BYTES/1024/1024, b.maxextend*8192/1024/1024)))) > 0
order by round(100*(SUM(a.bytes)/1024/1024 - round(c."Free"/1024/1024))/(SUM(decode(b.maxextend, null, A.BYTES/1024/1024, b.maxextend*8192/1024/1024)))) ;
exit;
EOF
