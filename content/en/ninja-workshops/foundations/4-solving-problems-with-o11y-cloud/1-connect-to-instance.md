---
title: Connect to EC2 Instance
linkTitle: 1. Connect to EC2 Instance
weight: 1
time: 5 minutes
---

## Connect to your EC2 Instance

We’ve prepared an Ubuntu Linux instance in AWS/EC2 for each attendee. To connect to your EC2 instance:

* Copy the `Web SSH` URL from your instance information in Splunk Show.
* Paste the URL in your browser.
* When prompted, input `splunk` as the user name.
* For the password, copy the `SSH Password` value from Splunk Show.

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

See [**An introduction to the vi editor**](https://www.redhat.com/en/blog/introduction-vi-editor) for a comprehensive introduction to `vi`.

If you'd prefer using another editor, you can use `nano` instead:

```bash
nano <filename> 
```
