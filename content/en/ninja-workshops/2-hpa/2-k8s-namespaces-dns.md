---
title: K8s Namespaces and DNS
linkTitle: 2. K8s Namespaces and DNS
weight: 2
---

## 1. Namespaces in Kubernetes

Most of our customers will make use of some kind of private or public cloud service to run Kubernetes. They often choose to have only a few large Kubernetes clusters as it is easier to manage centrally.

Namespaces are a way to organize these large Kubernetes clusters into virtual sub-clusters. This can be helpful when different teams or projects share a Kubernetes cluster as this will give them the easy ability to just see and work with their resources.

Any number of namespaces are supported within a cluster, each logically separated from others but with the ability to communicate with each other. Components are only **visible** when selecting a namespace or when adding the `--all-namespaces` flag to `kubectl` instead of allowing you to view just the components relevant to your project by selecting your namespace.

Most customers will want to install the applications into a separate namespace.  This workshop will follow that best practice.

## 2.  DNS and Services in Kubernetes

The Domain Name System (DNS) is a mechanism for linking various sorts of information with easy-to-remember names, such as IP addresses. Using a DNS system to translate request names into IP addresses makes it easy for end-users to reach their target domain name effortlessly.

Most Kubernetes clusters include an internal DNS service configured by default to offer a lightweight approach for service discovery. Even when Pods and Services are created, deleted, or shifted between nodes, built-in service discovery simplifies applications to identify and communicate with services on the Kubernetes clusters.

In short, the DNS system for Kubernetes will create a DNS entry for each Pod and Service. In general, a Pod has the following DNS resolution:

``` text
pod-name.my-namespace.pod.cluster-domain.example
```

For example, if a Pod in the `default` namespace has the Pod name `my_pod`, and the domain name for your cluster is `cluster.local`, then the Pod has a DNS name:

``` text
my_pod.default.pod.cluster.local
```

Any Pods exposed by a Service have the following DNS resolution available:

``` text
my_pod.service-name.my-namespace.svc.cluster-domain.example
```

More information can be found here: [**DNS for Service and Pods**](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
