# Creating a Test Environment

You are going to need to record a number of values during this Workshop which we will export as variables in later steps so create `values.txt` locally to store the following values as you work through the Workshop.

=== "values.txt"
    ```text
    export SFXVOPSID=
    export ACCESS_TOKEN=
    export REALM=
    export ROUTINGKEY=

    Service_API_Endpoint=
    ```

---

## Multipass

The easiest way to test VictorOps is to use Multipass to run some local test VMs which will be monitored by SignalFx.

If you do not already have Multipass installed you can download the installer from [here](https://multipass.run/).

Mac OS users can install it using [Homebrew](https://brew.sh/) by running:

=== "Code"

    ```bash
    brew cask install multipass
    ```

## SignalFx Details

We will use [cloud-init](https://cloudinit.readthedocs.io/en/latest/) to install the SignalFx Agent into the VMs but we first need to obtain the **Access Token** and **Realm** from your SignalFx account.

You can find your Access Token by clicking on the **Settings** icon on the top right of the SignalFx UI, select **Organization Settings → Access Tokens**, expand the Default token, then click on **Show Token** to expose your token.

Click the **Copy** button to copy it to your clipboard, then paste it into your `values document` using the `ACCESS_TOKEN` parameter.

![Access Token](../../images/victorops/m7-access-token.png)

You will also need to obtain the name of the Realm for your SignalFx account.

Click on the **Settings** icon again, but this time select **My Profile**.

The Ream can be found in the middle of the page within the Organizations section.  In this example it is `us1`, make a note of this in your `values document` using the `REALM` parameter.

![Realm](../../images/victorops/m7-realm.png)

## Local VMs using Multipass

The next step is to pull down the `cloud-init` file to launch a pre-configure VM.

=== "Input"

    ```bash
    curl -s https://raw.githubusercontent.com/signalfx/app-dev-workshop/master/cloud-init/victorops-ec2.yaml -o victorops.yaml
    ```

Open `victorops.yaml` in your preferred editor and replace {==SIGNALFX_REALM==} & {==SIGNALFX_ACCESS_TOKEN==} with the values stored in your `values document`.

=== "victorops.yaml"

    ```yaml
    #cloud-config
    ssh_pwauth: yes
    password: AppDev2020!
    chpasswd:
    expire: false

    package_update: true

    packages:
    - unzip

    runcmd:
    # Download Workshop
    - export WSVERSION=v1.14
    - curl -s -OL https://github.com/signalfx/app-dev-workshop/archive/$WSVERSION.zip
    - unzip -qq $WSVERSION.zip -d /home/ubuntu/
    - mv /home/ubuntu/app-dev-workshop-${WSVERSION#v} /home/ubuntu/workshop
    # Configure motd
    - curl -s https://raw.githubusercontent.com/signalfx/app-dev-workshop/master/etc/motd -o /etc/motd
    - chmod -x /etc/update-motd.d/*
    # Install Terraform
    - curl -s -OL https://releases.hashicorp.com/terraform/0.12.25/terraform_0.12.25_linux_amd64.zip
    - unzip -qq terraform_0.12.25_linux_amd64.zip -d /usr/local/bin/
    # Set correct permissions on ubuntu user home directory
    - chown -R ubuntu:ubuntu /home/ubuntu
    # Install Smart Agent
    - curl -sSL https://dl.signalfx.com/signalfx-agent.sh > /tmp/signalfx-agent.sh
    - sh /tmp/signalfx-agent.sh --realm {==SIGNALFX_REALM==} -- {==SIGNALFX_ACCESS_TOKEN==}
    ```

Remaining in the same directory where you created the `victorops.yaml`, run the following commands to create two VMs.

The first command will generate a random unique 4 character string. This will prevent clashes in the SignalFx UI.

!!! note "Free up resources"
    You may also want to first shutdown any other VMs you still have running from previous modules to free up resources.

Create the 1st VictorOps VM:

=== "Input"

    ``` bash
    export INSTANCE=$(cat /dev/urandom | base64 | tr -dc 'a-z' | head -c4)
    multipass launch \
    --name ${INSTANCE}-vo1 \
    --cloud-init victorops.yaml
    ```

=== "Example Output"

    ```bash
    multipass launch \
    --name ixmy-vo1 \
    --cloud-init victorops.yaml
    Launched: ixmy-vo1
    ```

Create the 2nd VictorOps VM:

=== "Input"

    ``` bash
    multipass launch \
    --name ${INSTANCE}-vo2 \
    --cloud-init victorops.yaml
    ```

=== "Example Output"

    ```
    multipass launch \
    --name ixmy-vo2 \
    --cloud-init victorops.yaml
    Launched: ixmy-vo2
    ```

Once your two VMs have been created check within the SignalFx UI, **INFRASTRUCTURE** tab, and confirm they are reporting in correctly.

Allow a couple or minutes for the VMs to spin up, install updates and then install the SignalFx Agent etc.

If they fail to appear, double check your {==SIGNALFX_REALM==} and{==SIGNALFX_ACCESS_TOKEN==} settings within your `victorops.yaml` file.

If errors are found these can easily be updated directly within the VM.

Simply update the `token` or `api_url` and `ingest_url` files located within `/etc/signalfx` within the VM
