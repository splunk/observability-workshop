---
title: Connect to EC2 Instance
linkTitle: 1. Connect to EC2 Instance
weight: 1
time: 5 minutes
---

## Connect to your EC2 Instance

We’ve prepared an Ubuntu Linux instance in AWS/EC2 for each attendee. 

Using the IP address and password provided by your instructor, connect to your EC2 instance
using one of the methods below: 

* Mac OS / Linux 
  * ssh splunk@IP address 
* Windows 10+
  * Use the OpenSSH client
* Earlier versions of Windows
  * Use Putty 

## Editing Files 

We'll use `vi` to edit files during the workshop.  Here's a quick primer. 

To open a file for editing: 

```bash
vi <filename> 
```

* To edit the file, click `i` to switch to **Insert mode** and begin entering text as normal. Use `Esc` to return to **Command mode**. 
* To save your changes without exiting the editor, enter `Esc` to return to command mode then enter `:w`. 
* To exit the editor without saving changes, enter `Esc` to return to command mode then enter `:q!`. 
* To save your changes and exist the editor, enter `Esc` to return to command mode then enter `:wq`. 

See [An introduction to the vi editor](https://www.redhat.com/en/blog/introduction-vi-editor) for a comprehensive introduction to `vi`. 

If you'd prefer using another editor, you can use `nano` instead: 

```bash
nano <filename> 
```


