FROM golang:1.22-bookworm AS build
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY main.go ./
RUN CGO_ENABLED=0 go build -o /bin/order-processor .

FROM debian:bookworm-slim
RUN useradd -r appuser
COPY --from=build /bin/order-processor /usr/local/bin/order-processor
USER appuser
EXPOSE 8080
ENTRYPOINT ["order-processor"]
