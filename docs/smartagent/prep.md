# Get Data In - Lab Summary

* Download the Workshop
* Start a Multipass[^1] or AWS/EC2 instance
* Deploy the SignalFx Smart Agent[^2] in K3s
* Validate Kubernetes[^3] K3s cluster is visible in Kubernetes Navigator
* Deploy a NGINX[^4] ReplicaSet in K3s
* Validate NGNIX metrics are flowing

---

## 1. Module Pre-requisites

=== "Running Locally"

    !!! note "Multipass"
        Install [Multipass](https://multipass.run/) for your operating system. Make sure you are using at least version `1.2.0`.

        On a Mac you can also install via [Homebrew](https://brew.sh/) e.g. `brew cask install multipass`

    !!! info "Struggling with Multipass?"
        Ask your instructor(s) for access to a pre-provisioned AWS/EC2 instance, you can then ignore the rest of this preparation lab and go straight to the next lab [Deploying the Smart Agent in Kubernetes (K3s)](../../smartagent/k3s).

=== "Running in AWS"

    !!! abstract "AWS/EC2 Instance"
        Install [Terraform](https://www.terraform.io/downloads.html) for your operating system. Please make sure it is version `0.12.18` or above.

        On a Mac you can also install via [Homebrew](https://brew.sh/) e.g. `brew install terraform`. This will get around Mac OS Catalina security.

---

## 2. Download App Dev Workshop

Regardless if you are running this lab locally or if you are going to create your own AWS/EC2 Instance you need to download the App Dev Workshop zip file locally, unzip the file, rename it and `cd` into the directory.

=== "Linux/Mac OS"

    ```bash
    WSVERSION=1.14
    curl -OL https://github.com/signalfx/app-dev-workshop/archive/v$WSVERSION.zip
    unzip v$WSVERSION.zip
    mv app-dev-workshop-$WSVERSION workshop
    cd workshop
    export INSTANCE=$(cat /dev/urandom | tr -dc 'a-z' | head -c4)
    ```

=== "Windows"

    !!! info
        Download the zip by clicking on the following URL <https://github.com/signalfx/app-dev-workshop/archive/v1.14.zip>.

        Once downloaded, unzip the the file and rename it to `workshop`. Then, from the command prompt change into that directory
        and run

    ```
    $INSTANCE = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".tochararray() | sort {Get-Random})[0..3] -join ''
    ```

If you are using your own AWS/EC2 instance please skip to [3. Launch Instance](../../smartagent/prep/#3-launch-instance) section and select the **Launch AWS/EC2 instance** tab

---

## 3. Launch Instance

=== "Launch Multipass instance"

    In this section you will  build and launch the Multipass instance which will run the Kubernetes (K3s) environment that you will use in multiple labs.

    For [µAPM](../../apm/) module we use the Hot R.O.D[^5] application to emit Traces/Spans for SignalFx µAPM. Launch your instance with:


    ```text
    multipass launch \
    --name $INSTANCE \
    --cloud-init cloud-init/k3s.yaml
    ```

    Once the instance has been successfully created (this can take several minutes), shell into it.

    === "Input"

        ```bash
        multipass shell $INSTANCE
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

        Waiting for cloud-init status...
        Your instance is ready!

        ubuntu@d823-k3s:~$
        ```

    Once your instance presents you with the App Dev logo, you have completed the preparation for your Multipass instance and can go directly to  the next lab [Deploy the Smart Agent in K3s](../../smartagent/k3s).

=== "Launch AWS/EC2 instance"

    In this section you will use terraform to build an AWS/EC2 instance in your favorite AWS region and will automatically deploy the Kubernetes (K3s) environment that you will use in this Workshop.

    !!! important "AWS Access Keys"
        You will need access to an AWS account to obtain both `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

    !!! warning "Minimum requirements"
        For the [µAPM](../../apm/) module we are using the Hot R.O.D. application.  The minimum requirements are:

        **Hot R.O.D AWS/EC2 Instance min. requirements:** _t2.micro_ 1 vCPU, 8Gb Disk, 1Gb Memory

    **Prepare Terraform**

    The first step is to go into the sub-directory where the Terraform files are located and initialise Terraform and upgrade the AWS Terraform Provider.

    === "Input"

        ```bash
        cd ec2
        terraform init -upgrade
        ```

    === "Output"
        ```text
        ~/workshop/ec2$ terraform init -upgrade
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

    ---

    **Create AWS/EC2 Instance**

    Creating the AWS/EC2 instance is done in two steps, a planning phase and an apply phase.

    * The planning phase will validate the Terraform scripts and check what changes it will make to your AWS environment.
    * The apply phase will actually create the instance.

    First, you need to create environment variables for your AWS access keys.

    === "Input"

        ```bash
        export AWS_ACCESS_KEY_ID="{==YOUR_AWS_ACCESS_KEY_ID==}"
        export AWS_SECRET_ACCESS_KEY="{==YOUR_AWS_SECRET_ACCESS_KEY==}"
        echo $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY
        ```

    === "Output"

        ```text
        ID: Axxxxxxxxxxxxxxxxy, KEY: Axxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxb
        ```

    Once you have confirmed that you have set you `AWS_SECRET_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY` correctly, you can start with the planning phase.

    !!! important Required input for Terraform

        **Desired AWS Region**: (Any AWS region by name, for example **us-west-2**)

        Please remember these values as you will need them again for the planning phase and when you use Terraform to destroy your AWS/EC2 instance.

    As we only wish to provide the input once, we are going to capture the output in a `.out` file that we can use for the apply step. Please provide your initials for the output file as indicated.

    === "Input"

        ```bash
        terraform plan -var="aws_instance_count=1" -var="instance_type=1" -out=app-dev-plan.out
        ```

    Enter your desired AWS Region where you wish to run the AWS/EC2 instance e.g. **us-west-2**

    === "Example"

        ```text hl_lines="4"
        var.aws_region
        Provide the desired region

        Enter a value: us-west-2
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

        This plan was saved to: app-dev-plan.out

        To perform exactly these actions, run the following command to apply:
        terraform apply "app-dev-plan.out"
        ```

    If there are no errors in the output and terraform has created your output file, you can start the apply phase of Terraform. This will create the AWS/EC2 instance.

    === "Input"

        ```bash
        terraform apply "app-dev-plan.out"
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
        "YOUR IP ADDRESS",
        ] 
        ```

    Verify there are no errors and copy the ip address that you see in the green output.

    ---

    **SSH into AWS/EC2 Instance**

    Once the instance has been successfully created (this can take several minutes), ssh into it.
    In most cases your ssh client will ask you to verify the connection.

    === "Input"

        ```bash hl_lines="1"
        ssh ubuntu@YOUR IP ADDRESS
        ```

    === "Output"

        ```text
        The authenticity of host 'YOUR IP ADDRESS (YOUR IP ADDRESS)' can't be established.
        ECDSA key fingerprint is SHA256:XdqN55g0z/ER660PARM+mGqtpYpwM3333YS9Ac8Y9hLY.
        Are you sure you want to continue connecting (yes/no/[fingerprint])?
        ```

    Please confirm that you wish to continue by replying to the prompt with `yes`

    === "Input"

        ```bash hl_lines="1"
        Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
        ```

    === "Output"
        ```text
        Warning: Permanently added 'YOUR IP ADDRESS' (ECDSA) to the list of known hosts.

        ubuntu@YOUR IP ADDRESS's password:
        ```

    To login to your instance please use the password provided by the Workshop host.

    === "Input"

        ```bash hl_lines="1"
        ubuntu@YOUR IP ADDRESS's password: PASSWORD
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


        Waiting for cloud-init status...
        Your instance is ready!

        ubuntu@ip-172-31-41-196:~$
        ```

    Once your instance presents you with the App Dev logo, make sure you see `Your instance is ready!` in the output.

    You have now completed the preparation for your AWS/EC2 instance and can go directly to  the next lab [Deploy the Smart Agent in K3s](../../smartagent/k3s).

[^1]: Multipass is a lightweight VM manager for Linux, Windows and macOS. It's designed for developers who want a fresh Ubuntu environment with a single command. It uses KVM on Linux, Hyper-V on Windows and HyperKit on macOS to run the VM with minimal overhead. It can also use VirtualBox on Windows and macOS. Multipass will fetch images for you and keep them up to date.
[^2]: The SignalFx Smart Agent gathers host performance, application, and service-level metrics from both containerized and non-container environments. The Smart Agent installs with more than 100 bundled monitors for gathering data, including Python-based plug-ins such as Mongo, Redis, and Docker.
[^3]: [What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
[^4]: [What is NGINX?](https://www.nginx.com/resources/glossary/nginx/)
[^5]: [What is Hot R.O.D.?](https://github.com/jaegertracing/jaeger/tree/master/examples/hotrod)
