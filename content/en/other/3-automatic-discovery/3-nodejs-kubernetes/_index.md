---
title: NodeJS Zero-Config Workshop
weight: 3
description: A workshop using Zero Configuration Auto-Instrumentation for NodeJS.
authors: ["Robert Castley"]
time: 30 minutes
---

The goal is to walk through the basic steps to configure the following components of the **Splunk Observability Cloud** platform:

* Splunk Infrastructure Monitoring (IM)
* Splunk Zero Configuration Auto Instrumentation for NodeJS (APM)
  * AlwaysOn Profiling
* Splunk Log Observer (LO)

We will deploy the OpenTelemetry Astronomy Shop application in Kubernetes, which contains two NodeJS services (**Frontend** & **Payment Service**). Once the application and the OpenTelemetry Connector are up and running, we will start seeing metrics, traces and logs via the **Zero Configuration Auto Instrumentation** for NodeJS that will be used by the **Splunk Observability Cloud** platform to provide insights into the application.

{{% notice title="Prerequisites" style="primary" icon="info" %}}

* Outbound SSH access to port `2222`.
* Outbound HTTP access to port `8083`.
* Familiarity with the `bash` shell and `vi/vim` editor.

{{% /notice %}}

Next, we will deploy the **OpenTelemetry Demo**.

{{< mermaid >}}
graph TD
subgraph Service Diagram
accountingservice(Accounting Service):::golang
adservice(Ad Service):::java
cache[(Cache)]
cartservice(Cart Service):::dotnet
checkoutservice(Checkout Service):::golang
currencyservice(Currency Service):::cpp
emailservice(Email Service):::ruby
frauddetectionservice(Fraud Detection Service):::kotlin
frontend(Frontend):::typescript
frontendproxy(Frontend Proxy):::cpp
loadgenerator([Load Generator]):::python
paymentservice(Payment Service):::javascript
productcatalogservice(Product Catalog Service):::golang
quoteservice(Quote Service):::php
recommendationservice(Recommendation Service):::python
shippingservice(Shipping Service):::rust
featureflagservice(Feature Flag Service):::erlang
featureflagstore[(Feature Flag Store)]
queue[(queue)]
Internet -->|HTTP| frontendproxy
frontendproxy -->|HTTP| frontend
frontendproxy -->|HTTP| featureflagservice
loadgenerator -->|HTTP| frontendproxy
accountingservice -->|TCP| queue
cartservice --->|gRPC| featureflagservice
checkoutservice --->|gRPC| cartservice --> cache
checkoutservice --->|gRPC| productcatalogservice
checkoutservice --->|gRPC| currencyservice
checkoutservice --->|HTTP| emailservice
checkoutservice --->|gRPC| paymentservice
checkoutservice -->|gRPC| shippingservice
checkoutservice --->|TCP| queue
frontend -->|gRPC| adservice
frontend -->|gRPC| cartservice
frontend -->|gRPC| productcatalogservice
frontend -->|gRPC| checkoutservice
frontend -->|gRPC| currencyservice
frontend -->|gRPC| recommendationservice -->|gRPC| productcatalogservice
frontend -->|gRPC| shippingservice -->|HTTP| quoteservice
frauddetectionservice -->|TCP| queue
adservice --->|gRPC| featureflagservice
productcatalogservice -->|gRPC| featureflagservice
recommendationservice -->|gRPC| featureflagservice
shippingservice -->|gRPC| featureflagservice
featureflagservice --> featureflagstore
end

classDef dotnet fill:#178600,color:white;
classDef cpp fill:#f34b7d,color:white;
classDef erlang fill:#b83998,color:white;
classDef golang fill:#00add8,color:black;
classDef java fill:#b07219,color:white;
classDef javascript fill:#f1e05a,color:black;
classDef kotlin fill:#560ba1,color:white;
classDef php fill:#4f5d95,color:white;
classDef python fill:#3572A5,color:white;
classDef ruby fill:#701516,color:white;
classDef rust fill:#dea584,color:black;
classDef typescript fill:#e98516,color:black;
{{< /mermaid >}}

{{< mermaid >}}
graph TD
subgraph Service Legend
  dotnetsvc(.NET):::dotnet
  cppsvc(C++):::cpp
  erlangsvc(Erlang/Elixir):::erlang
  golangsvc(Go):::golang
  javasvc(Java):::java
  javascriptsvc(JavaScript):::javascript
  kotlinsvc(Kotlin):::kotlin
  phpsvc(PHP):::php
  pythonsvc(Python):::python
  rubysvc(Ruby):::ruby
  rustsvc(Rust):::rust
  typescriptsvc(TypeScript):::typescript
end

classDef dotnet fill:#178600,color:white;
classDef cpp fill:#f34b7d,color:white;
classDef erlang fill:#b83998,color:white;
classDef golang fill:#00add8,color:black;
classDef java fill:#b07219,color:white;
classDef javascript fill:#f1e05a,color:black;
classDef kotlin fill:#560ba1,color:white;
classDef php fill:#4f5d95,color:white;
classDef python fill:#3572A5,color:white;
classDef ruby fill:#701516,color:white;
classDef rust fill:#dea584,color:black;
classDef typescript fill:#e98516,color:black;
{{< /mermaid >}}
