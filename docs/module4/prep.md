# SignalFx Smart Agent - Lab Summary

* Download the workshop
* Start a Multipass or AWS EC2 instance
* Deploy the SignalFx Smart Agent in K3s
* Validate K3s cluster is visible in Kubernetes Navigator
* Deploy a NGINX ReplicaSet in K3s
* Validate NGNIX metrics are flowing

{==

Minimum recommended time to complete - **20 minutes**

==}

!!! note
    If you have been give access to a pre-provisioned EC2 instance, you can ignore the rest of this preparation lab and go straight to the next lab [Deploying the Smart Agent in Kubernetes (K3s)](../../module4/k3s).

---

## 1. Let’s bake some K8s

If you are going to run this locally please install [Multipass](https://multipass.run/) for your OS. Make sure you are using at least version `1.2.0`. On a Mac you can also install via [Homebrew](https://brew.sh/) e.g. `brew cask install multipass`

If you have chosen to run the workshop on an EC2 instance and its not yet provisioned for you,  please install [Terraform](https://www.terraform.io/downloads.html) for your OS. Please make sure it is version 0.12.12 or above.
On a Mac you can also install via [Homebrew](https://brew.sh/) e.g. `brew install terraform`

!!! note AWS Account detail
    You also need access to an AWS account and have an AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.

Regardless if you are running this lab locally or if you are going to create your own AWS/EC2 instance, download the App Dev Workshop Zip file locally, then proceed to unzip the file, rename it and cd into it:

=== "Linux/Mac OS"

    ```bash
    WSVERSION=1.7
    curl -OL https://github.com/signalfx/app-dev-workshop/archive/v$WSVERSION.zip
    unzip v$WSVERSION.zip
    mv app-dev-workshop-$WSVERSION workshop
    cd workshop
    ```

=== "Windows"

    !!! info
        Download the zip by clicking on the following URL <https://github.com/signalfx/app-dev-workshop/archive/v1.7.zip>.

        Once downloaded, unzip the the file and from the command prompt then change into that directory.

If you are using your own EC2 instance please skip to the [EC2 preparation section](../../module4/prep/#3-preparation-for-ec2-instances)

---

## 2. Preparation for Multipass

In this section you will  build and launch the Multipass instance which will run the Kubernetes (K3s) environment that you will use in multiple labs.

!!! important "Make sure to use your initials"
    During the build of your Multipass instance you need to provide a name, please use your initials `[YOUR_INITIALS]-k3s` so that the value of the instance hostname is unique e.g. `rwc-k3s`

!!! Warning
    In [Module 6](../../module6/) there are two applications available for deployment to emit Traces/Spans for SignalFx µAPM.

    **Hot R.O.D Multipass min. requirements:** 1 vCPU, 5Gb Disk, 1Gb Memory

    **Sock Shop Multipass min. requirements:** 4 vCPU, 15Gb Disk, 8Gb Memory

Ask which version is going to be used as part of this workshop, then select either the Hot R.O.D or Sock Shop Multipass launch parameters. Lines highlighted in yellow need to be edited:
=== "Hot R.O.D"

    ```text hl_lines="2"
    multipass launch \
    --name [YOUR_INITIALS]-k3s \
    --cloud-init cloud-init/k3s.yaml
    ```

=== "Sock Shop"

    ```text hl_lines="2"
    multipass launch \
    --name [YOUR_INITIALS]-k3s \
    --cloud-init cloud-init/k3s.yaml \
    --cpus 4 --disk 15G --mem 8G
    ```

Once the instance has been successfully created (this can take several minutes), shell into it.

=== "Input"

    ```bash hl_lines="1"
    multipass shell [YOUR_INITIALS]-k3s
    ```

=== "Output"
    ```text
     █████╗ ██████╗ ██████╗     ██████╗ ███████╗██╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔════╝██║   ██║
    ███████║██████╔╝██████╔╝    ██║  ██║█████╗  ██║   ██║
    ██╔══██║██╔═══╝ ██╔═══╝     ██║  ██║██╔══╝  ╚██╗ ██╔╝
    ██║  ██║██║     ██║         ██████╔╝███████╗ ╚████╔╝
    ╚═╝  ╚═╝╚═╝     ╚═╝         ╚═════╝ ╚══════╝  ╚═══╝  

    To run a command as administrator (user "root"), use "sudo <command>".
    See "man sudo_root" for details

    ubuntu@rwc-k3s:~$
    ```

Once your instance presents you with the App Dev logo, you have completed the preparation for your Multipass instance and can go directly to  the next lab [Deploying the Smart Agent in Kubernetes (K3s)](../../module4/k3s).

---

## 3. Preparation for EC2 Instances

In this section you will use terraform to build an EC2 instance in your favorite AWS region and will automatically deploy the Kubernetes (K3s) environment that you will use in multiple labs on it.

!!! Warning
    In [Module 6](../../module6/) there are two applications available for deployment to emit Traces/Spans for SignalFx µAPM.

    **Hot R.O.D EC2 Instance min. requirements:** _t2.micro_ 1 vCPU, 8Gb Disk, 1Gb Memory

    **Sock Shop EC2 Instance min. requirements:** _t2.largefrom_ 2 vCPU, 15Gb Disk, 8Gb Memory

Ask which version is going to be used as part of this workshop, then select either the Hot R.O.D or Sock Shop option when using terraform to launch your instance.

### Step 1: Prepare Terraform

The first step is to go into the sub-directory where the terraform files are located

=== "Input"

    ```bash 
    cd ec2
    ```

=== "Output"

    ```text
    ~/workshop/ec2$  
    ```

Verify that you are running version V0.12.12 or above of Terraform>

=== "Input"

    ```bash 
    terraform version
    ```

=== "Output"

    ```text
    Terraform v0.12.24
    ```

Initialize your terraform environment, this will download or upgrade the terraform providers plugins needed to run the terraform scripts in this directory.

=== "Input"

    ```bash 
    terraform init
    ```

=== "Output"
    ```text
    Initializing the backend...

    Initializing provider plugins...
    - Checking for available provider plugins...
    - Downloading plugin for provider "aws" (hashicorp/aws) 2.60.0...

    The following providers do not have any version constraints in configuration,
    so the latest version was installed.

    To prevent automatic upgrades to new major versions that may contain breaking
    changes, it is recommended to add version = "..." constraints to the
    corresponding provider blocks in configuration, with the constraint strings
    suggested below.

    * provider.aws: version = "~> 2.60"

    Terraform has been successfully initialized!

    You may now begin working with Terraform. Try running "terraform plan" to see
    any changes that are required for your infrastructure. All Terraform commands
    should now work.

    If you ever set or change modules or backend configuration for Terraform,
    rerun this command to reinitialize your working directory. If you forget, other
    commands will detect it and remind you to do so if necessary.
    ```

### Step 2: Creating your EC2 Instance

Creating the EC2 instance is done in two steps, a planning phase and an apply phase. The planning phase will validate the terraform scripts and check what changes it will make to your AWS environment. The apply phase will actually create the instances.
First you need to provide your AWS credentials to terraform, you do this by providing two environment variables.

=== "Input"

    ```bash hl_lines="1 2" 
    export AWS_ACCESS_KEY_ID="[YOUR_AWS_ACCESS_KEY_ID]"
    export AWS_SECRET_ACCESS_KEY="[YOUR_AWS_SECRET_ACCESS_KEY]"
    echo $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY
    ```

=== "Output"

    ```text
    ID: Axxxxxxxxxxxxxxxxy, KEY: Axxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxb
    ```

If you have confirmed that you have set you **AWS_SECRET_ACCESS_KEY_ID** & **AWS_SECRET_ACCESS_KEY** correctly, you can start with the planning phase to verify all is working correctly. During this phase you need to  provide the following inputs:

!!! note Required input for Terraform
    **Instance Count**: (If your not batch creating instances, type **1** to create a single Instance)

    **Desired AWS region**: (Any AWS region by name, for example **us-west-2**) 
    
    **Instance Type**:      (Type **1** for the Hot R.O.D. or **2** for the Sock Shop instance type)

    Please remember the values you provide as you will need them again for  the planning phase and when you use Terraform to destroy your EC2 instance.

Start the planning phase for Terraform. As we only wish to provide the input once, we are going to catch the output in a out file that we can reuse. Please provide your initials for the output file as indicated.

=== "Input"

    ```bash hl_lines="1"
    terraform plan -out=[YOUR_INITIALS].out
    ```

=== "Output"

    ```text
    var.aws_instance_count
    Instance Count (Usually 1) 

    Enter a value:
    ```

On the question Instance count, type 1 to indicate you wish a single EC2 instance to be created

=== "Input"

    ```bash hl_lines="1"
    Enter a value:  [NUMBER]
    ```

=== "Output"

    ```text
    var.aws_region
    Provide the desired region (for example: us-west-2)

    Enter a value: 
    ```
On the question, Provide the desired AWS region, enter the name of your favorite AWS region. This is where you want to deploy the EC2 instance in.

=== "Input"

    ```text hl_lines="1"
    Enter a value: [Your preferred AWS region name]
    ```

=== "Output"

    ```text
    var.instance_type
    Select instance type required (1 = Hot R.O.D. 2 = Sock Shop)
     
    Enter a value: 
    ```
On the question which instance types do you wish to use, choose **1** or **2**, If in doubt ask you workshop host.

=== "Input"

    ```bash  hl_lines="1"
     Enter a value: [1 or 2]
    ```

=== "Output"

    ```text
    Refreshing Terraform state in-memory prior to plan...
    The refreshed state will be used to calculate this plan, but will not be
    persisted to local or remote state storage.

    data.aws_ami.latest-ubuntu: Refreshing state...

    ------------------------------------------------------------------------

    An execution plan has been generated and is shown below.
    Resource actions are indicated with the following symbols:
    + create

    Terraform will perform the following actions:

    **(BIG WALL OF AWS RELATED TEXT REMOVED)**
    
    Plan: 2 to add, 0 to change, 0 to destroy.

    ------------------------------------------------------------------------

    This plan was saved to: [YOUR_INITIALS].out

    To perform exactly these actions, run the following command to apply:
    terraform apply "[YOUR_INITIALS].out"
    ```

If there are no errors in the output and terraform has created your output file, you can start the apply phase of Terraform. This will create the instance in AWS EC2.

=== "Input"

    ```bash hl_lines="1"
    terraform apply "[YOUR_INITIALS].out"
    ```

=== "Output"

    ```text
    ws_security_group.instance: Creating...
    aws_security_group.instance: Creation complete after 2s [id=sg-0459afecae5953b51]
    aws_instance.app-dev-instance[0]: Creating...
    aws_instance.app-dev-instance[0]: Still creating... [10s elapsed]
    aws_instance.app-dev-instance[0]: Still creating... [20s elapsed]
    aws_instance.app-dev-instance[0]: Creation complete after 23s [id=i-095a12cd39f8e2283]

    Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

    The state of your infrastructure has been saved to the path
    below. This state is required to modify and destroy your
    infrastructure, so keep it safe. To inspect the complete state
    use the `terraform show` command.

    State path: terraform.tfstate

    Outputs:

    ip = [
    "YOUR_IP-ADDRESS",
    ] 
    ```

Verify there are no errors and copy the ip address that you see in the green output.  

### Step 3: Connect to your EC2 Instance

Once the instance has been successfully created (this can take several minutes), ssh into it.
In most cases your ssh client will ask you to verify the connection.

=== "Input"

    ```bash hl_lines="1"
    ssh ubuntu@[YOUR_IP-ADDRESS]
    ```

=== "Output"

    ```text
    The authenticity of host '[YOUR_IP-ADDRESS] ([YOUR_IP-ADDRESS])' can't be established.
    ECDSA key fingerprint is SHA256:XdqN55g0z/ER660PARM+mGqtpYpwM3333YS9Ac8Y9hLY.
    Are you sure you want to continue connecting (yes/no/[fingerprint])?  
    ```

Please confirm that you wish to continue by replying to the prompt with  **yes**

=== "Input"

    ```bash hl_lines="1"
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
    ```

=== "Output"
    ```text
    Warning: Permanently added 'YOUR_IP-ADDRESS' (ECDSA) to the list of known hosts.

    ubuntu@YOUR_IP-ADDRESS's password:
    ```

To login to your instance please use the password provided by the workshop host.

=== "Input"

    ```bash hl_lines="1"
    ubuntu@[YOUR_IP-ADDRESS]'s password: [PASSWORD]
    ```

=== "Output"
    ```text
     █████╗ ██████╗ ██████╗     ██████╗ ███████╗██╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔════╝██║   ██║
    ███████║██████╔╝██████╔╝    ██║  ██║█████╗  ██║   ██║
    ██╔══██║██╔═══╝ ██╔═══╝     ██║  ██║██╔══╝  ╚██╗ ██╔╝
    ██║  ██║██║     ██║         ██████╔╝███████╗ ╚████╔╝
    ╚═╝  ╚═╝╚═╝     ╚═╝         ╚═════╝ ╚══════╝  ╚═══╝  

    To run a command as administrator (user "root"), use "sudo <command>".
    See "man sudo_root" for details

    ubuntu@ip-172-31-41-196:~$
    ```

Once your instance presents you with the App Dev logo, you have completed the preparation for your EC2 instance and can go directly to  the next lab [Deploying the Smart Agent in Kubernetes (K3s)](../../module4/k3s).
