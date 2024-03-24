FROM python:alpine

RUN apk add curl bash --no-cache -U

WORKDIR /app
COPY --chmod=775 init.sh init.sh
COPY server.py server.py

CMD ["./init.sh"]
