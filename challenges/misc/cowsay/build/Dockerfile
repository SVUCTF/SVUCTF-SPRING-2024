FROM tsl0922/ttyd:latest

RUN apt-get update && \
    apt-get install -y cowsay && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --chmod=500 challenge.sh /challenge.sh
COPY --chmod=500 init.sh /init.sh

CMD ["/init.sh"]
