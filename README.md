# chatgpt-web-share-v4
### Frok from moeakwak/chatgpt-web-share
添加了poeapi等多api设置，添加了多个poe模型支持
## 待实现功能
 - ppt生成器
 - AI绘画
## Nginx配置方法
```Nginx
server {
    listen 80;
    server_name website;

    # Enforce HTTPS
    return 301 https://$server_name$request_uri;
}
server {
    server_name website;
    charset utf-8;
    listen 443 ssl http2 ;
    ssl_certificate /etc/ssl/certificate.cer;
    ssl_certificate_key /etc/ssl/private.key;


    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Vouch-User $auth_resp_x_vouch_user;

    }


}
```