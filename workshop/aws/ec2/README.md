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

### Required variables

- `aws_region`: Which region do you want the instances in?
- `aws_instance_count`: How many instances?
- `slug`: Short name/tag, e.g. acme. Used to derive project and hostnames, AWS tags and terraform workspace e.g. `emea-ws`)

### Optional variables

- `splunk_access_token`: Observability Access Token
- `splunk_rum_token`: Observability RUM Token
- `splunk_realm`: Observability Realm
- `subnet_count`: How many subnets to create. The default is 2.

### Instance type variables

- `splunk_presetup`: Provide a preconfigured instance (OTel Collector and Online Boutique deployed with RUM enabled). The default is FALSE.
- `splunk_jdk`: Install OpenJDK and Maven on the instance. The default is FALSE.
- `otel_demo` : Install and configure the OpenTelemetry Astronomy Shop Demo. This requires that `splunk_presetup` is set to FALSE. The default is FALSE

## 6. Create a Terraform plan

Run `terraform plan` to see what will be created. Once happy run `terraform apply` to create the instances.

## 7. Example command line

```bash
terraform apply \
-auto-approve \
-input=false
```

Once the apply is complete, the output will contain the public IP addresses, instance names and the _(automatically generated)_ instance password.

### Example output from Terraform

``` text
Apply complete! Resources: 10 added, 0 changed, 0 destroyed.

Outputs:

login_details = tolist([
  "workshop-01, 10.1.1.1, mKV50oR36MgASJd3",
  "workshop-02, 10.1.1.2, mKV50oR36MgASJd3",
  "workshop-03, 10.1.1.3, mKV50oR36MgASJd3",
])
```

<!--
Or you use the provided script `up` to request instances:

Install the prerequisites, e.g. on Mac: `brew install terraform jq pssh`

Then use the script:

```bash
./up myproject 12 eu-central-1
```

This will create a terraform workspace `o11y-for-myproject`, request 12 instances and ensure all instances have completed provisioning.
-->
