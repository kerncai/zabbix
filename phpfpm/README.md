在添加脚本之前，需要将所监控php-fpm需要在nginx内配置php-fpm的状态并转发出来，nginx内配置如下
配置完成后，可以打开浏览器查看下状态，是否可以正常访问

配置完成后，将脚本放在所需要监控的机器上面，模板导入到web即可

nginx配置如下：


server {

        listen 40080;
        server_name _;
        allow 127.0.0.1;
        deny all;
        access_log off;
        location /php-fpm_status {
        fastcgi_pass unix:/tmp/php-fpm.sock;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $fastcgi_script_name;
    
        }
       
location /nginx_status {   #这里配置的是nginx的状态，和php-fpm的监控一样
        
       stub_status on;
     
       }

}
      
         
         

         
         
         
