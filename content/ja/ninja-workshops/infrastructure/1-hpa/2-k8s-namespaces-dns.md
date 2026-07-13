---
title: K8s NamespaceとDNS
linkTitle: 2. K8s NamespaceとDNS
weight: 2
---

## 1. KubernetesのNamespace

多くのお客様は、Kubernetesを実行するために何らかのプライベートまたはパブリッククラウドサービスを利用しています。一元管理が容易なため、少数の大規模なKubernetesクラスターのみを運用することが多いです。

Namespaceは、これらの大規模なKubernetesクラスターを仮想的なサブクラスターに整理する方法です。異なるチームやプロジェクトがKubernetesクラスターを共有する場合、自分たちのリソースだけを簡単に表示・操作できるため便利です。

クラスター内では任意の数のNamespaceがサポートされており、それぞれ論理的に分離されていますが、相互に通信する機能を持っています。コンポーネントは、Namespaceを選択した場合、または `kubectl` に `--all-namespaces` フラグを追加した場合にのみ **表示** されます。Namespaceを選択することで、プロジェクトに関連するコンポーネントだけを表示できます。

ほとんどのお客様は、アプリケーションを別のNamespaceにインストールすることを望みます。このワークショップではそのベストプラクティスに従います。

## 2. KubernetesにおけるDNSとService

Domain Name System（DNS）は、IPアドレスなどのさまざまな情報を覚えやすい名前に紐付けるメカニズムです。DNSシステムを使用してリクエスト名をIPアドレスに変換することで、エンドユーザーはターゲットのドメイン名に容易に到達できます。

ほとんどのKubernetesクラスターには、サービスディスカバリのための軽量なアプローチを提供するように、デフォルトで設定された内部DNSサービスが含まれています。PodやServiceが作成、削除、またはノード間で移動された場合でも、組み込みのサービスディスカバリにより、アプリケーションはKubernetesクラスター上のサービスを容易に識別し通信できます。

つまり、KubernetesのDNSシステムは、各PodとServiceにDNSエントリを作成します。一般的に、Podは次のようなDNS名前解決を持ちます。

``` text
pod-name.my-namespace.pod.cluster-domain.example
```

例えば、`default` Namespace内のPodのPod名が `my_pod` で、クラスターのドメイン名が `cluster.local` の場合、そのPodのDNS名は次のようになります。

``` text
my_pod.default.pod.cluster.local
```

Serviceによって公開されているPodは、次のようなDNS名前解決が利用可能です。

``` text
my_pod.service-name.my-namespace.svc.cluster-domain.example
```

詳細はこちらを参照してください: [**DNS for Service and Pods**](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
