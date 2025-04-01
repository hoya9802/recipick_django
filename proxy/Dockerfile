FROM nginx:1.21.5-alpine
LABEL maintainer="recipick_team"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000
ENV DOMAIN=hoya9802.com

USER root

RUN mkdir -p /vol/static && \
    mkdir -p /var/www/certbot && \
    chmod 755 /vol/static && \
    chmod 755 /var/www/certbot && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD [ "/run.sh" ]