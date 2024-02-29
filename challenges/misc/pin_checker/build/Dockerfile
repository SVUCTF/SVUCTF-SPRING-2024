FROM ghcr.io/svuctf/base-v2/xinetd:latest

COPY xinetd.conf /etc/xinetd.conf
COPY --chmod=544 pin_checker /pin_checker

ENV PIN="12345678"
ENV GZCTF_FLAG="flag{test_flag}"

CMD ["xinetd", "-dontfork"]
