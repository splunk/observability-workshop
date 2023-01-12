# Prerequisites to perform this lab

- Terraform installed
- AWS Account  
- AWS access keys aws_access_key_id aws_secret_access_key
- SSH Key (the Private SSH Key file one you use for AWS Instances follow
[create a key pair for AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html) if you don't have one already)

An observability cloud suite organisation ID.

Either use the observability cloud suite environmment from the IM/APM workshop
Or you use/create an observability cloud suite environment to run the ITSI workshop to run it on its own.

Data need to be ingested in the observability cloud for this workshop:

- Follow the steps to deploy the online boutique on a aws instance:

[here](https://github.com/splunk/observability-workshop/tree/main/workshop/aws/ec2)

- Follow the steps to connect the AWS instance to the observability suite [here](https://splunk.github.io/observability-workshop/latest/)

Open observability-workshop/workshop/itsi in your preferred code editor.

```bash
cp terraform.tfvars.example terraform.tfvars
```

Lab

## 1 Modify terraform.tfvars file

In section Enable / Disable Modules  

```ini
## Enable / Disable Modules ##
itsi_o11y_cp_enabled = true

In section Auth Settings:

```ini
## Auth Settings ##
key_name                = "<NAME>" #enter key name without the extension
private_key_path        = "~/.ssh/id_rsa" #enter key path with the key name with the extension
instance_type           = "t2.micro"
aws_access_key_id       = "<ACCCESS_KEY_ID>>"
aws_secret_access_key   = "<SECRET_ACCESS_KEY>>"
```

In section Splunk IM/APM Variables

```ini
### Splunk IM/APM Variables ###
access_token             = "<ACCESS_TOKEN>"
api_url                  = "https://api.<REALM>.signalfx.com"
realm                    = "<REALM>"
environment              = "<ENVIRONMENT>" #prefix for your AWS objects
```

## 2 review the variable for ITSI

## Splunk ITSI Variables

The Splunk ITSI Module requires various splunk apps files that cannot be included in this repo and are downloaded as part of the script.

The versions of ITSI and other apps are defined in the variables don't change it.

current versions are :

itsi version = 4.9.3
splunk enterprise version = splunk-8.2.3
splunk app for content packs = 1.4.0
splunk synthetic monitoring add on  = 1.0.7
splunk infrastructure monitoring add on   = 1.2.1

### Deploy the instance

Navigate on your terminal `observability-workshop/workshop/itsi` the itsi folder.
You should expect the environment to take between 5 and 10 minute to spin up.

run

```bash
terraform init
```

run

```bash
terraform plan
```

```text
var.region
  Select region (1:eu-west-1, 2:eu-west-3, 3:eu-central-1, 4:us-east-1, 5:us-east-2, 6:us-west-1, 7:us-west-2, 8:ap-southeast-1, 9:ap-southeast-2, 10:sa-east-1 )

  Enter a value:
```

enter 1 for the region

At the bottom of your editor you should get the output

```text
Plan: 10 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + Splunk_ITSI_Password = [
      + (known after apply),
    ]
  + Splunk_ITSI_Server   = [
      + [
          + (known after apply),
        ],
    ]
  + Splunk_ITSI_URL      = [
      + [
          + (known after apply),
        ],
    ]
```

Note If you get an error review the previous steps.

run

```bash
terraform apply
```

```text
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value:
```

Enter yes

Note if you get an error run terraform destroy and restart the installation.

You should get the output below:

```text
Apply complete! Resources: 1 added, 0 changed, 1 destroyed.

Outputs:

Splunk_ITSI_Password = [
  "xxx.xxx.xxx.xxx",
]
Splunk_ITSI_Server = [
  tolist([
    "ipapa_splunk-itsi, xxx.xxx.xxx.xxx",
  ]),
]
Splunk_ITSI_URL = [
  tolist([
    "http://xxx.xxx.xxx.xxx:8000",
  ]),
]
```

Login to your newly created splunk instance using:
the address -> Splunk_ITSI_URL
username -> admin
password -> Splunk_ITSI_Password

## destroy all of your good work

```text
Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value:
```

Enter yes

health check of the environment

you should be seeing this view once you log into your ITSI instance:

![Login](/content/en/itsi/images/itsi_login_view.png)
