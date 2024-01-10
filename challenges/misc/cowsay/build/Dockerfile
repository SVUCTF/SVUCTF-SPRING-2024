FROM alpine as builder
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add -U perl git
RUN git clone https://github.com/tnalpgge/rank-amateur-cowsay && \
    cd rank-amateur-cowsay && \
    ./install.sh /usr/

FROM tsl0922/ttyd:alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add -U perl --no-cache

COPY --from=builder /usr/bin/cowsay /usr/bin/
COPY --from=builder /usr/share/cows /usr/share/cows

COPY --chmod=500 challenge.sh /challenge.sh
COPY --chmod=500 init.sh /init.sh

CMD ["/init.sh"]
