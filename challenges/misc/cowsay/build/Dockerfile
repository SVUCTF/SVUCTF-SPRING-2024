FROM alpine as builder
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add -U perl git
RUN git clone https://github.com/tnalpgge/rank-amateur-cowsay && \
    cd rank-amateur-cowsay && \
    ./install.sh /usr/

FROM ghcr.io/svuctf/base/xinetd:alpine
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add -U perl --no-cache

COPY --from=builder /usr/bin/cowsay /usr/bin/
COPY --from=builder /usr/share/cows /usr/share/cows

COPY --chmod=500 init.sh /init.sh
COPY --chmod=544 challenge.sh /challenge.sh
COPY xinetd.conf /etc/xinetd.conf

CMD ["xinetd", "-dontfork"]
