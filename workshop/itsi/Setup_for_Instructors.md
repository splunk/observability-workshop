Prerequisites:

to perform this lab you need :

Terraform installed 

AWS credentials (AWS console ?) AWS Account aws_access_key_id | aws_secret_access_key
SSH Key 

An observability cloud organisation ID. 

Have data ingested in the environmment for this workshop:
we have deploy the online boutique of the observability workshop on a aws instance available here https://signalfx.github.io/observability-workshop/v3.13/
we have connected our AWS instance to the observability suite

Open sfx-tf-demo in your preferred code editor.

```
cp terraform.tfvars.example terraform.tfvars
```

Lab 
## 1 Modify terraform.tfvars file ##
In section Enable / Disable Modules
```
## Enable / Disable Modules ##
itsi_o11y_cp_enabled        = true
```
In section Auth Settings
```
## Auth Settings ##
key_name                = "<NAME>"
private_key_path        = "~/.ssh/id_rsa"
instance_type           = "t2.micro"
aws_access_key_id       = "<ACCCESS_KEY_ID>>"
aws_secret_access_key   = "<SECRET_ACCESS_KEY>>"
```
In section Splunk IM/APM Variables
```
### Splunk IM/APM Variables ###
access_token             = "<ACCESS_TOKEN>"
api_url                  = "https://api.<REALM>.signalfx.com"
realm                    = "<REALM>"
environment              = "<ENVIRONMENT>"
```

## 2 review the variable for ITSI ##


### Splunk ITSI Variables

The Splunk ITSI Module requires various files that cannot be included in this repo and need to be downloaded from https://splunkbase.splunk.com/ then their locations specified in this section


### Download the files via the link provided by the instructor and install it locally 

on MAC in ~Downloads 
on Windows in ...

### Deploy the instance

go into sfx-tf-demo

run

```terraform init```

run

```terraform plan``` 

```
var.region
  Select region (1:eu-west-1, 2:eu-west-3, 3:eu-central-1, 4:us-east-1, 5:us-east-2, 6:us-west-1, 7:us-west-2, 8:ap-southeast-1, 9:ap-southeast-2, 10:sa-east-1 )

  Enter a value:
```

enter 1 for the region

At the bottom of your editor you should get the output
```
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

```terraform apply```

```
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value:
```
Enter yes

Note if you get an error run terraform destroy and restart the installation.

You should get the output below:
```
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

### destroy all of your good work 

```
Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value:
```

Enter yes





