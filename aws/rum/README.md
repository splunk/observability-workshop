# Instructions on how to set up RUM cloud instances

The RUM Module utilizes Terraform remote-exec which needs to access the instances via SSH to execute the commands. Therefore you need to have an AWS SSH Key setup in the AWS Zone you will be deploying your instances into.

There are a number of terraform variables that are used that can either be configured in a terraform.tfvars file, or supplied each run time as environment variables.

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

NOTE 1: If you have AWS config and credentials files configured on your laptop and do not set the above Env Vars, your 'default' profile will be used, so ensure it is pointing at the correct AWS Account such as you Splunk Account.

NOTE 2: If you wish to run this RUM workshop next to the original Workshop to give a full stack workshop, please make sure you install this to a **different** AWS realm to make sure they do not conflict!

## Step 3 - Configure Terraform Variables

There are two options for this step, `Option 1 - Using env_vars` OR `Option 2 - using terraform.tfvars`

### Option 1 - Using env_vars

Create the Terraform Specific environment variables which are required to setup the RUM workshop.

- access_token: The Access Token from the Org being used for the workshop
- rum_token: The RUM Token from the Org being used for the workshop
- realm: The Realm for the Org being used for the workshop
- key_name: The name of your AWS SSH Key in the AZ you intend to deploy your instances into
- private_key_path: Path to the location of your private key linked to the AWS SSH Key, e.g."~/.ssh/id_rsa"
- aws_region: The AWS Region you want to deploy your instances into

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

Contents of terraform.tfvars which should be located in this 'rum' folder (this will not get pushed back to github as it is excluded via git.ignore)

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
cd observability-workshop/aws/rum/
terraform init -upgrade
terraform apply
```

If you have correctly setup your AWS Access Variables (step2) or Terraform Variables or terraform.tfvar file (step 3), you should not be asked any questions at run time.

## Step 5 - Successful Deployment

Terraform will now do its magic and deploy the rum instances.  The output from terraform will display a summary of the instances, their Host Names, IP Addresses, and the random passwords allocated to the RUM instances.

TIP: For mac users, the Online_Boutique_URL is clickable if you hold down `<cmd>` whilst clicking, this will take you straight to the Online Boutique running on the RUM Master, but please allow a couple of minutes for it to fully deploy.

There will be a single `RUM Master`, a `No RUM` version and typically 3 Rum Workers (value set in variables.tf).  The `No Rum` version is simply there to enable you to show workshop attendees the differences in the headers that have enabled RUM.

The RUM Workers will automatically start to generate load against the RUM Master and populate the system with both APM and RUM data.

Below is an example of the output with the 5 Instances and 2 URLs.  The first value in the 'no_rum_details' and 'rum_master_details' output, in this example `epwh` & `nxuf` are their unique identifiers, created in case there are multiple workshops running at the same time, it will appear as the prefix to the Environment and Cluster Names in the Splunk UI. e.g. `nxuf-rum-master`

```bash
no_rum_details = tolist([
  "epwh, no-rum, 54.217.144.37, YGyhOvukBlaU",
])
no_rum_online_boutique_details = tolist([
  "http://54.217.144.37:81",
])
rum_online_boutique_details = tolist([
  "http://18.203.127.114:81",
])
rum_master_details = tolist([
  "nxuf, rum-master, 18.203.127.114, bHTyPhTHvJ7V",
])
rum_worker_details = tolist([
  "rum-worker-1, 34.245.39.225, NyfIewLpFfR4",
  "rum-worker-2, 3.249.38.51, vakkn1erLgUz",
  "rum-worker-3, 34.245.208.75, ehjI7PqqRLeT",
])
```
