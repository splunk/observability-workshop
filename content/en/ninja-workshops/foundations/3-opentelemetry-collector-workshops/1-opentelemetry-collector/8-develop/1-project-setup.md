---
title: OpenTelemetry Collector Development
linkTitle: 8.1 Project Setup
weight: 9
---

## Project Setup {{% badge style=primary icon=user-ninja %}}**Ninja**{{% /badge %}}

{{% notice style="note" %}}

The time to finish this section of the workshop can vary depending on experience.

A complete solution can be found [**here**](https://github.com/splunk/collector-workshop-example) in case you're stuck or want to follow
along with the instructor.

{{% /notice %}}

To get started developing the new _Jenkins CI_ receiver, we first need to set up a Golang project.
The steps to create your new Golang project is:

1. Create a new directory named `${HOME}/go/src/jenkinscireceiver` and change into it
    1. The actual directory name or location is not strict, you can choose your own development directory to make it in.
1. Initialize the golang module by going `go mod init splunk.conf/workshop/example/jenkinscireceiver`
    1. This will create a file named `go.mod` which is used to track our direct and indirect dependencies
    1. Eventually, there will be a `go.sum` which is the checksum value of the dependencies being imported.

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}Review your go.mod{{% /badge %}}" %}}

``` text
module splunk.conf/workshop/example/jenkinscireceiver

go 1.20
```

{{% /expand %}}
