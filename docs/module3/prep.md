# Lab Summary

* Download the workshop and configure Kubernetes ([K3s](https://k3s.io/)) environment.

---

## Let’s bake some K8s

If you have chosen to run the workshop on a [AWS/EC2 instance](../module-support/ec2-setup.md), please follow instructions given to connect and run the Workshop as described, however skip the Multipass commands in the next section.

If you are  going to run this locally please install [Multipass](https://multipass.run/) for your OS. Make sure you are using at least version `1.2.0`. On a Mac you can also install via [Homebrew](https://brew.sh/) e.g. `brew cask install multipass`

Regardless if you are running this lab locally or using an AWS/EC2 instance, download the App Dev Workshop Master Zip file locally or on to the EC2 instance, then proceed to unzip the file, rename it and cd into it:

=== "Linux/Mac OS"

    ```bash
    WSVERSION=1.3
    curl -OL https://github.com/signalfx/app-dev-workshop/archive/v$WSVERSION.zip
    unzip v$WSVERSION.zip
    mv app-dev-workshop-$WSVERSION workshop
    cd workshop
    ```

=== "Windows"

    !!! info
        Download the zip by clicking on the following URL <https://github.com/signalfx/app-dev-workshop/archive/v1.2.zip>.

        Once downloaded, unzip the the file and from the command prompt change into that directory.

When using an EC2 instance you can skip the following section and continue to [Deploying the Smart Agent in Kubernetes (K3s)](../../module3/k3s/#2-ive-got-the-key-ive-got-the-secret)

Launch the Multipass instance which will run Kubernetes (K3s)

!!! Warning
    In [Module 6](../../module6/) there are two applications available for deployment to emit Traces/Spans for SignalFx µAPM.

    **Hot R.O.D minimum requirements:** 1 vCPU, 5Gb Disk, 1Gb Memory

    **Sock Shop minimum requirements:** 2 vCPU, 15Gb Disk, 4Gb Memory

!!! note
    Use `[YOUR_INITIALS]-k3s` so that the value of the instance hostname is unique e.g. `rwc-k3s`

Select either the Hot R.O.D or Sock Shop Multipass launch parameters. Lines highlighted in yellow need to be edited:

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
    --cpus=4 --disk=15G --mem=8G
    ```

Once the instance has been successfully created shell into it.

=== "Input"

    ```bash hl_lines="1"
    multipass shell [YOUR_INITIALS]-k3s
    ```

![Shell](../images/module3/shell.png)
