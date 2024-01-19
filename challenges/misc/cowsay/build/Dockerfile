FROM alpine as builder
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add -U perl git
RUN git clone https://github.com/tnalpgge/rank-amateur-cowsay && \
    cd rank-amateur-cowsay && \
    ./install.sh /usr/

FROM alpine:latest

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add --no-cache openssh perl

RUN adduser -D ctf && passwd -d ctf && \
    sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords yes/' /etc/ssh/sshd_config && \
    echo 'ForceCommand /challenge.sh' >> /etc/ssh/sshd_config && \
    ssh-keygen -A

COPY --from=builder /usr/bin/cowsay /usr/bin/
COPY --from=builder /usr/share/cows /usr/share/cows

COPY --chmod=500 --chown=ctf challenge.sh /challenge.sh
COPY --chmod=500 init.sh /init.sh

CMD ["/init.sh"]
