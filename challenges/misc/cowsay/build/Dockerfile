FROM alpine as builder
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add -U perl git
RUN git clone https://github.com/tnalpgge/rank-amateur-cowsay && \
    cd rank-amateur-cowsay && \
    ./install.sh /usr/

FROM python:alpine

ENV FLASK_APP=app FLASK_ENV=production FLASK_ENV_DEBUG=False

RUN pip install flask gunicorn --no-cache-dir && \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add -U --no-cache perl

COPY --from=builder /usr/bin/cowsay /usr/bin/
COPY --from=builder /usr/share/cows /usr/share/cows

COPY --chmod=500 init.sh /init.sh
COPY ./app /app

CMD ["/init.sh"]
