# HTTP를 HTTPS로 리다이렉트
#server {
#    listen ${LISTEN_PORT};
#    server_name hoya9802.com;
#    return 301 https://$server_name$request_uri;
#}
#
# HTTPS server
#server {
#    listen 443 ssl;
#    server_name hoya9802.com;
#
#    ssl_certificate /etc/nginx/ssl/fullchain.pem;
#    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
#    include /etc/letsencrypt/options-ssl-nginx.conf;
#    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
#
#    location /static {
#        alias /vol/static;
#    }
#
#    location / {
#        uwsgi_pass           ${APP_HOST}:${APP_PORT};
#        include              /etc/nginx/uwsgi_params;
#        client_max_body_size 10M;
#
#        # 프록시 헤더 설정 추가
#        proxy_set_header X-Real-IP $remote_addr;
#        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#        proxy_set_header Host $http_host;
#    }
#}

# HTTP server
server {
    listen ${LISTEN_PORT};

    location /static {
        alias /vol/static;
    }

    location / {
        uwsgi_pass           ${APP_HOST}:${APP_PORT};
        include              /etc/nginx/uwsgi_params;
        client_max_body_size 10M;
    }
}
