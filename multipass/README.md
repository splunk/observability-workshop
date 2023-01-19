# Launch a Multipass instance

## 1. Pre-requisites

Install [Multipass](https://multipass.run/)[^1] and Terraform for your operating system. On a Mac you can also install via [Homebrew](https://brew.sh/) e.g.

```text
brew install multipass
brew install terraform
```

## 2. Clone workshop repository

```bash
git clone https://github.com/splunk/observability-workshop
```

## 3. Change into multipass directory

```bash
cd observability-workshop/multipass
```

## 4. Initialise Terraform

```bash
terraform init --upgrade
```

```text
Initializing the backend...

Initializing provider plugins...
- Reusing previous version of hashicorp/template from the dependency lock file
- Reusing previous version of larstobi/multipass from the dependency lock file
- Reusing previous version of hashicorp/local from the dependency lock file
- Reusing previous version of hashicorp/random from the dependency lock file
- Using previously-installed hashicorp/random v3.4.3
- Using previously-installed hashicorp/template v2.2.0
- Using previously-installed larstobi/multipass v1.4.1
- Using previously-installed hashicorp/local v2.2.3

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see any changes that are required for your infrastructure. All Terraform commands should now work.

If you ever set or change modules or backend configuration for Terraform, rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

## 5. Terraform variables description

- `splunk_access_token`: Observability Access Token
- `splunk_rum_token`: Observability RUM Token
- `splunk_realm`: Observability Realm
- `splunk_presetup`: Provide a preconfigured instance (OTel Collector and Online Boutique deployed with RUM enabled)
- `splunk_jdk`: Install OpenJDK and Maven on the instance (for PetClinic workshop or other Java based workshops)

## 6. Create Terraform variables file

Variables are kept in file `terrform.tfvars` and we provide a template as `terraform.tfvars.template` to copy and edit:

```bash
cp terraform.tfvars.template terraform.tfvars
```

The file `terraform.tfvars` is ignored by git and should not be committed to the repo.

Edit `terraform.tfvars` and set the variables accordingly to your needs e.g.

```text
splunk_access_token = "1234xxxx5678yyyy"
splunk_rum_token = "1234xxxx5678yyyy"
splunk_realm = "us1"
splunk_presetup = true
splunk_jdk = false
```

Then run `terraform plan` to see what will be created. Once happy run `terraform apply` to create the instances.

## 7. Terraform plan

```bash
terraform plan
```

## 8. Terraform apply

```bash
terraform apply
```

```local_file.user_data: Creating...
local_file.user_data: Creation complete after 0s [id=00ffc34e2fc7ebff9a09f80f53ec508544aa55d8]
multipass_instance.ubuntu: Creating...
multipass_instance.ubuntu: Still creating... [10s elapsed]
...
multipass_instance.ubuntu: Still creating... [4m30s elapsed]
multipass_instance.ubuntu: Creation complete after 4m39s [name=lsvt]
```

Once the instance has been successfully created (this can take several minutes), shell into it using the `name` output above e.g.

```bash
multipass shell lsvt
```

```text
███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗
██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗
███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗
╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝
███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝
╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝

To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details

Waiting for cloud-init status...
Your instance is ready!

ubuntu@lsvt ~ $
```

Once your instance presents you with the Splunk logo, you have completed the preparation for your Multipass instance and can at this point you are ready to continue and [start the workshop](https://splunk.github.io/observability-workshop/latest/).

[^1]: Multipass is a lightweight VM manager for Linux, Windows and macOS. It's designed for developers who want a fresh Ubuntu environment with a single command. It uses KVM on Linux, Hyper-V on Windows and HyperKit on macOS to run the VM with minimal overhead. It can also use VirtualBox on Windows and macOS. Multipass will fetch images for you and keep them up to date.
