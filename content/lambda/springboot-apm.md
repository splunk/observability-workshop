# Enable APM for Mobile Shop Springboot App

## 1. Validate APM Environment

The first activity we are going to do is validate that we have access to the Splunk APM environment and establish our starting point. To do this please login to Splunk Infrastructure & APM and select **APM**.

![APM-MENU](../images/lambda/springboot-apm/IsAPMAvailable.png)

This will bring you to the APM monitoring page, depending how many services you are currently monitoring with Splunk APM, you may or may not see a list of services.

Once you have run the applications with APM enabled, you can filter the environment by entering your unique id you have been provided. This should then show just your APM environment.

![APM-MENU](../images/lambda/springboot-apm/APM-monitor.png)

So lets start enabling APM in our environment.

---

## 2. Update the settings in the spring boot app

To enable APM on the Spring boot application we need to update the FrameWork (pom.xml), update the application settings en add enable some lines in the code.

### 2.1 Update the FrameWork by updating POM.XML

Connect back into your EC2 instance and stop the running Spring boot application by pressing ++ctrl+c++.

Once the application is stopped, open an editor and edit the pom.xml file
=== "Shell Command"

    ```text
    nano pom.xml
    ```

Scroll down until you find the following section
![pom-1](../images/lambda/springboot-apm/POM_xml-1.png)

and remove the comment marks lines *(<-- & -->)* by placing the cursor on the line with the remark and press ++ctrl+k++

Afterwards the section will look like this:
![pom-2](../images/lambda/springboot-apm/POM_xml-2.png)

Make sure the lines are properly aligned and save the file by pressing ++ctrl+o++ followed by ++enter++ to write the file pom.xml to disk.

You can now leave the nano editor by pressing ++ctrl+x++. This should bring you back to the command line.

### 2.2 Update the application property file

Edit the application property file of the springboot application in the nano editor by enter in the following command:

=== "Shell Command"

    ```text
    nano src/main/resources/application.properties
    ```

Remove the comment marks `##` on the following 2 lines:

    ```java
    ##spring.sleuth.sampler.probability=1.0

    ##spring.zipkin.baseUrl=http://localhost:9080
    ```

The first line tells the springboot app to send 100% of the traces to Splunk APM and the second line directs the traces and spans to the local local OpenTelemetry Collector that will forward them to splunk APM.

Your file should now look like this:

=== "application.properties File"

    ```text

    spring.thymeleaf.cache=false
    spring.thymeleaf.enabled=true
    spring.thymeleaf.prefix=classpath:/templates/
    spring.thymeleaf.suffix=.html

    server.port=8080
    spring.application.name=ACME-Mobile-Web-Shop-Base

    # For Sleuth 2.1+ use this property
    ## Enable this for full fidelity tracing   
    spring.sleuth.sampler.probability=1.0

    # The base url with the endpoint (/api/v2/spans) excluded
    # OpenTelemetry Collector deployed in your TKE namespace
    ## Enable this to send Traces to SignalFX
    spring.zipkin.baseUrl=http://localhost:9080
    ```
Now save the file by pressing ++ctrl+o++ followed by enter to write the file applications.properties file to disk.

You can now leave the nano editor by pressing ++ctrl+x++. This should bring you back to the command line.

### 2.3 Update the source code by enabling APM

Open the main java file of the springboot application in the nano editor by enter in the following command:

=== "Shell Command"

    ```text
    nano src/main/java/com/sfx/JavaLambda/JavaLambdaController.java
    ```

Remove the comment marks /\* & \*/ around the following three lines:

    /*
    import brave.sampler.Sampler;
    import brave.SpanCustomizer;
    import brave.Tracer;
    */

And remove the comment marks // in front of the following two lines:

    //@Autowired Tracer tracer;
    //@Autowired SpanCustomizer span;

So that your JavaLambdaController.java file now looks like this (note only the first 33 lines are shown below for brevity):

=== "JavaLambdaController.java"

    ```text
    package com.sfx.JavaLambda;

    import org.slf4j.Logger;
    import org.slf4j.LoggerFactory;
    import com.fasterxml.jackson.databind.ObjectMapper;
    import com.fasterxml.jackson.databind.ObjectReader;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.context.annotation.Bean;
    import org.springframework.http.*;
    import org.springframework.web.bind.annotation.GetMapping;
    import org.springframework.web.client.RestTemplate;
    import org.springframework.beans.factory.annotation.Value;
    import org.springframework.stereotype.Controller;
    import org.springframework.ui.Model;
    import org.springframework.web.bind.annotation.RequestParam;
    import org.springframework.web.bind.annotation.ModelAttribute;
    import org.springframework.web.bind.annotation.PostMapping;
    import java.util.*;
    import java.io.IOException;

    import brave.sampler.Sampler;
    import brave.SpanCustomizer;
    import brave.Tracer;

    @Controller
    public class JavaLambdaController {
        // set up AutoWired sleuth for APM

            @Autowired Tracer tracer;
            @Autowired SpanCustomizer span;
    ```
Now save the file by pressing ++ctrl+o++ followed by enter to write the file Java file to disk.
You can now leave the nano editor by pressing ++ctrl+x++. This should bring you back to the command line.

### 2.4 Run the App

Run the application by issuing the following command again:

=== "Shell Command"

    ```text
    mvn spring-boot:run 
    ```
When you have updated the files correctly you should see the SpringBoot logo again with no errors .

![ec2-loaded](../images/lambda/initial_run/Springboot.png)

We are now ready to test the app and send our first Trace.
!!! info
    If you get errors:

    Please make sure that all the files are properly aligned and replace any leading spaces with Tabs

Continue to the next section.
