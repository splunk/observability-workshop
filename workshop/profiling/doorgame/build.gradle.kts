plugins {
    java
    id("com.github.johnrengelman.shadow") version "7.1.0"
}

repositories {
    mavenCentral()
}

tasks.withType<Jar> {
    manifest {
        attributes["Main-Class"] = "com.splunk.profiling.workshop.ServiceMain"
    }
}

dependencies {
    implementation("com.sparkjava:spark-core:2.9.4")
    implementation("org.slf4j:slf4j-api:2.0.18")
    runtimeOnly("org.slf4j:slf4j-simple:2.0.18")
    implementation("io.opentelemetry:opentelemetry-api:1.63.0")
    implementation("io.opentelemetry.instrumentation:opentelemetry-instrumentation-annotations:2.29.0")
    implementation("com.mysql:mysql-connector-j:9.3.0")

    constraints {
        implementation("org.eclipse.jetty:jetty-client:9.4.57.v20241219")
        implementation("org.eclipse.jetty:jetty-http:9.4.57.v20241219")
        implementation("org.eclipse.jetty:jetty-io:9.4.57.v20241219")
        implementation("org.eclipse.jetty:jetty-security:9.4.57.v20241219")
        implementation("org.eclipse.jetty:jetty-server:9.4.57.v20241219")
        implementation("org.eclipse.jetty:jetty-servlet:9.4.57.v20241219")
        implementation("org.eclipse.jetty:jetty-util:9.4.57.v20241219")
        implementation("org.eclipse.jetty:jetty-util-ajax:9.4.57.v20241219")
        implementation("org.eclipse.jetty:jetty-webapp:9.4.57.v20241219")
        implementation("org.eclipse.jetty:jetty-xml:9.4.57.v20241219")

        implementation("org.eclipse.jetty.websocket:websocket-api:9.4.57.v20241219")
        implementation("org.eclipse.jetty.websocket:websocket-client:9.4.57.v20241219")
        implementation("org.eclipse.jetty.websocket:websocket-common:9.4.57.v20241219")
        implementation("org.eclipse.jetty.websocket:websocket-server:9.4.57.v20241219")
        implementation("org.eclipse.jetty.websocket:websocket-servlet:9.4.57.v20241219")
    }
}