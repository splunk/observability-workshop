# How to connect to your workshop environment

1. How to retrieve the IP address of the EC@ instance assigned to you.
2. Connect to your instance using ssh, putty or browser.
3. Verify Your connection to your AWS cloud instance.

---

## 1. How to retrieve the IP address of the EC2 instance assigned to you

In preparation for the workshop, signalFX has prepared a Linux Instance on AWS for you.
To get access to the instance that you will be using in the workshop please visit the URl provided by the workshop leader and search for your name by entering your first name as you have provided it with your registration for the workshop.

![attendee spreadsheet](../images/intro/search-spreadsheet.png){: .zoom}

This should give you a list as shown above,  it will provide you with the  ip address, the SSH command and the password to use to connect to the workshop instance.

!!! important
    Please make a note of the IP address as you will need this during the workshop

## 2. Connect to your instance using regular ssh

Most attendees should be able to connect to the workshop by using ssh directly.
ssh is a commonly used tool to connect to cloud instances.
To use ssh, open a command prompt on your system and type ssh ubuntu@x.x.x.x  (Where you replace x.x.x.x with the Ip address found in step 1. In this case below ssh ubuntu@3.127.80.222)

![ssh login](../images/intro/ssh-1.png){: .zoom}

Due to ssh security it is possible that you need to a on time confirmation that you wish to connect to this cloud instance,, please type **yes**

![ssh password](../images/intro/ssh-2.png){: .zoom}

You then will be presented with a request for a password, this is the password found in the spreadsheet in section 1.

Once you have successfully logged in you should be represented with a screen similar to the one below.

![ssh connected](../images/intro/ssh-3.png){: .zoom}

At this point you are ready to continue and [start the workshop](https://signalfx.github.io/observability-workshop/latest/smartagent/k3s/)

---

## 3. Connect to your instance using putty (Windows)

---

## 4. Connect to your instance using a browser

If you are restricted and you cannot instal an ssh application like putty on your system,  you may be able to connect to the workshop instance by using a browser.   This assumes that access to port 6501 is nor restricted by your companies fire wall.

Open you favorite modern browser and type HTTP//X.X.X.X:6501  (where X.X.X.X is the ip address you found in section 1.)

![http-6501](../images/intro/shellinabox-url.png){: .zoom}

Once you have connected correctly  you should receive an login in prompt similar like the screen below.

![http-connect](../images/intro/shellinabox-connect.png){: .zoom}

To connect please enter the user name **ubuntu** followed by the password found in section 1.
This should result in the welcome page of the workshop as show below:

![web login](../images/intro/shellinabox-login.png){: .zoom}

Due to additional security requirements of browser technology please read the next section:

---

## 5. Use of copy and page when connected via a browser

Unlike whe you are using regular ssh,  copy and page as is used during the workshop does require a few extra steps to complete when using a browser to connect.

!!! Note
    The reason for this is that regular paste option  cannot accept data from outside the browser, due to cross browser restrictions)

When the workshop ask you to type or copy some instructions please do the following:

*Copy the instruction as normal, but when  ready to paste it in the web terminal, choose **Paste from browser**  as show below:*

![web paste 1](../images/intro/shellinabox-paste-browser.png){: .zoom}

This will open a dialog box asking for the text to be pasted into the web terminal:

![web paste 3](../images/intro/shellinabox-example-1.png){: .zoom}

Paste the text in the text box as show, then press **OK** to complete the copy and paste process.

Unlike regular ssh connection, the web browser has a 60 second time out, and  you will be disconnected, and a **Connect** button will be show in the center of the web terminal.
Simply hit the connect button and you will be reconnected and you will be able to continue

 ![web reconnect](../images/intro/shellinabox-reconnect.png){: .zoom}

At this point you are ready to continue and [start the workshop](https://signalfx.github.io/observability-workshop/latest/smartagent/k3s/)
