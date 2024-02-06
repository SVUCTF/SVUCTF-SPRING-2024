FROM python:alpine

ENV FLASK_APP=app FLASK_ENV=production FLASK_ENV_DEBUG=False

RUN pip install flask gunicorn openai --no-cache-dir

COPY --chmod=500 init.sh /init.sh
COPY ./main.py /app/
COPY ./templates/ /app/templates/

WORKDIR /app

ENV OPENAI_BASE_URL="https://api.tutujin.com/v1/"
ENV OPENAI_API_KEY="sk-2H53P64mqXoa9JZG3731Cb58B7254916940dF3Af7b5fF68f"

CMD ["/init.sh"]
