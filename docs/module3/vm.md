### Lab Summary

1. Deploy SignalFx Smart Agent via install script on a VM
1. Confirm the Smart Agent is working and sending data

### 1. Deploy SignalFx Smart Agent via install script on a VM

SignalFx maintains a shell script to install on supported distributions:

```
curl -sSL https://dl.signalfx.com/signalfx-agent.sh > /tmp/signalfx-agent.sh
sudo sh /tmp/signalfx-agent.sh --realm $REALM $ACCESS_TOKEN
```

Once the installation is complete, validate the agent is running.

Input:

```text
signalfx-agent status
```

Output:

```text
SignalFx Agent version:           5.0.4
Agent uptime:                     9m34s
Observers active:                 k8s-api
Active Monitors:                  13
Configured Monitors:              13
Discovered Endpoint Count:        15
Bad Monitor Config:               None
Global Dimensions:                {kubernetes_cluster:    AS-SFX-WORKSHOP, host: as-k3s, kubernetes_node_uid:    a58cf908-0536-478d-aa63-8ba381ef2c33}
GlobalSpanTags:                   map[]
Datapoints sent (last minute):    726
Datapoints failed (last minute):  0
Datapoints overwritten (total):   0
Events Sent (last minute):        6
Trace Spans Sent (last minute):   0
Trace Spans overwritten (total):  0
Kubernetes Leader Node:           as-k3s

Additional status commands:

signalfx-agent status config - show resolved config in use    by agent
signalfx-agent status endpoints - show discovered endpoints
signalfx-agent status monitors - show active monitors
signalfx-agent status all - show everything
```

### 2. Confirm the Smart Agent is working and sending data

In the SignalFX UI, go to Infrastructure, Hosts and make sure you see your multipass instance in the list of hosts. You can also set a filter for just your instance.

### 3. Stop the agent on the VM

In the next module we are going to roll out the agent on the Kubernetes cluster. Before doing that, stop the VM agent with

Input:

```
signalfx-agent stop
```

Output:

