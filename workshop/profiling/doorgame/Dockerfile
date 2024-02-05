FROM gradle:8.6.0-jdk11-jammy AS build
COPY --chown=gradle:gradle . /home/gradle/src
WORKDIR /home/gradle/src
#RUN gradle build --no-daemon
RUN ./gradlew shadowJar

FROM openjdk:11-jre-slim as final

EXPOSE 9090

RUN mkdir /app

COPY --from=build /home/gradle/src/build/libs/*.jar /app/profiling-workshop-all.jar

# Adds the latest version of the Splunk Java agent
ADD https://github.com/signalfx/splunk-otel-java/releases/latest/download/splunk-otel-javaagent.jar .

# Modifies the entry point
ENTRYPOINT ["java","-javaagent:splunk-otel-javaagent.jar","-jar","/app/profiling-workshop-all.jar"]