FROM python:3.12-alpine

RUN apk add curl

WORKDIR /app
COPY . /app/
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

ENV PORT=5000
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "app:app"]