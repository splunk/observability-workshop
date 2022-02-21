# Workshop Setup

This setup module is used to prepare a set of AWS Lambda Functions and EC2 Instances to be used for the workshop, these will need to be created by an AWS Admin who has access to a suitable account that can be used for the workshop.

There will be 4 Lambda Functions and 1 EC2 instance deployed for each participant.  Every resource will be prefixed with a Unique ID (UID) to identify which attendee they belong to.

Terraform is used to deploy all of the resources and this module details the steps required to install and configure terraform, configure it to authenticate with AWS, and then deploy the resources.

---

## 1. Install Terraform

Terraform is used to deploy all of the AWS infrastructure for the workshop, so needs to be installed on your machine. Instructions on how to install Terraform can be found [here](https://learn.hashicorp.com/tutorials/terraform/install-cli){: target=_blank}.

### Terraform AWS Authentication

Once Terraform is installed, you need to configure it to authenticate with your AWS Account.  Details on AWS Authentication can be found [here](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication){: target=_blank}.

The AWS Authentication consists of two files, `config` and `credentials` which are typically located in the `~/.ssh` folder.

The `config` file details different profiles, and  works in conjunction with the `credentials` file which contains your `access` and `secret` keys.

=== "config"

    ```
    [default]
    region = us-east-1
    output = json
    [profile splunk]
    region = us-east-1
    output = json
    ```

=== "authentication"
    ```

    [default]
    aws_access_key_id = {your access key}
    aws_secret_access_key = {your secret key}
    [splunk]
    aws_access_key_id = {your access key}
    aws_secret_access_key = {your secret key}

    ```

---

## 2. Clone Workshop Content - WILL NEED TO UPDATE URL ONCE PUBLISHED TO SPLUNK REPO

The Workshop Content needs to be pulled down from Github to your local machine, then updated with your specific settings for AWS Authentication.

### 2.1 Download the Workshop Repo

Git Clone

=== "git clone"
    ```

    git clone https://github.com/geoffhigginbottom/tflambdatestv2.git

    ```

=== "example result"
    ```

    Workshop git clone https://github.com/geoffhigginbottom/tflambdatestv2.git
    cloning into 'tflambdatestv2'...
    remote: Enumerating objects: 276, done.
    remote: Counting objects: 100% (276/276), done.
    remote: Compressing objects: 100% (186/186), done.
    remote: Total 276 (delta 159), reused 206 (delta 89), pack-reused 0
    Receiving objects: 100% (276/276), 269.48 KiB | 1.13 MiB/s, done.
    Resolving deltas: 100% (159/159), done.

    ```

---

### 2.2 Create terraform.tfvars

A file called terraform.tfvars needs to be created and populated with your specific settings.  This file contains all of the settings required to enable Terraform to connect to both your AWS and Splunk Environments.

An example version of the file is included in the repo named `terraform.tfvars.example`, which you should copy and rename to `terraform.tfvars`. Run the following command from within the directory where the workshop content was download.

=== "crete terraform.tfvars"
    ```

    cp terraform.tfvars.example terraform.tfvars

    ```

Then update the newly created `terraform.tfvars`starting with the AWS Variables Section.

#### 2.2.1 AWS Variables Section

* `profile` should match the profile name used in your aws `authentication` file which Terraform will use to authenticate with AWS

* `key_name` is the name of the ssh_key you wish to use to access the EC2 instances (note password login is also enabled on the Instances)

* `private_key_path` is the path to your private ssh key, such as `~/.ssh/xxx.pem` or `~/.ssh/id_rsa`

* `instance_type` is the AWS Instance Type used for the EC2 Instances - this defaults to the free tier "t2.micro"

* `region` is an optional parameter, normally left commented out.  It enables you to override the region prompt during the Terraform deployment

=== "terraform.tfvars - AWS Variables"
    ```
    ### AWS Variables ###
    profile = "xxx"
    key_name = "yyy"
    private_key_path = "~/.ssh/xxx.pem or ~/.ssh/id_rsa etc"
    instance_type = "t2.micro"

    ## Terraform will prompt you to select an AWS Region to deploy the resources into
    ## Setting a region here removes the region prompt (default is to have it prompt you)
    ## List of supported regions can be found in the variables.tf file
    #region = "2"
    ```

#### 2.2.2 Splunk Variables Section

* `function_version` is an optional parameter, normally left commented out. It enables you to override the version prompt during the Terraform deployment

* `access_token` is the token you wish to use to authenticate with the Splunk Monitoring backend

* `realm` specifies which Realm your Splunk Monitoring backend is deployed in

* `collector_image` specifies the contributor version of the otel collector, and the latest version can be found [here](https://github.com/open-telemetry/opentelemetry-collector-contrib/releases){: target=_blank} and will need updating as new versions are released

=== "terraform.tfvars - Splunk Variables"
    ```
    ### Splunk Variables ###

    ## Terraform will prompt you to select a version to be deployed,
    ## "a" = apm version, "b" = base version.
    ## Base version is typically deployed, but the apm version can be deployed 
    ## for testing and comparison purposes
    #function_version = "b"

    access_token = "xxxxxxxxxx"
    realm = "xxx"

    # smart_agent_version = "5.6.0-1" # Optional - If left blank, latest will be installed
    smart_agent_version = "" # Optional - If left blank, latest will be installed

    ## Latest otel collector releases can be found at 
    ## https://github.com/open-telemetry/opentelemetry-collector-contrib/releases
    collector_image = "otel/opentelemetry-collector-contrib:0.15.0"
    ```

---

### 2.3 Generate the Unique IDs

A file named `quantity.auto.tfvars` needs to be created and populated with your specific settings.  This file contains the Unique IDs which will be appended to each AWS Resource to identify which workshop participant they are allocated to.

There is an example file in the repo called `quantity.auto.tfvars.example` which needs to be copied and renamed to `quantity.auto.tfvars`.  Run the following command from within the directory where the workshop content was download.

=== "crete quantity.auto.tfvars"
    ```

    cp quantity.auto.tfvars.example quantity.auto.tfvars

    ```

Edit `quantity.auto.tfvars` and populate the list of participants, ensuring each value is unique and has no spaces.  Ensure the `function_count` value equals the total number of names, and that each entry ends with a comma, apart from the last one, as per the example below.

=== "quantity.auto.tfvars"
    ```

    function_count = "3"
    function_ids = [
        "John",
        "Sarah",
        "Amir"
        ]
        
    ```

---

## 3. Initialize Terraform

Once you have finished creating and updating `xxx` and `yyy` you now need to initialize terraform, so run the following command:

=== "Terraform init"

    ```
    teraform init
    ```

=== "Example output"
    ```
    Initializing the backend...

    Initializing provider plugins...
    - Finding latest version of terraform-providers/docker...
    - Finding latest version of hashicorp/null...
    - Finding latest version of hashicorp/archive...
    - Finding latest version of hashicorp/aws...
    - Installing hashicorp/archive v2.0.0...
    - Installed hashicorp/archive v2.0.0 (signed by HashiCorp)
    - Installing hashicorp/aws v3.18.0...
    - Installed hashicorp/aws v3.18.0 (signed by HashiCorp)
    - Installing terraform-providers/docker v2.7.2...
    - Installed terraform-providers/docker v2.7.2 (signed by HashiCorp)
    - Installing hashicorp/null v3.0.0...
    - Installed hashicorp/null v3.0.0 (signed by HashiCorp)

    The following providers do not have any version constraints in configuration,
    so the latest version was installed.

    To prevent automatic upgrades to new major versions that may contain breaking
    changes, we recommend adding version constraints in a required_providers block
    in your configuration, with the constraint strings suggested below.

    * hashicorp/archive: version = "~> 2.0.0"
    * hashicorp/aws: version = "~> 3.18.0"
    * hashicorp/null: version = "~> 3.0.0"
    * terraform-providers/docker: version = "~> 2.7.2"


    Warning: Additional provider information from registry

    The remote registry returned warnings for
    registry.terraform.io/terraform-providers/docker:
    - For users on Terraform 0.13 or greater, this provider has moved to
    kreuzwerker/docker. Please update your source in required_providers.

    Terraform has been successfully initialized!

    You may now begin working with Terraform. Try running "terraform plan" to see
    any changes that are required for your infrastructure. All Terraform commands
    should now work.

    If you ever set or change modules or backend configuration for Terraform,
    rerun this command to reinitialize your working directory. If you forget, other
    commands will detect it and remind you to do so if necessary.
    ```

## 4. Deploy the Workshop

### 4.1 Terraform Plan

You can now deploy the workshop using Terraform.  It is always best practice to run a `plan` so you can check what changes Terraform is going to make.  When executing Terraform will prompt you to select a version of the workshop (select `b` for base), and also an AWS Region (choose an appropriate one from the list)

=== "Terraform plan"
    ```
    terraform plan

    var.function_version
        Select Function Version (a:apm, b:base)

        Enter a value: b

    var.region
        Select region (1:eu-west-1, 2:eu-west-3, 3:eu-central-1, 4:us-east-1, 5:us-east-2, 6:us-west-1, 7:us-west-2, 8:ap-southeast-1, 9:ap-southeast-2, 10:sa-east-1 )

        Enter a value: 2
    
    ```

=== "Example output"
    ```
    terraform plan

    var.function_version
        Select Function Version (a:apm, b:base)

        Enter a value: b

    var.region
        Select region (1:eu-west-1, 2:eu-west-3, 3:eu-central-1, 4:us-east-1, 5:us-east-2, 6:us-west-1, 7:us-west-2, 8:ap-southeast-1, 9:ap-southeast-2, 10:sa-east-1 )

        Enter a value: 2

    Refreshing Terraform state in-memory prior to plan...
    The refreshed state will be used to calculate this plan, but will not be
    persisted to local or remote state storage.

    data.aws_ami.latest-ubuntu: Refreshing state...

    ------------------------------------------------------------------------

    An execution plan has been generated and is shown below.
    Resource actions are indicated with the following symbols:
    + create
    <= read (data resources)

    Terraform will perform the following actions:

    # data.archive_file.retailorder_lambda_zip will be read during apply
    # (config refers to values not yet known)
    <= data "archive_file" "retailorder_lambda_zip"  {
        + id                  = (known after apply)
        + output_base64sha256 = (known after apply)
        + output_md5          = (known after apply)
        + output_path         = "retailorder_lambda.zip"
        + output_sha          = (known after apply)
        + output_size         = (known after apply)
        + source_file         = "retailorder_lambda_function.py"
        + type                = "zip"
        }

    ........
    EXTRA LINES REMOVED 
    ........
    
    Plan: 106 to add, 0 to change, 0 to destroy.

    ------------------------------------------------------------------------

    Note: You didn't specify an "-out" parameter to save this plan, so Terraform
    can't guarantee that exactly these actions will be performed if
    "terraform apply" is subsequently run.
    ```

### 4.3 Terraform Apply

After checking the plan output looks OK, you can now `apply` the deployment, using the same options as when you ran the `plan`, and entering `yes` when prompted:

=== "Terraform apply"
    ```
    terraform apply

    var.function_version
        Select Function Version (a:apm, b:base)

        Enter a value: b

    var.region
        Select region (1:eu-west-1, 2:eu-west-3, 3:eu-central-1, 4:us-east-1, 5:us-east-2, 6:us-west-1, 7:us-west-2, 8:ap-southeast-1, 9:ap-southeast-2, 10:sa-east-1 )

        Enter a value: 2
    
    Plan: 106 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
        Terraform will perform the actions described above.
        Only 'yes' will be accepted to approve.

        Enter a value: yes
    ```

=== "Example output"
    ```
    Apply complete! Resources: 106 added, 0 changed, 0 destroyed.

    Outputs:

    OTC_Instances = [
    "john_otc, 52.47.138.166",
    "sarah_otc, 15.188.51.119",
    "amir_otc, 35.180.230.215",
    ]
    retaildiscount_invoke_url = [
    "John_RetailOrderDiscount_api_gateway, o91dr4o3c6.execute-api.eu-west-3.amazonaws.com",
    "Sarah_RetailOrderDiscount_api_gateway, leelg1e0y9.execute-api.eu-west-3.amazonaws.com",
    "Amir_RetailOrderDiscount_api_gateway, 0gdlkj8ceb.execute-api.eu-west-3.amazonaws.com",
    ]
    retailorder_arns = [
    "John_RetailOrder, arn:aws:lambda:eu-west-3:527477237977:function:John_RetailOrder",
    "Sarah_RetailOrder, arn:aws:lambda:eu-west-3:527477237977:function:Sarah_RetailOrder",
    "Amir_RetailOrder, arn:aws:lambda:eu-west-3:527477237977:function:Amir_RetailOrder",
    ]
    retailorder_invoke_url = [
    "John_RetailOrder_api_gateway, https://286kkhj9k1.execute-api.eu-west-3.amazonaws.com/default",
    "Sarah_RetailOrder_api_gateway, https://rgv6lwdf81.execute-api.eu-west-3.amazonaws.com/default",
    "Amir_RetailOrder_api_gateway, https://5lnuuesqz3.execute-api.eu-west-3.amazonaws.com/default",
    ]
    retailorderdiscount_arns = [
    "John_RetailOrderDiscount, arn:aws:lambda:eu-west-3:527477237977:function:John_RetailOrderDiscount",
    "Sarah_RetailOrderDiscount, arn:aws:lambda:eu-west-3:527477237977:function:Sarah_RetailOrderDiscount",
    "Amir_RetailOrderDiscount, arn:aws:lambda:eu-west-3:527477237977:function:Amir_RetailOrderDiscount",
    ]
    retailorderdiscount_path = [
    "John_RetailOrderDiscount, /default/John_RetailOrderDiscount",
    "Sarah_RetailOrderDiscount, /default/Sarah_RetailOrderDiscount",
    "Amir_RetailOrderDiscount, /default/Amir_RetailOrderDiscount",
    ]
    retailorderline_arns = [
    "John_RetailOrderLine, arn:aws:lambda:eu-west-3:527477237977:function:John_RetailOrderLine",
    "Sarah_RetailOrderLine, arn:aws:lambda:eu-west-3:527477237977:function:Sarah_RetailOrderLine",
    "Amir_RetailOrderLine, arn:aws:lambda:eu-west-3:527477237977:function:Amir_RetailOrderLine",
    ]
    retailorderprice_arns = [
    "John_RetailOrderPrice, arn:aws:lambda:eu-west-3:527477237977:function:John_RetailOrderPrice",
    "Sarah_RetailOrderPrice, arn:aws:lambda:eu-west-3:527477237977:function:Sarah_RetailOrderPrice",
    "Amir_RetailOrderPrice, arn:aws:lambda:eu-west-3:527477237977:function:Amir_RetailOrderPrice",
    ]
    retailorderprice_invoke_url = [
    "John_RetailOrderPrice_api_gateway, https://gohem8pwib.execute-api.eu-west-3.amazonaws.com/default",
    "Sarah_RetailOrderPrice_api_gateway, https://dv23py0xo0.execute-api.eu-west-3.amazonaws.com/default",
    "Amir_RetailOrderPrice_api_gateway, https://dv1rn91g83.execute-api.eu-west-3.amazonaws.com/default",
    ]
    ```

## 4.3 What Did We Deploy?

Assuming a successful deployment, if you check in your AWS Console you should find the following (with multiple versions where UID matches the user names from `quantity.auto.tfvars`):

* Lambda Functions
  * UID_RetailOrder
  * UID_RetailOrderDiscount
  * UID_RetailOrderLine
  * UID_RetailOrderPrice

* Lambda Layers
  * request-opentracing_2_0

* Instances
  * UID_otc

* API Gateways
  * UID_RetailOrder_api_gateway
  * UID_RetailOrderDiscount_api_gateway
  * UID_RetailOrderPrice_api_gateway

* IAM Roles
  * splunk_lambda_role_xxxxxxxxxx

* IAM Policies
  * lambda_initiate_lambda_policy_xxxxxxxxxxx
