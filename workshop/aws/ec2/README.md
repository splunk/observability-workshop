# Instructions on how to set up EC2 cloud instances for participants

You will need access to an AWS account to obtain both **AWS_ACCESS_KEY_ID** and **AWS_SECRET_ACCESS_KEY**.

1. Initialize Terraform

    ```bash
    terraform init -upgrade
    ```

1. Create environment variables for **AWS_ACCESS_KEY_ID** and **AWS_SECRET_ACCESS_KEY**

    ```bash
    export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
    export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
    ```

1. Validate the environment variables are set

    ```bash
    echo $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY
    ```

Use the following terraform variables:

- `aws_region`: Which region do you want the instances in?
- `aws_instance_type`: What kind of instance?
- `aws_instance_count`: How many instances?

Sample command:

```bash
terraform apply \
-auto-approve \
-var="aws_region=eu-central-1" \
-var="aws_instance_type=t2.xlarge" \
-var="aws_instance_count=1"
```

Or you use the provided script `up` to request instances:

Install the prerequisites, e.g. on Mac: `brew install terraform jq pssh`

Then use the script:

```bash
./up myproject 12 eu-central-1
```

This will create a terraform workspace `o11y-for-myproject`, request 12 instances and ensure all instances have completed provisioning.
