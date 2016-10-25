#####################################

zabbix_send_image.py 用途：

  可实现告警触发的同时，将该告警时间点，往前推3600秒，获取改item的数据曲线图，
以方便排错

action.xml 需要在action内，创建动作，默认信息需要填action.xml的内容，将zabbix的url换成
当前正在使用的即可。
