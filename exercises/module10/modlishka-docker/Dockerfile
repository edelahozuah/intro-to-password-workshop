FROM golang:alpine AS builder
RUN apk add --no-cache git
WORKDIR /app
RUN git clone https://github.com/drk1wi/Modlishka.git .
# Build static binary
RUN CGO_ENABLED=0 GOOS=linux go build -o modlishka main.go

FROM alpine:latest
WORKDIR /app
RUN apk add --no-cache ca-certificates openssl
COPY --from=builder /app/modlishka /app/modlishka
# Copiamos templates por si acaso, aunque proxy mode no los usa mucho
COPY --from=builder /app/templates /app/templates
RUN mkdir -p /etc/modlishka
CMD ["/app/modlishka"]
