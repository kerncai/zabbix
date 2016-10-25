#!/usr/bin/env python 
#encoding:utf-8
#owner:kerncai

import os
import re
import sys
import time,datetime
import smtplib
import urllib2,cookielib,urllib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class mail:
    def __init__(self):
        self.login_url = 'http://zabbix.test/zabbix/index.php'
        self.zab_user = 'Admin'
        self.zab_passwd = 'passwd'

    def GetItemID(self,body):
        try:
            ItemID = re.match(r'.*ItemID:(\d+)[^\d]+.*',body.replace('\n',''),re.S).group(1)  
        except:
            pass
        return ItemID

    def GetTime(self):
        itemtime = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y%m%d%H%M%S")
        return itemtime

    def GetImage(self,body):
        login_data = urllib.urlencode({
                        "name": self.zab_user,
                        "password": self.zab_passwd,
                        "autologin": 1,
                        "enter": "Sign in"})
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
        urllib2.install_opener(opener)
        r = opener.open(self.login_url,login_data).read()
        zab_img_url = 'http://zabbix.test/zabbix/chart.php?period=3600&stime=%s&itemids[0]=%s&type=0&updateProfile=1&profileIdx=web.item.graph&profileIdx2=%s&width=1138' %(self.GetTime(),self.GetItemID(body),self.GetItemID(body))
        s = opener.open(zab_img_url)
        image_data = s.read()
        s.close()
        if s.info().get('Content-Type') == "image/png":
            image_file = open('/usr/lib/zabbix/alertscripts/imgs/%s.png' %self.GetItemID(body),'wb')
            image_file.write(image_data)
            image_file.close()     

    def sendmail(self,receiver,title,body):
        logfile = open('/usr/lib/zabbix/alertscripts/logs/alarm_mail.log','a')
        host = 'smtp.test.com'
        port = 25
        sender = 'zabbix@test.com'
        pwd = 'passwd'
        
        msg = MIMEMultipart('related')
        msg['subject'] = title
        msg['from'] = sender
        msg['To'] = ','.join(receiver)
        con_txt = MIMEText(body, 'html','utf-8')
        msg.attach(con_txt)
        img_path = '/usr/lib/zabbix/alertscripts/imgs/%s.png' %self.GetItemID(body)
        if os.path.exists(img_path):
            a = open(img_path,'r')
            img = a.read()
            a.close()
        else:
            a = open('/usr/lib/zabbix/alertscripts/imgs/404.jpg','r')
            img = a.read()
            a.close()
        con_img = MIMEImage(img)
        con_img.add_header('Content-ID','<img1>')
        msg.attach(con_img)
        try:  
            s = smtplib.SMTP(host, port)
            s.login(sender, pwd)
            s.sendmail(sender, receiver, msg.as_string())
            print 'The mail named %s to %s is sended successly.' % (title, receiver)
            log = '%s, OK,%s,%s\n' %(time.ctime(),title,receiver)
        except Exception,e:
            print "失败："+str(e)
            log = '%s, Fail,%s,%s,%s\n' %(time.ctime(),title,receiver,str(e))
        logfile.write(log)
        logfile.close()

if __name__=='__main__':
    run = mail()
    receiver = []
    receiver.append(sys.argv[1])
    title = sys.argv[2]
    body = sys.argv[3]
    run.GetItemID(body)
    old_img = '/usr/lib/zabbix/alertscripts/imgs/%s.png' %run.GetItemID(body)
    rm_cmd = 'rm -fv %s' %old_img
    os.system(rm_cmd)
    run.GetImage(body)
    run.sendmail(receiver,title,body)
    del run
