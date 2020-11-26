# Initial run of Splunk Mobile Phone Shop Application 

!!! important "Required information"
    **You should have the following information at hand as you will need this in various places throughout the workshop**

    - Access to the AWS account that is used to setup the workshop. 
    - The region the Workshop is using to run the workshop (f.e. Ireland, Frankfurt,
      Ohio, Tokio ..)
    - A Preset allowing you to identify your services etc.
    - IP address & password of the EC2 instances assigned to you.

---
## 1. Validate availability of Lambda Functions
Please log into the AWS account that has been used to create the workshop and select the region that is used by the workshop.

![AWS-Lambda-region](../../images/lambda/Initial_run/AWS Management Console Lambda.png){: .zoom}

Once the Lambda service have been selected you should see a list of available Lambda Functions.  To find the ones that are assigned to you, use the filter option, to see only the ones for you - **ACME** in our example
You should have:

 - RetailOrder_**Preset**
 - RetailOrderLine_**Preset**
 - RetailOrderPrice_**Preset**
 - RetailOrderDiscount_**Preset**

(Replace **Preset** with the text you have been provided)
![AWS-Lambda-filtered](../../images/lambda/Initial_run/Functions - Lambda filtered.png){: .zoom}

---
## 2. Verify CloudWatch logs location

To verify issues that may occur during the run, we need to check the CloudWatch logs.
Please open or clone a second Browser window to the same AWS account. The service to select is CloudWatch this time.

![AWS-Cloudwatch](../../images/lambda/Initial_run/CloudWatch.png){: .zoom}

The activity to pick in CloudWatch is the Log Group section.
 
![AWS-Cloudwatch-logGroups](../../images/lambda/Initial_run/CloudWatch_LogGroups.png){: .zoom}

If there logs present, you can filter on your preset like before. The result should be that there are no logs visible (see below). If there are logs, even after filtering on your preset, make sure they are not be related to the 4 service above, or delete them if possible)

![AWS-Cloudwatch-no-logs](../../images/lambda/Initial_run/CloudWatch_No_logs.png){: .zoom}

---
## 3. Connect to your EC2 instance
Next open a Terminal window and log into your EC2 instance you have been assigned.
If you need help with this, here are the instructions how to access you pre-configured [AWS/EC2 instance](../../../smartagent/connect-info/). Please return here after successfully connection to you instance.

Once connected move into the correct directory to run the Java SpringBoot application.
=== "Shell Command"

    ```text
    cd ~/SplunkLambdaAPM/LocalLambdaCallers/JavaLambdaBase
    ```

From here we will start the Java SpringBoot application that contains out simple web shop application.
Run the application by issuing the following command:

=== "Shell Command"

    ```text
    mvn spring-boot:run 
    ```
 

!!! info
    If you get the following error: 
    
    Command 'mvn' not found, but can be installed with:

    sudo apt install maven

    Maven has been updated and you can fix this by running the following commands:
   
    ```text
    sudo apt-get  update
    sudo apt-get install maven
    ```
    Please respond with Y to any prompt and try the mvn command again.
 

 On the first run SpringBoot will download a lot of packages, be patience!
 The next runs will be
![ec2-download](../../images/lambda/Initial_run/downloading.png){: .zoom}

but if everything is loaded you should see the SpringBoot logo.

![ec2-loaded](../../images/lambda/Initial_run/Springboot.png){: .zoom}

We are now ready to test the app.

---
## 4. Test the Splunk mobile phone shop app

Please open a new browser tab and surf to  http://[ec2_ip]:8080/order (where [ec2_ip] ids the ip address of you assigned EC2 instance)

![ec2-shop1](../../images/lambda/Initial_run/Shop.png){: .zoom}

To test enter the following information:
    - Name of a phone: for example *Geoff's big pictures phone*
    - Quantity:  *2*
    - Select a customer type: *Silver*

And hit submit to run a test

The result should be simulair to this :
![ec2-shop2](../../images/lambda/Initial_run/Shop-result.png){: .zoom} 
    
---
## 4. Verify logs in Cloudwatch

Even if there are no errors and you ahve the above result  check the Cloudwatch logs:
Go to CloudWatch Browser tab  hit the refresh button and check if all four logs have been generated.

![ec2-shop3](../../images/lambda/Initial_run/ClouwdWatchLogs-created.png){: .zoom} 

If this is correct we are now ready to add Traces and span's



