---
title: Setup Users
linkTitle: 6. Setup Users
weight: 6
time: 2 minutes
---

In this section, we'll create users for each workshop participant, with a namespace and resource 
quota for each. 

## Create Users

``` bash
cd user-setup
./create-users.sh
```

## Create User Namespaces and Resource Quotas

``` bash
./create-namespaces.sh
```