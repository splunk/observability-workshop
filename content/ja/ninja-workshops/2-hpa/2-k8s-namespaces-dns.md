---
title: K8s Namespaces と DNS
linkTitle: 2. K8s Namespaces と DNS
weight: 2
---

## 1. Kubernetes における Namespaces

多くのお客様は、Kubernetes を実行するために何らかのプライベートまたはパブリッククラウドサービスを利用しています。一元管理が容易であるため、少数の大規模な Kubernetes クラスターのみを持つことを選択することが多いです。

Namespaces は、これらの大規模な Kubernetes クラスターを仮想的なサブクラスターに整理する方法です。異なるチームやプロジェクトが Kubernetes クラスターを共有する場合に役立ちます。これにより、自分のリソースだけを簡単に表示して作業できるようになります。

クラスター内では任意の数の Namespaces がサポートされており、それぞれが論理的に分離されていますが、相互に通信する機能を持っています。コンポーネントは、Namespace を選択した場合、または `kubectl` に `--all-namespaces` フラグを追加した場合にのみ**表示**されます。Namespace を選択することで、プロジェクトに関連するコンポーネントのみを表示できます。

ほとんどのお客様は、アプリケーションを別の Namespace にインストールすることを望んでいます。このワークショップでは、そのベストプラクティスに従います。

## 2. Kubernetes における DNS とサービス

Domain Name System（DNS）は、IP アドレスなどのさまざまな情報を覚えやすい名前にリンクするメカニズムです。DNS システムを使用してリクエスト名を IP アドレスに変換することで、エンドユーザーは目的のドメイン名に簡単にアクセスできます。

ほとんどの Kubernetes クラスターには、サービスディスカバリのための軽量なアプローチを提供するデフォルトで設定された内部 DNS サービスが含まれています。Pod やサービスが作成、削除、またはノード間で移動された場合でも、組み込みのサービスディスカバリにより、アプリケーションは Kubernetes クラスター上のサービスを識別して通信することが簡素化されます。

簡単に言えば、Kubernetes の DNS システムは、各 Pod とサービスに対して DNS エントリを作成します。一般的に、Pod は以下の DNS 解決を持ちます:

``` text
pod-name.my-namespace.pod.cluster-domain.example
```

例えば、`default` Namespace 内の Pod が `my_pod` という Pod 名を持ち、クラスターのドメイン名が `cluster.local` の場合、Pod は以下の DNS 名を持ちます:

``` text
my_pod.default.pod.cluster.local
```

サービスによって公開される Pod は、以下の DNS 解決が利用可能です:

``` text
my_pod.service-name.my-namespace.svc.cluster-domain.example
```

詳細については、こちらを参照してください: [**DNS for Service and Pods**](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
