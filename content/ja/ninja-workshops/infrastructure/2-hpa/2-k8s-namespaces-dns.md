---
title: K8s Namespaces and DNS
linkTitle: 2. K8s Namespaces and DNS
weight: 2
---

## 1. Kubernetes における Namespace

ほとんどのお客様は、Kubernetes を実行するために何らかのプライベートまたはパブリッククラウドサービスを利用します。中央集約的に管理しやすいため、大規模な Kubernetes クラスターを少数だけ運用する選択をされることがよくあります。

Namespace は、こうした大規模な Kubernetes クラスターを仮想的なサブクラスターに整理する仕組みです。複数のチームやプロジェクトが Kubernetes クラスターを共有する場合に、それぞれのチームが自分たちのリソースだけを簡単に確認して操作できるようになるため、便利な機能です。

クラスター内では任意の数の Namespace がサポートされ、それぞれが論理的に分離されつつも、相互に通信できる能力を持っています。コンポーネントは Namespace を選択した場合、または `kubectl` に `--all-namespaces` フラグを追加した場合にのみ**表示**されます。これにより、自分の Namespace を選択することで、プロジェクトに関連するコンポーネントだけを表示できます。

ほとんどのお客様は、アプリケーションを個別の Namespace にインストールしたいと考えるでしょう。本ワークショップではそのベストプラクティスに従います。

## 2. Kubernetes における DNS と Service

Domain Name System (DNS) は、IP アドレスのようなさまざまな情報を、覚えやすい名前と紐付けるための仕組みです。リクエスト名を IP アドレスに変換する DNS システムを使用することで、エンドユーザーは目的のドメイン名に容易にアクセスできます。

ほとんどの Kubernetes クラスターには、サービスディスカバリーのための軽量なアプローチを提供するため、デフォルトで内部 DNS サービスが構成されています。Pod や Service が作成、削除、またはノード間で移動された場合でも、組み込みのサービスディスカバリーにより、アプリケーションは Kubernetes クラスター上の Service を簡単に識別して通信できます。

要するに、Kubernetes 用の DNS システムは、各 Pod および Service に対して DNS エントリを作成します。一般に、Pod は次のような DNS 解決を持ちます。

``` text
pod-name.my-namespace.pod.cluster-domain.example
```

例えば、`default` Namespace 内の Pod が `my_pod` という Pod 名を持ち、クラスターのドメイン名が `cluster.local` である場合、その Pod の DNS 名は次のようになります。

``` text
my_pod.default.pod.cluster.local
```

Service によって公開された Pod では、次のような DNS 解決が利用できます。

``` text
my_pod.service-name.my-namespace.svc.cluster-domain.example
```

詳細は次を参照してください: [**DNS for Service and Pods**](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
