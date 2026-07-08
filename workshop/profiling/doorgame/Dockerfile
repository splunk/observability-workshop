FROM eclipse-temurin:21-jdk-alpine as builder

ENV BUILD_HOME=/workspace/app
ENV ARTIFACTS=${BUILD_HOME}/target/dependency
ENV USR=svc
ENV GRP=svc
ENV UID=5001
ENV GID=5001

RUN addgroup --gid ${GID} -S ${GRP} \
    && adduser --disabled-password --gecos "" --ingroup ${GRP} --uid ${UID} --system ${USR}
RUN mkdir -p ${BUILD_HOME} /home/${USR} \
    && chown ${USR}:${GRP} -R ${BUILD_HOME} /home/${USR}
USER ${USR}

WORKDIR ${BUILD_HOME}/

COPY --chown=${USR}:${GRP} mvnw .
COPY --chown=${USR}:${GRP} .mvn .mvn
COPY --chown=${USR}:${GRP} pom.xml .
COPY --chown=${USR}:${GRP} src src

RUN ./mvnw clean install -DskipTests
RUN mkdir -p ${ARTIFACTS} && (cd ${ARTIFACTS}; find .. -type f -name "*.jar" -exec jar -xf {} \;)

FROM eclipse-temurin:21-jre-alpine

ENV USR=svc
ENV GRP=svc
ENV UID=5001
ENV GID=5001
ENV APP_HOME=/app
ENV APP_NAME=com.splunk.profiling.workshop.ServiceMain

RUN addgroup --gid ${GID} -S ${GRP} \
    && adduser --disabled-password --gecos "" --ingroup ${GRP} --no-create-home --uid ${UID} --system ${USR}
RUN mkdir -p ${APP_HOME} && chown ${USR}:${GRP} -R ${APP_HOME}

# Download agent as root so we can set ownership; ADD from URL doesn't support --chown
RUN apk add --no-cache curl && \
    curl -fsSL -o ${APP_HOME}/splunk-otel-javaagent.jar \
      https://github.com/signalfx/splunk-otel-java/releases/latest/download/splunk-otel-javaagent.jar && \
    chown ${USR}:${GRP} ${APP_HOME}/splunk-otel-javaagent.jar && \
    apk del curl

USER ${USR}
WORKDIR ${APP_HOME}

COPY --chown=${USR}:${GRP} --from=builder /workspace/app/target/dependency/BOOT-INF/lib /app/lib
COPY --chown=${USR}:${GRP} --from=builder /workspace/app/target/dependency/META-INF /app/META-INF
COPY --chown=${USR}:${GRP} --from=builder /workspace/app/target/dependency/BOOT-INF/classes /app

EXPOSE 9090

ENTRYPOINT java \
    -javaagent:${APP_HOME}/splunk-otel-javaagent.jar \
    -Dotel.java.global-autoconfigure.enabled=true \
    -cp ${APP_HOME}:${APP_HOME}/lib/* "${APP_NAME}"
