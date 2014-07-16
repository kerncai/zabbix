

zabbix监控oracle

1，Orabbix插件的下载

http://www.smartmarmot.com/product/orabbix/download/

 也可以直接搜索下载，目前最新版本为1.2.3

  

 下载插件：wget http://www.smartmarmot.com/downloads/orabbix-1.2.3.zip

  

 2.环境配置

 若是没有java 需要安装java环境

 查看java环境：

 [root@wap ~]# whereis java
 java:

 安装java环境：

 [root@wap ~]# yum install java  这里需要查看下安装的java会对系统本身造成什么更改

 安装完成后查看：

 [root@wap ~]# whereis java
 java: /usr/bin/java /etc/java /usr/lib/java /usr/share/java /usr/share/man/man1/java.1.gz

 2.2 创建一个目录作为orabbix的源地址：

 mkdir -p /usr/local/orabbix

 解压缩插件：

 [root@wap ~]# unzip -n orabbix-1.2.3.zip -d /usr/local/orabbix/

 确认一下是否有oracle帐号 （这步可以不操作，因为本身是监控oracle，肯定会有帐号）

 [root@wap local]# id oracle
 uid=552(oracle) gid=552(oinstall) groups=552(oinstall),553(dba)


        给定目录权限：

         

        [root@wap local]# chown -R oracle. orabbix/

        drwxr-xr-x 7 oracle oinstall 4096 Apr 30 17:26 orabbix/

        3.更改配置文件：

        cd /usr/local/orabbix/

        [root@wap orabbix]# cp conf/config.props.sample conf/config.props

        顺带这添加下系统启动脚本：

        [root@wap orabbix]# cp init.d/orabbix /etc/init.d/orabbix

        [root@wap conf]# pwd
        /usr/local/orabbix/conf
        [root@wap conf]# vim config.props

        [root@wap conf]# cat config.props|grep -v "^$"|grep -v "^#"
        ZabbixServerList=ZabbixServer

        ZabbixServer.Address=10.40.40.15
        ZabbixServer.Port=10051


        OrabbixDaemon.PidFile=./logs/orabbix.pid
        OrabbixDaemon.Sleep=300
        OrabbixDaemon.MaxThreadNumber=100

        DatabaseList=DB_MON

        DatabaseList.MaxActive=10
        DatabaseList.MaxWait=100
        DatabaseList.MaxIdle=1

        DB_MON.Url=jdbc:oracle:thin:@10.168.109.22:1521:DB_MON
        DB_MON.User=zabbix
        DB_MON.Password=zabbix
        DB_MON.MaxActive=10
        DB_MON.MaxWait=100
        DB_MON.MaxIdle=1
        DB_MON.QueryListFile=./conf/query.props

        创建zabbix用户

        1,账号创建,指定数据及临时表空间profile及账号状态;
        　　create user zabbix identified by zabbix default tablespace system temporary tablespace temp profile default account unlock;

        2,给账号赋权限

        　　grant connect,resource,dba to zabbix;
        　　alter user zabbix default role all;
        　　grant select any table to zabbix;
        　　grant create session to zabbix;
        　　grant select any dictionary to zabbix;
        　　grant unlimited tablespace to zabbix;

        完成之后，/etc/init.d/orabbix start

