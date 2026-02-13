---
title: K8s Namespaces と DNS
linkTitle: 2. K8s Namespaces と DNS
weight: 2
---

## 1. Kubernetes における Namespaces

多くのお客様は、Kubernetesを実行するために何らかのプライベートまたはパブリッククラウドサービスを利用しています。一元管理が容易であるため、少数の大規模なKubernetesクラスターのみを持つことを選択することが多いです。

Namespacesは、これらの大規模なKubernetesクラスターを仮想的なサブクラスターに整理する方法です。異なるチームやプロジェクトがKubernetesクラスターを共有する場合に役立ちます。これにより、自分のリソースだけを簡単に表示して作業できるようになります。

クラスター内では任意の数のNamespacesがサポートされており、それぞれが論理的に分離されていますが、相互に通信する機能を持っています。コンポーネントは、Namespaceを選択した場合、または `kubectl` に `--all-namespaces` フラグを追加した場合にのみ**表示**されます。Namespaceを選択することで、プロジェクトに関連するコンポーネントのみを表示できます。

ほとんどのお客様は、アプリケーションを別のNamespaceにインストールすることを望んでいます。このワークショップでは、そのベストプラクティスに従います。

## 2. Kubernetes における DNS とサービス

Domain Name System（DNS）は、IPアドレスなどのさまざまな情報を覚えやすい名前にリンクするメカニズムです。DNSシステムを使用してリクエスト名をIPアドレスに変換することで、エンドユーザーは目的のドメイン名に簡単にアクセスできます。

ほとんどのKubernetesクラスターには、サービスディスカバリのための軽量なアプローチを提供するデフォルトで設定された内部DNSサービスが含まれています。Podやサービスが作成、削除、またはノード間で移動された場合でも、組み込みのサービスディスカバリにより、アプリケーションはKubernetesクラスター上のサービスを識別して通信することが簡素化されます。

簡単に言えば、KubernetesのDNSシステムは、各Podとサービスに対してDNSエントリを作成します。一般的に、Podは以下のDNS解決を持ちます:

``` text
pod-name.my-namespace.pod.cluster-domain.example
```

例えば、`default` Namespace内のPodが `my_pod` というPod名を持ち、クラスターのドメイン名が `cluster.local` の場合、Podは以下のDNS名を持ちます:

``` text
my_pod.default.pod.cluster.local
```

サービスによって公開されるPodは、以下のDNS解決が利用可能です:

``` text
my_pod.service-name.my-namespace.svc.cluster-domain.example
```

詳細については、こちらを参照してください: [**DNS for Service and Pods**](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
