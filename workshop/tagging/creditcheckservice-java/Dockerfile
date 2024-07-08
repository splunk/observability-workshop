FROM eclipse-temurin:22-jdk-alpine as builder

ENV BUILD_HOME=/workspace/app
ENV ARTIFACTS=${BUILD_HOME}/target/dependency
ENV USR=svc
ENV GRP=svc
ENV UID=5001
ENV GID=5001

RUN addgroup --gid ${GID} -S ${GRP} \
    && adduser --disabled-password --gecos "" --ingroup ${GRP} --no-create-home --uid ${UID} --system ${USR}
RUN mkdir -p ${BUILD_HOME} && chown ${USR}:${GRP} -R ${BUILD_HOME}
USER ${USR}

WORKDIR ${BUILD_HOME}/

RUN wget https://github.com/signalfx/splunk-otel-java/releases/download/v1.32.0/splunk-otel-javaagent.jar -O ${BUILD_HOME}/splunk-otel-javaagent.jar

COPY --chown=${USR}:${GRP} mvnw .
COPY --chown=${USR}:${GRP} .mvn .mvn
COPY --chown=${USR}:${GRP} pom.xml .
COPY --chown=${USR}:${GRP} src src

RUN --mount=type=cache,uid=${UID},gid=${GID},target=/home/${USR}/.m2 ./mvnw clean install -DskipTests
RUN mkdir -p ${ARTIFACTS} && (cd ${ARTIFACTS}; find .. -type f -name "*.jar" -exec jar -xf {} \;)

FROM eclipse-temurin:22-jre-alpine

ENV USR=svc
ENV GRP=svc
ENV UID=5001
ENV GID=5001
ENV BUILD_HOME=/workspace/app
ENV ARTIFACTS=${BUILD_HOME}/target/dependency
ENV ARTIFACT_NAME=creditcheckservice-0.0.1-SNAPSHOT.jar
ENV APP_HOME=/app
ENV APP_NAME=com.example.creditcheckservice.CreditCheckApplication

RUN addgroup --gid ${GID} -S ${GRP} \
    && adduser --disabled-password --gecos "" --ingroup ${GRP} --no-create-home --uid ${UID} --system ${USR}
RUN mkdir -p ${APP_HOME} && chown ${USR}:${GRP} -R ${APP_HOME}

USER ${USR}
WORKDIR ${APP_HOME}
COPY --chown=${USR}:${GRP} --from=builder ${BUILD_HOME}/splunk-otel-javaagent.jar ${APP_HOME}/
COPY --chown=${USR}:${GRP} --from=builder ${ARTIFACTS}/BOOT-INF/lib /app/lib
COPY --chown=${USR}:${GRP} --from=builder ${ARTIFACTS}/META-INF /app/META-INF
COPY --chown=${USR}:${GRP} --from=builder ${ARTIFACTS}/BOOT-INF/classes /app

ENTRYPOINT java \
    -javaagent:${APP_HOME}/splunk-otel-javaagent.jar \
    -Dotel.java.global-autoconfigure.enabled=true \
    -cp ${APP_HOME}:${APP_HOME}/lib/* "${APP_NAME}"
