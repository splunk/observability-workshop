---
title: Summary
linkTitle: 7. Summary
weight: 7
---

## Before you Go

Please kindly clean up your lab using the following command:

{{< tabs >}}
{{% tab title="Remove Functions" %}}

``` bash
sls remove
```

{{% /tab %}}
{{< /tabs >}}

## Conclusion

Congratuations on finishing the lab. You have seen how we complement auto-instrumentation with manual steps to force `Producer` function's context to be sent to `Consumer` function via a Record put on a Kinesis stream. This allowed us to build the expected Distributed Trace.

![7-conclusion-1-architecture](../images/7-conclusion-1-architecture.png)

You can now build out a Trace manually by linking two different functions together. This is very powerful when your auto-instrumenation, or third-party systems, do not support context propagation out of the box.
