# `New` Instructions on how to set up EC2 cloud instances for participants

The new RUM Module utilizes Terraform remote-exec which needs to access the instances via SSH to execute the commands. Therefore you need to have an AWS SSH Key setup in the AWS Zone you will be deploying your instances into.

There are a number of additional terraform variables that are used that can either be configured in a terraform.tfvars file, or setup each time as environment variables.

## Step 1 - Clone the Repo

```bash
# clone the repo
$ git clone https://github.com/signalfx/observability-workshop.git
```

## Step 2 - Configure AWS Access

You will need access to an AWS account to obtain both `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

Create environment variables for your AWS access keys.

```bash
export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
echo $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY
```

NOTE: If you have AWS config and credentials files configured on your laptop and do not set the above Env Vars, your 'default' profile will be used, so ensure it is pointing at the correct AWS Account such as you Splunk Account.

## Step 3 - Configure Terraform Variables

There are two options for this step, `Option 1 - Using env_vars` OR `Option 2 - using terraform.tfvars`

### Option 1 - Using env_vars

Create the Terraform Specific environment variables which are now required to setup the workshop.

- access_token: The Access Token from the Org being used for the workshop
- rum_token: The RUM Token from the Org being used for the workshop
- realm: The Realm for the Org being used for the workshop
- key_name: The name of your AWS SSH Key in the AZ you intend to deploy your instances into
- private_key_path: Path to the location of your private key linked to the AWS SSH Key, e.g."~/.ssh/id_rsa"
- aws_region: (Optional) The AWS Region you want to deploy your instances into

```bash
export TF_VAR_access_token="YOUR_ACCESS_TOKEN"
export TF_VAR_rum_token="YOUR_RUM_TOKEN"
export TF_VAR_realm="YOUR_REALM"
export TF_VAR_key_name="YOUR_SSH_KEY_NAME"
export TF_VAR_private_key_path="YOUR_SSH_KEY_PATH"
export TF_VAR_aws_region="YOUR_AWS_REGION"
```

Test the values

```bash
echo $TF_VAR_access_token 
echo $TF_VAR_rum_token 
echo $TF_VAR_realm 
echo $TF_VAR_key_name 
echo $TF_VAR_private_key_path 
echo $TF_VAR_aws_region
```

### Option 2 - Using a terraform.tfvars file

An alternative is to create a terraform.tfvars file which can store these values and make them easily reusable, but please be aware that we often cycle the `ACCESS_TOKEN` and `RUM_TOKEN` after each workshop, so check each time you create a new one.

Contents of terraform.tfvars which should be located in this ec2 folder (this will not get pushed back to github as it is excluded via git.ignore)

```bash
### SFx Variables ###
access_token = "YOUR_ACCESS_TOKEN"
rum_token= "YOUR_RUM_TOKEN"
realm = "YOUR_REALM"

### AWS Variables ###
key_name = "YOUR_SSH_KEY_NAME"
private_key_path = "YOUR_SSH_KEY_PATH"
aws_region = "YOUR_AWS_REGION"
```

### Option 3 - Enter details at run time

If you do not setup the Terraform Environment Variables or create a terraform.tfvars, or miss any of the settings out, then when you run `terraform apply` you will be prompted for each missing value.

## Step 4 - Deploying the Instances

```bash
cd observability-workshop/aws/ec2/
terraform init -upgrade
terraform apply
```

Assuming you have setup your AWS Access Variables (step2), Terraform Variables or terraform.tfvar file (step 3), you will be asked two questions at run time.

- Instance Count is the number of workshop instances you want to deploy (enter 0 for none)
- Deploy Rum Instances? enables you to optionally deploy the RUM instances, enter 0 for No, or 1 for Yes

### Possible Scenarios

If you only want to deploy Instances for the workshop and `no` RUM Instances enter the desired value e.g. `20` for the first question `Instance Count`, then for `Deploy Rum Instances` enter `0` for No.

If you want to deploy Instances for the workshop `and` RUM enter the desired value e.g. `20` for the first question `Instance Count`, then for `Deploy Rum Instances` enter `1` for Yes.

If you only want to only deploy RUM Instances enter `0` for the first question `Instance Count`, then for `Deploy Rum Instances` enter `1` for Yes.

```bash
var.aws_instance_count
  Instance Count

  Enter a value: 20

var.rum_instances_enabled
  Deploy RUM Instances? 0=No, 1=Yes

  Enter a value: 1
```

## Step 5 - Successful Deployment

Terraform will now do its magic and deploy the desired instances.  The output from terraform will display a summary of the instances, their Host Names, IP Addresses, and the random passwords allocated to the RUM instances.

TIP: For mac users, the Online_Boutique_URL is clickable if you hold down `<cmd>` whilst clicking, this will take you straight to the Online Boutique running on the RUM Master, but please allow a couple of minutes for it to fully deploy.

If you have chosen to deploy the RUM instances there will be a single RUM Master and typically 3 Rum Workers (value set in variables within the RUM Module).

The RUM Workers will automatically start to generate load against the RUM Master and populate the system with both APM and RUM data.

Below is an example of the output with RUM enabled, and 5 Workshop Instances.  The first value in the RUM_Master output, in this case `zhsu` is the unique identifier, created in case there are multiple workshops running at the same time, it will appear as the prefix to the Environment and Cluster Names in the Splunk UI. e.g. `zhsu-rum-master`

```bash
Online_Boutique_URL = [
  tolist([
    "http://35.180.69.148:81",
  ]),
]
RUM_Master = [
  tolist([
    "zhsu, rum-master, 35.180.69.148, aX9cqacveqQn",
  ]),
]
RUM_Workers = [
  tolist([
    "rum-worker-1, 35.180.40.207, 2GiSW9JsKQo0",
    "rum-worker-2, 15.236.60.107, wxzg5iy0KxCr",
    "rum-worker-3, 15.237.81.170, QIsLGPl2KAGU",
  ]),
]
ip = [
  "35.180.190.108",
  "35.180.156.232",
  "35.180.152.238",
  "13.36.39.142",
  "52.47.138.238",
]
```

<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />

# OLD Instructions on how to set up EC2 cloud instances for participants

You will need access to an AWS account to obtain both **AWS_ACCESS_KEY_ID** and **AWS_SECRET_ACCESS_KEY**.

Initialize Terraform

```
terraform init -upgrade
```
Create environment variables for **AWS_ACCESS_KEY_ID** and **AWS_SECRET_ACCESS_KEY**

```
export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
```

Validate the environment variables are set

```
echo $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY
```

Set the following variables:

- `aws_region`: Which region do you want the instances in?
- `aws_instance_type`: What kind of instance?
- `aws_instance_count`: How many instances?

Sample command:

```
terraform apply \
-auto-approve \
-var="aws_region=eu-central-1" \
-var="aws_instance_type=t2.xlarge" \
-var="aws_instance_count=1"
```

