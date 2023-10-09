# Dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

COPY entrypoint.sh /app
# RUN chmod +x /app/entrypoint.sh

CMD ["./entrypoint.sh"]