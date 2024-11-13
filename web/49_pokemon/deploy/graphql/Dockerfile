FROM node:lts-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ENV PASSCODE="dish-percent-drop-brief"
CMD ["node", "server.js", "-w", "4"]