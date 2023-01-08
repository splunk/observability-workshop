# Launch a Multipass instance

## 1. Pre-requisites

Install [Multipass](https://multipass.run/)[^1] and Terraform for your operating system. On a Mac you can also install via [Homebrew](https://brew.sh/) e.g.

```text
brew install multipass
brew install terraform
```

## 2. Clone workshop repository

```bash
git clone https://github.com/signalfx/observability-workshop
```

## 3. Change into multipass directory

```bash
cd observability-workshop/multipass
```

## 4. Initialise Terraform

```bash
terraform init
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

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

## 5. Terraform plan

```bash
terraform plan
```

You will see similar output to this:

```terraform
var.splunk_access_token
  Splunk Oberservability Cloud Access Token

  Enter a value: xxx

var.splunk_presetup
  Presetup the instance? (true/false)

  Enter a value: true

var.splunk_realm
  Splunk Oberservability Cloud Realm (us0, us1, us2, eu0, jp0, au0)

  Enter a value: eu0

var.splunk_rum_token
  Splunk Oberservability Cloud RUM Token

  Enter a value: xxx

data.template_file.user_data: Reading...
data.template_file.user_data: Read complete after 0s [id=64bb9842ad5c5cf56fe9be09ba73f5e3b4dadffd9606921f07b42beacbdb01cb]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # local_file.user_data will be created
  + resource "local_file" "user_data" {
      + content              = <<-EOT
            #cloud-config
            ssh_pwauth: yes
            password: Observability2022!
            chpasswd:
              expire: false
            
            package_update: true
            
            packages:
              - unzip
              - shellinabox
              - lynx
              - w3m
              - gnupg2
              - docker-compose
              - podman
              - python3-venv
              - jq
              - maven
              - openjdk-11-jdk
              - python3-pip
            
            groups:
              - docker
            
            system_info:
              default_user:
                groups: [docker]
            
            write_files:
              - path: /etc/skel/.profile
                append: true
                content: |
                  helm() {
            
                    echo >&2 "Using ACCESS_TOKEN=xxx"
                    echo >&2 "Using REALM=eu0"
            
                    command helm "$@"
                  }
            
                  terraform() {
            
                    echo >&2 "Using ACCESS_TOKEN=xxx"
                    echo >&2 "Using REALM=eu0"
            
                    command terraform "$@"
                  }
            
                  echo "Waiting for cloud-init status..."
                  if ! /usr/bin/timeout 180 grep -q 'Cloud-init .*finished at' <(sudo tail -f /var/log/cloud-init-output.log); then
                    echo "Instance setup did not complete after 3 minutes. Please try again.";
                  else
                    echo "Your instance is ready!";
                  fi
            
                  if [ -e /etc/.instance ]; then
                    INSTANCE=$(cat /etc/.instance)
                    CLUSTER_NAME="$INSTANCE-cluster"
                  fi
                  export INSTANCE CLUSTER_NAME
                    
            
                  export REALM=eu0
                  export ACCESS_TOKEN=xxx
                  export RUM_TOKEN=xxx
                  if [ ! -f ~/.helmok} ]; then
                    helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart 
                    helm repo update
                    helm install splunk-otel-collector --set="splunkObservability.realm=$REALM" --set="splunkObservability.accessToken=$ACCESS_TOKEN" --set="clusterName=$INSTANCE-k3s-cluster" --set="splunkObservability.logsEnabled=true" --set="splunkObservability.profilingEnabled=true" --set="splunkObservability.infrastructureMonitoringEventsEnabled=true" --set="environment=$INSTANCE-apm-env" splunk-otel-collector-chart/splunk-otel-collector -f ~/workshop/k3s/otel-collector.yaml
                    cd ~/workshop/apm/
                    ./apm-config.sh -r
                    sudo kubectl apply -f deployment.yaml
                    echo $INSTANCE > ~/.helmok
                  fi  
            
                  # Set prompt
                  export PS1='\u@\h:\w$ '
                  export KUBECONFIG=/home/ubuntu/.kube/config
                  alias kc='kubectl'
                  alias dc='docker-compose'
                  alias docker='podman'
              - path: /etc/rancher/k3s/registries.yaml
                permissions: '0600'
                owner: root:root
                content: |
                  mirrors:
                    docker.registry:
                      endpoint:
                        - "http://docker.registry:9999"
              - path: /etc/containers/registries.conf.d/docker.registry.conf
                permissions: '0644'
                owner: root:root
                content: |
                  [[registry]]
                  location="docker.registry:9999"
                  insecure=true
              - path: /etc/docker/daemon.json
                content: |
                  {
                    "insecure-registries" : ["docker.registry:9999"]
                  }
              - path: /usr/local/bin/setup-docker-registry.sh
                permissions: '0744'
                content: |
                  #!/usr/bin/env bash
                  REGISTRY_NAME=docker.registry
                  REGISTRY_PORT=9999
                  NODE_IP=$(ip -o -4 addr | awk '$2 != "lo" { print $4}' | sed -e 's,/[[:digit:]]\+$,,')
                  echo "$NODE_IP $REGISTRY_NAME" | tee -a /etc/hosts
                  echo "$NODE_IP $REGISTRY_NAME" | tee -a /etc/cloud/templates/hosts.debian.tmpl
                  systemctl restart docker
              - path: /usr/local/bin/local-setup.sh
                permissions: "0744"
                content: |
                  if [ -e /etc/.instance ]; then
                    INSTANCE=$(cat /etc/.instance)
                  fi
                  if [ -z ${INSTANCE+x} ]; then
                    INSTANCE=$(cat /dev/urandom | base64 | tr -dc 'a-z' | head -c4)
                    sed -i "s/127.0.0.1.*/127.0.0.1 $INSTANCE.local $INSTANCE localhost/" /etc/hosts
                    sed -i "s/127.0.0.1.*/127.0.0.1 $INSTANCE.local $INSTANCE localhost/" /etc/cloud/templates/hosts.debian.tmpl
                    sudo hostnamectl set-hostname $INSTANCE
                    echo $INSTANCE > /etc/.instance
                  fi
                  export INSTANCE
            
            runcmd:
              # Install Helm
              - curl -s https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
              # Install K9s (Kubernetes UI)
              - curl -S -OL https://github.com/derailed/k9s/releases/download/v0.26.7/k9s_Linux_x86_64.tar.gz
              - tar xfz k9s_Linux_x86_64.tar.gz -C /usr/local/bin/ k9s
              # Download Workshop
              - export WSVERSION=4.36
              - 'export WSARCHIVE=$([ "$WSVERSION" = "main" ] && echo "main" || echo "v$WSVERSION")'
              - curl -s -OL https://github.com/signalfx/observability-workshop/archive/$WSARCHIVE.zip
              - unzip -qq $WSARCHIVE.zip -d /home/ubuntu/
              - mkdir /home/ubuntu/workshop
              - mv /home/ubuntu/observability-workshop-$WSVERSION/workshop/* /home/ubuntu/workshop
              - rm -rf /home/ubuntu/observability-workshop-$WSVERSION
              # Set apm-config.sh executable
              - chmod +x /home/ubuntu/workshop/apm/apm-config.sh
              # Download Splunk Observability Cloud Jumpstart
              - curl -s -L https://github.com/signalfx/signalfx-jumpstart/archive/main.zip -o jumpstart.zip
              - unzip -qq jumpstart.zip -d /home/ubuntu/
              - mv /home/ubuntu/signalfx-jumpstart-main /home/ubuntu/signalfx-jumpstart
              # Configure motd
              - curl -s https://raw.githubusercontent.com/signalfx/observability-workshop/main/workshop/cloud-init/motd -o /etc/motd
              - chmod -x /etc/update-motd.d/*
              # Install Terraform
              - curl -S -OL https://releases.hashicorp.com/terraform/1.2.8/terraform_1.2.8_linux_amd64.zip 
              - unzip -qq terraform_1.2.8_linux_amd64.zip -d /usr/local/bin
              - bash /usr/local/bin/setup-docker-registry.sh
              - bash /usr/local/bin/local-setup.sh
              # Install K3s
              - curl -sfL https://get.k3s.io | sh -
              # Create kube config and set correct permissions on ubuntu user home directory
              - mkdir /home/ubuntu/.kube && kubectl config view --raw > /home/ubuntu/.kube/config
              - chmod 400 /home/ubuntu/.kube/config
              - chown -R ubuntu:ubuntu /home/ubuntu
              # Deploy private registry
              - /usr/local/bin/kubectl apply -f /home/ubuntu/workshop/k3s/registry/registry.yaml
              # Configure shellinabox port and disable ssl then restart
              - sed -i 's/SHELLINABOX_PORT=4200/SHELLINABOX_PORT=6501/'  /etc/default/shellinabox
              - sed -i "s/\"--no-beep\"/\"--no-beep --disable-ssl\"/" /etc/default/shellinabox
              - sudo service shellinabox restart
        EOT
      + directory_permission = "0777"
      + file_permission      = "0777"
      + filename             = "ubuntu-cloudinit.yml"
      + id                   = (known after apply)
    }

  # multipass_instance.ubuntu will be created
  + resource "multipass_instance" "ubuntu" {
      + cloudinit_file = "ubuntu-cloudinit.yml"
      + cpus           = 4
      + disk           = "32GiB"
      + image          = "jammy"
      + memory         = "8096MiB"
      + name           = (known after apply)
    }

  # random_string.hostname will be created
  + resource "random_string" "hostname" {
      + id          = (known after apply)
      + length      = 4
      + lower       = true
      + min_lower   = 0
      + min_numeric = 0
      + min_special = 0
      + min_upper   = 0
      + number      = false
      + numeric     = false
      + result      = (known after apply)
      + special     = false
      + upper       = false
    }

Plan: 3 to add, 0 to change, 0 to destroy.
```

## 6. Terraform apply

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

ubuntu@vmpe:~$
```

Once your instance presents you with the Splunk logo, you have completed the preparation for your Multipass instance and can at this point you are ready to continue and [start the workshop](https://signalfx.github.io/observability-workshop/latest/).

[^1]: Multipass is a lightweight VM manager for Linux, Windows and macOS. It's designed for developers who want a fresh Ubuntu environment with a single command. It uses KVM on Linux, Hyper-V on Windows and HyperKit on macOS to run the VM with minimal overhead. It can also use VirtualBox on Windows and macOS. Multipass will fetch images for you and keep them up to date.
