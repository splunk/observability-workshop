---
title: How to connect to your workshop environment
linkTitle: 1.1 Access AWS/EC2 Instance
weight: 2
authors: ["Tim Hard"]
time: 5 minutes
draft: false
---

1. How to retrieve the IP address of the AWS/EC2 instance assigned to you.
2. Connect to your instance using SSH, Putty[^1] or your web browser.
3. Verify your connection to your AWS/EC2 cloud instance.
4. Using Putty (Optional)
5. Using Multipass (Optional)

---

## 1. AWS/EC2 IP Address

In preparation for the workshop, Splunk has prepared an Ubuntu Linux instance in AWS/EC2.

To get access to the instance that you will be using in the workshop please visit the URL to access the Google Sheet provided by the workshop leader.

Search for your AWS/EC2 instance by looking for your first and last name, as provided during registration for this workshop.

![attendee spreadsheet](../../images/spreadsheet-info.png)

Find your allocated IP address, SSH command (for Mac OS, Linux and the latest Windows versions) and password to enable you to connect to your workshop instance.

It also has the Browser Access URL that you can use in case you cannot connect via SSH or Putty - see [EC2 access via Web browser](#4-web-browser-all)

{{% notice title="Important" style="info" %}}
Please use SSH or Putty to gain access to your EC2 instance if possible and
make a note of the IP address as you will need this during the workshop.
{{% /notice %}}

## 2. SSH (Mac OS/Linux)

Most attendees will be able to connect to the workshop by using SSH from their Mac or Linux device, or on Windows 10 and above.

To use SSH, open a terminal on your system and type `ssh splunk@x.x.x.x` (replacing x.x.x.x with the IP address found in Step #1).

![ssh login](../../images/ssh-1.png)

When prompted **`Are you sure you want to continue connecting (yes/no/[fingerprint])?`** please type **`yes`**.

![ssh password](../../images/ssh-2.png)

Enter the password provided in the Google Sheet from Step #1.

Upon successful login, you will be presented with the Splunk logo and the Linux prompt.

![ssh connected](../../images/ssh-3.png)

## 3. SSH (Windows 10 and above)

The procedure described above is the same on Windows 10, and the commands can be executed either in the Windows Command Prompt or PowerShell.
However, Windows regards its SSH Client as an "optional feature", which might need to be enabled.

You can verify if SSH is enabled by simply executing `ssh`

If you are shown a help text on how to use the SSH command (like shown in the screenshot below), you are all set.

![Windows SSH enabled](../../images/windows-ssh-enabled-feedback.png)

If the result of executing the command looks something like the screenshot below, you want to enable the "OpenSSH Client" feature manually.

![Windows SSH disabled](../../images/windows-ssh-disabled-feedback.png)

To do that, open the "Settings" menu, and click on "Apps". While in the "Apps & features" section, click on "Optional features".

![Windows Apps Settings](../../images/windows-gui-optionalfeatures.png)

Here, you are presented with a list of installed features. On the top, you see a button with a plus icon to "Add a feature". Click it.
In the search input field, type "OpenSSH", and find a feature called "OpenSSH Client",  or respectively, "OpenSSH Client (Beta)", click on it, and click the "Install"-button.

![Windows Enable OpenSSH Client](../../images/windows-enable-openssh-client.png)

Now you are set! In case you are not able to access the provided instance despite enabling the OpenSSH feature, please do not shy away from reaching
out to the course instructor, either via chat or directly.

At this point you are ready to continue and [start the workshop](../gdi/index.html)

---

## 4. Putty (For Windows Versions prior to Windows 10)

If you do not have SSH pre-installed or if you are on a Windows system, the best option is to install Putty which you can find [here.](https://www.putty.org/)

{{% notice title="Important" style="info" %}}
If you **cannot** install Putty, please go to [Web Browser (All)](#4-web-browser-all).
{{% /notice %}}
  
Open Putty and enter in the **Host Name (or IP address)** field the IP address provided in the Google Sheet.

You can optionally save your settings by providing a name and pressing **Save**.

![putty-2](../../images/putty-settings.png)

To then login to your instance click on the **Open** button as shown above.

If this is the first time connecting to your AWS/EC2 workshop instance, you will be presented with a security dialogue, please click **Yes**.

![putty-3](../../images/putty-security.png)

Once connected, login in as **splunk** and the password is the one provided in the Google Sheet.

Once you are connected successfully you should see a screen similar to the one below:

![putty-4](../../images/putty-loggedin.png)

At this point, you are ready to continue and [start the workshop](../gdi/index.html)

---

## 5. Web Browser (All)

If you are blocked from using SSH (Port 22) or unable to install Putty you may be able to connect to the workshop instance by using a web browser.

{{% notice title="Note" style="info" %}}
This assumes that access to port 6501 is not restricted by your company's firewall.
{{% /notice %}}

Open your web browser and type **[http://x.x.x.x:6501](http://x.x.x.x:6501)** (where X.X.X.X is the IP address from the Google Sheet).

![http-6501](../../images//shellinabox-url.png)

Once connected, login in as **splunk** and the password is the one provided in the Google Sheet.

![http-connect](../../images//shellinabox-connect.png)

Once you are connected successfully you should see a screen similar to the one below:

![web login](../../images//shellinabox-login.png)

Unlike when you are using regular SSH, *copy and paste* does require a few extra steps to complete when using a browser session. This is due to cross browser restrictions.

When the workshop asks you to copy instructions into your terminal, please do the following:

*Copy the instruction as normal, but when ready to paste it in the web terminal, choose **Paste from the browser** as show below:*

![web paste 1](../../images//shellinabox-paste-browser.png)

This will open a dialogue box asking for the text to be pasted into the web terminal:

![web paste 3](../../images//shellinabox-example-1.png)

Paste the text in the text box as shown, then press **OK** to complete the copy and paste process.

{{% notice title="Note" style="info" %}}
Unlike regular SSH connection, the web browser has a 60-second time out, and you will be disconnected, and a **Connect** button will be shown in the center of the web terminal.

Simply click the **Connect** button and you will be reconnected and will be able to continue.
{{% /notice %}}

![web reconnect](../../images//shellinabox-reconnect.png)

At this point, you are ready to continue and [start the workshop](../gdi/index.html).

---

## 6. Multipass (All)

If you are unable to access AWS but want to install software locally, follow the instructions for [using Multipass](https://github.com/splunk/observability-workshop/blob/main/multipass/README.md).

[^1]: [Download Putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/)
