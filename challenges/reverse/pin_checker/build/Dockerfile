FROM ghcr.io/svuctf/base-v2/xinetd:latest

COPY xinetd.conf /etc/xinetd.conf
COPY --chmod=544 pin_checker /pin_checker

CMD ["xinetd", "-dontfork"]
