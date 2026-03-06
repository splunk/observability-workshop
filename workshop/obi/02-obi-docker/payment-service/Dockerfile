FROM golang:1.22-bookworm AS build
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY main.go ./
RUN CGO_ENABLED=0 go build -o /bin/payment-service .

FROM debian:bookworm-slim
RUN useradd -r appuser
COPY --from=build /bin/payment-service /usr/local/bin/payment-service
USER appuser
EXPOSE 8081
ENTRYPOINT ["payment-service"]
