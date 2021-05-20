---
hide:
  - navigation # Hide navigation
  - toc        # Hide table of contents
---
# Launch a Multipass instance

---

## 1. Pre-requisites

Install [Multipass](https://multipass.run/){: target=_blank}[^1] for your operating system. Make sure you are using at least version `1.6.0`.

On a Mac you can also install via [Homebrew](https://brew.sh/){: target=_blank} e.g. `brew install multipass`

---

## 2. Download cloud-init YAML

=== "Linux/Mac OS"

    ```text
    WSVERSION=2.26
    mkdir cloud-init
    curl -s \
    https://raw.githubusercontent.com/signalfx/observability-workshop/v$WSVERSION/cloud-init/k3s.yaml \
    -o cloud-init/k3s.yaml
    export INSTANCE=$(cat /dev/urandom | base64 | tr -dc 'a-z' | head -c4)
    ```

=== "Windows"

    !!! info
        Download the zip by clicking on the following URL <https://github.com/signalfx/observability-workshop/archive/v2.26.zip>.

        Once downloaded, unzip the the file and rename it to `workshop`. Then, from the command prompt change into that directory
        and run

    ```
    $INSTANCE = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".tochararray() | sort {Get-Random})[0..3] -join ''
    ```

---

## 3. Launch Multipass instance

In this section you will build and launch the Multipass instance which will run the Kubernetes (K3s) environment that you will use in the workshop.

=== "Shell Command"

    ```text
    multipass launch \
    --name ${INSTANCE} \
    --cloud-init cloud-init/k3s.yaml \
    --cpus 4 \
    --mem 4Gb \
    --disk 32Gb
    ```

    Once the instance has been successfully created (this can take several minutes), shell into it.

    === "Shell Command"

        ```text
        multipass shell ${INSTANCE}
        ```

    === "Output"
    
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

    Once your instance presents you with the Splunk logo, you have completed the preparation for your Multipass instance and can at this point you are ready to continue and [start the workshop](../../otel/k3s/).

[^1]: Multipass is a lightweight VM manager for Linux, Windows and macOS. It's designed for developers who want a fresh Ubuntu environment with a single command. It uses KVM on Linux, Hyper-V on Windows and HyperKit on macOS to run the VM with minimal overhead. It can also use VirtualBox on Windows and macOS. Multipass will fetch images for you and keep them up to date.
