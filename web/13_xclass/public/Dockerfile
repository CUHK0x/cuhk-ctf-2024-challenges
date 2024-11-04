FROM python:3.13-rc-alpine

RUN apk add chromium-chromedriver

# Add cache directory for selenium
RUN mkdir /.cache/
RUN mkdir /.cache/selenium
RUN chmod -R 777 /.cache/selenium/

WORKDIR /app
RUN python -m venv .venv
RUN . .venv/bin/activate
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Change on deployment!
ENV HOSTNAME=localhost:24013

USER nobody
EXPOSE 24013

CMD ["python", "-m", "flask", "run", "--port", "24013", "--host", "0.0.0.0"]