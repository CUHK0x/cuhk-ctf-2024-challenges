FROM golang:1.23.2-alpine
WORKDIR /go/src/app
COPY go.mod go.sum /go/src/app/
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /go/bin/app

COPY entrypoint.sh flag.txt items.json static/ /go/bin/
RUN chmod +x /go/bin/entrypoint.sh
EXPOSE 8080
CMD ["/bin/sh", "-c", "/go/bin/entrypoint.sh"]
