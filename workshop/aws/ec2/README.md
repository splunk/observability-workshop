# Instructions on how to set up EC2 cloud instances for participants

You will need access to an AWS account to obtain both **AWS_ACCESS_KEY_ID** and **AWS_SECRET_ACCESS_KEY**.

## 1. Initialize Terraform

```bash
terraform init -upgrade
```

## 2. Create environment variables

Create the required AWS environment variables: **AWS_ACCESS_KEY_ID** and **AWS_SECRET_ACCESS_KEY**

```bash
export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
```

## 3. Validate the environment variables are set

```bash
echo $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY
```

## 4. Create Terraform variables file

Variables are kept in file `terrform.tfvars` and we provide a template as `terraform.tfvars.template` to copy and edit:

```bash
cp terraform.tfvars.template terraform.tfvars
```

The file `terraform.tfvars` is ignored by git and should not be committed to the repo.

## 5. Set Terraform variables

The following variables are available. Edit `terraform.tfvars` to reflect what you need.

- `aws_region`: Which region do you want the instances in?
- `aws_instance_count`: How many instances?
- `slug`: Workshop name slug that will be used to tag aws resources (keep this short as this forms part of the instance hostname e.g. `acme`)
- `splunk_access_token`: Observability Access Token
- `splunk_rum_token`: Observability RUM Token
- `splunk_realm`: Observability Realm
- `splunk_presetup`: Provide a preconfigured instance (OTel Collector and Online Boutique deployed with RUM enabled)
- `splunk_jdk`: Install OpenJDK and Maven on the instance

## 6. Create a Terraform plan

Run `terraform plan` to see what will be created. Once happy run `terraform apply` to create the instances.

## 7. Example command line

```bash
terraform apply \
-auto-approve \
-input=false
```

Or you use the provided script `up` to request instances:

Install the prerequisites, e.g. on Mac: `brew install terraform jq pssh`

Then use the script:

```bash
./up myproject 12 eu-central-1
```

This will create a terraform workspace `o11y-for-myproject`, request 12 instances and ensure all instances have completed provisioning.
