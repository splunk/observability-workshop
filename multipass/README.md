# Launch a Multipass instance

## 1. Pre-requisites

Install [Multipass](https://multipass.run/)[^1] for your operating system. On a Mac you can also install via [Homebrew](https://brew.sh/) e.g. `brew install multipass`

## 2. Download cloud-init YAML

```
mkdir cloud-init
```

```
curl -sL https://git.io/JKYEQ -o cloud-init/k3s.yaml
```

For Linux/Mac OS set the instance name environment variable:

```
export INSTANCE=$(cat /dev/urandom | base64 | tr -dc 'a-z' | head -c4)
```

For Windows download the latest version of the workshop from [GitHub](https://github.com/signalfx/observability-workshop/archive/refs/heads/master.zip).

Once downloaded, unzip the the file and rename it to `workshop`. Then, from the command prompt change into the `workshop\cloud-init` directory and set the instance name environment variable:

```
$INSTANCE = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".tochararray() | sort {Get-Random})[0..3] -join ''
```

## 3. Launch Multipass instance

Build and launch a Multipass instance which will run the Kubernetes (K3s) environment that you will use in the workshop.

```text
multipass launch --name ${INSTANCE} --cloud-init cloud-init/k3s.yaml --cpus 4 --mem 8Gb --disk 32Gb
```

Once the instance has been successfully created (this can take several minutes), shell into it:

```
multipass shell ${INSTANCE}
```

```
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
