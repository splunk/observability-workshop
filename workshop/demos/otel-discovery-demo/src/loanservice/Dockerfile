FROM eclipse-temurin:17-jdk AS builder

WORKDIR /src

COPY ./ ./

ENV KAFKA_BROKER=localhost:9092
ENV DB_URL="jdbc:mysql://localhost/MyDB"

RUN ./gradlew build

# -----------------------------------------------------------------------------

FROM eclipse-temurin:17-jre

WORKDIR /app

COPY --from=builder /src/build/libs/*.jar loanservice.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "./loanservice.jar"]