oracle_cron.sh 为oracle用户下的crontab  每分钟一次，用来将表空间信息提取出来
oracle_discovery.sh 将所需要的数据拼成json格式
oracle_check.sh 检测信息
tablespace.conf为配置文件
*.xml为zabbixserver端的模板，导入即可；这个模板包含了oracle的插件orabbix，里面的一些item做了精简,配置方法见orabbix.md
