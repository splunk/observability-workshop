# Provisioning EC2 instances for a workshop

**NOTE:** Due to new security restrictions the SSH port is now 2222.

Go to [https://swipe.splunk.show](https://swipe.splunk.show) and provision your workshop environment.

You will need:

- User API Session Token (available from your profile page)
- Realm
- A CSV containing the email addresses of your attendees

Follow the guidance provided by SWIPE and after provisioning is completed, you will be provided with:

- **INGEST Token**
- **API Token**
- **RUM Token**
- **HEC URL**
- **HEC Token**

These will be used to populate the `terraform.tfvars` file in **Step 5** below.

## Instructions on how to set up EC2 cloud instances for participants

**NOTE:** The preferred way of provisioning EC2 instances is directly via [Splunk Show](https://show.splunk.com).

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

## 4. Create a Terraform variables file

Variables are kept in file `terrform.tfvars` and we provide a template as `terraform.tfvars.template` to copy and edit:

```bash
cp terraform.tfvars.template terraform.tfvars
```

The file `terraform.tfvars` is ignored by git and should not be committed to the repo.

## 5. Set Terraform variables

The following variables are available. Edit `terraform.tfvars` to reflect what you need.

### Required Variables

- `aws_region`: Which region do you want the instances in?
- `aws_instance_count`: How many instances?
- `slug`: Short name/tag, e.g. acme. Used to derive project and hostnames, AWS tags and terraform workspace e.g. `emea-ws`)
- `splunk_access_token`: Observability Access Token
- `splunk_api_token`: Observability API Token
- `splunk_realm`: Observability Realm
- `splunk_rum_token`: Observability RUM Token
- `splunk_hec_url`: Splunk HEC URL
- `splunk_hec_token`: Splunk HEC Token

### Optional variables

- `subnet_count`: How many subnets to create. The default is 2.
- `user_data_tpl`: name of the cloud-init template for the instances, read from `templates/` folder. The default is `userdata.yaml`.
- `pub_key`: SSH public key to provision on the instances

### Instance type variables

- `splunk_presetup`: Provide a preconfigured instance (OTel Collector and Online Boutique deployed with RUM enabled). The default is `false`.
- `splunk_diab`: Install Demo-in-a-Box on the instance. The default is `false`.
- `otel_demo` : Install and configure the OpenTelemetry Astronomy Shop Demo. This requires that `splunk_presetup` is set to `false`. The default is `false`

## 6. Create a Terraform plan

Run `terraform plan` to see what will be created. Once happy run `terraform apply` to create the instances.

## 7. Example command line

```bash
terraform apply \
-auto-approve \
-input=false
```

Once the `apply` is complete, the output will contain the public IP addresses, instance names and the _(automatically generated)_ instance password.

### Example output from Terraform

``` text
Apply complete! Resources: 10 added, 0 changed, 0 destroyed.

Outputs:

login_details = tolist([
  "workshop, ssh -p 2222 splunk@192.168.2.1, u$CTKigp@Bkt337p",
])
```

### Accessing instances as instructor via ssh

The `var.pub_key` (if provided) is added to the default user `ubuntu` on the ec2 instances. In addition, ssh configuration and a keypair to access instances are generated as `ssh-<slug>.conf` and `ssh-<slug>.key`.

To access an instance for a workshop with slug `acme`, use:

```bash
ssh -F ssh-acme.conf -p 2222 acme-01
```
