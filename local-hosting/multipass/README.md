# Preparing a Multipass instance

**NOTE:** Please disable any VPNs or proxies before running the commands below e.g:

- ZScaler
- Cisco AnyConnect

These tools **will** prevent the instance from being created properly.

## 1. Pre-requisites

Install [Multipass](https://multipass.run/) and Terraform for your operating system. On a Mac, you can also install via [Homebrew](https://brew.sh/) e.g.

```text
brew install multipass
brew install terraform
```

**NOTE:** Make sure you have mulitpass `1.12.0` or above installed!

```bash
multipass --version

multipass   1.12.0+mac
multipassd  1.12.0+mac
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
terraform init -upgrade
```

```text
Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/random...
- Finding latest version of hashicorp/local...
- Finding larstobi/multipass versions matching "~> 1.4.1"...
- Installing hashicorp/random v3.5.1...
- Installed hashicorp/random v3.5.1 (signed by HashiCorp)
- Installing hashicorp/local v2.4.0...
- Installed hashicorp/local v2.4.0 (signed by HashiCorp)
- Installing larstobi/multipass v1.4.2...
- Installed larstobi/multipass v1.4.2 (self-signed, key ID 797707331BF3549C)
```

## 5. Terraform variables description

### Required variables

- `splunk_access_token`: Observability Access Token
- `splunk_api_token`: Observability API Token
- `splunk_rum_token`: Observability RUM Token
- `splunk_realm`: Observability Realm e.g. `eu0`
- `splunk_hec_url`: Splunk HEC URL
- `splunk_hec_token`: Splunk HEC Token

### Instance type variables

- `splunk_presetup`: Provide a preconfigured instance (OTel Collector and Online Boutique deployed with RUM enabled). The default is `false`.
- `splunk_jdk`: Install OpenJDK and Maven on the instance. The default is `false`.
- `otel_demo` : Install and configure the OpenTelemetry Astronomy Shop Demo. This requires that `splunk_presetup` is set to `false`. The default is `false`

### Optional advanced variables

- `wsversion`: Set this to `main` if working on development of the workshop, otherwise this can be omitted.

## 6. Create Terraform variables file

Variables are kept in file `terrform.tfvars` and we provide a template as `terraform.tfvars.template` to copy and edit:

```bash
cp terraform.tfvars.template terraform.tfvars
```

The file `terraform.tfvars` is ignored by git and should not be committed to the repository.

Edit `terraform.tfvars` and set the variables accordingly to your needs e.g.

```text
splunk_access_token = "1234xxxx5678yyyy"
splunk_rum_token = "1234xxxx5678yyyy"
splunk_realm = "us1"
splunk_presetup = true
splunk_jdk = false
otel_demo = false
```

Run `terraform plan` to check that all configuration is OK. Once happy run `terraform apply` to create the instance.

## 7. Terraform plan

```bash
terraform plan
```

## 8. Terraform apply

```bash
terraform apply
```

``` text
random_string.hostname: Creating...
random_string.hostname: Creation complete after 0s [id=cynu]
local_file.user_data: Creating...
local_file.user_data: Creation complete after 0s [id=46a5c50e396a1a7820c3999c131a09214db903dd]
multipass_instance.ubuntu: Creating...
multipass_instance.ubuntu: Still creating... [10s elapsed]
multipass_instance.ubuntu: Still creating... [20s elapsed]
...
multipass_instance.ubuntu: Still creating... [1m30s elapsed]
multipass_instance.ubuntu: Creation complete after 1m38s [name=cynu]
data.multipass_instance.ubuntu: Reading...
data.multipass_instance.ubuntu: Read complete after 1s [name=cynu]

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

Outputs:

instance_details = [
  {
    "image" = "Ubuntu 22.04.2 LTS"
    "image_hash" = "345fbbb6ec82 (Ubuntu 22.04 LTS)"
    "ipv4" = "192.168.205.185"
    "name" = "cynu"
    "state" = "Running"
  },
]
```

Once the instance has been successfully created (this can take several minutes), shell into it using the `name` output above e.g.

```bash
multipass shell cynu
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

ubuntu@cynu ~ $
```

## 9. Validate instance

SSH into your instance using the IP address from the `instance_details`. Once in the shell you can validate that the instance is ready by running the following command:

```bash
kubectl version --output=yaml
```

If you get an error please check that you have disabled any VPNs or proxies and try again e.g. ZScaler, Cisco AnyConnect.

To start again, delete the instance and re-run `terraform apply`:

```bash
terraform destroy
```
