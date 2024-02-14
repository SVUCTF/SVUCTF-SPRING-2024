FROM nginx:1.25.3-alpine

COPY --chown=www-data:www-data html/ /usr/share/nginx/html
COPY --chmod=500 init.sh /init.sh

CMD ["/init.sh"]
