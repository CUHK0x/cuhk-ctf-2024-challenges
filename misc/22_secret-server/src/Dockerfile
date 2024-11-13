FROM python:3.12-alpine

WORKDIR /app
COPY requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt
COPY . /app/

CMD ["python", "main.py"]