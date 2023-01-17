# Instructions on how to set up EC2 cloud instances for participants

You will need access to an AWS account to obtain both **AWS_ACCESS_KEY_ID** and **AWS_SECRET_ACCESS_KEY**.

1. Initialize Terraform

    ```bash
    terraform init -upgrade
    ```

2. Create environment variables for **AWS_ACCESS_KEY_ID** and **AWS_SECRET_ACCESS_KEY**

    ```bash
    export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
    export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
    ```

3. Validate the environment variables are set

    ```bash
    echo $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY
    ```

4. Use the following terraform variables:

    - `aws_region`: Which region do you want the instances in?
    - `aws_instance_count`: How many instances?
    - `slug`: Project name slug that will be used to tag aws resources
    - `splunk_access_token`: Observability Access Token
    - `splunk_rum_token`: Observability RUM Token
    - `splunk_realm`: Observability Realm
    - `splunk_presetup`: Provide a preconfigured instance (OTel Collector and Online Boutique deployed)
    - `splunk_jdk`: Install JDK on the instance

5. Edit the `terraform.tfvars` file and set the variables.

    ```text
    aws_region = ""
    aws_instance_count = ""
    slug = ""
    splunk_access_token = ""
    splunk_rum_token = ""
    splunk_realm = ""
    splunk_presetup = false
    splunk_jdk = false
    ```

Sample command:

```bash
terraform apply \
-auto-approve \
-var="aws_region=eu-central-1" \
-var="aws_instance_count=1" \
-var= "slug=myproject" \
-var="splunk_access_token=123xxx456xxx789" \
-var="splunk_rum_token=123xxx456xxx789" \
-var="splunk_realm=eu0" \
-var="splunk_presetup=true" \
-var="splunk_jdk=false"
```

Or you use the provided script `up` to request instances:

Install the prerequisites, e.g. on Mac: `brew install terraform jq pssh`

Then use the script:

```bash
./up myproject 12 eu-central-1
```

This will create a terraform workspace `o11y-for-myproject`, request 12 instances and ensure all instances have completed provisioning.
