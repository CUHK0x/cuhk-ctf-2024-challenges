FROM python:3.12-alpine

WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt
COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "-w", "4", "--threads", "4", "app:app"]
