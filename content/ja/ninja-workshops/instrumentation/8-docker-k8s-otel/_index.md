---
title: Hands-On OpenTelemetry, Docker, and K8s
linkTitle: Hands-On OpenTelemetry, Docker, and K8s
weight: 8
archetype: chapter
time: 60 minutes
authors: ["Derek Mitchell"]
description: .NETアプリケーションをOpenTelemetryで計装し、Dockerでコンテナ化、Kubernetesにデプロイして、Helm経由でOTel Collectorを構成します。
draft: false
hidden: false
aliases:
  - /ninja-workshops/8-docker-k8s-otel/
---

このワークショップでは、以下の内容をハンズオン形式で体験します。

* LinuxおよびKubernetes環境において、Collectorのデプロイと、Splunk distribution of OpenTelemetry .NETを使った.NETアプリケーションの計装を実践します。
* .NETアプリケーションを"dockerize"してDockerで実行し、その後Splunk OpenTelemetryによる計装を追加する流れを実践します。
* HelmでSplunk distro of the collectorをK8s環境にデプロイします。その後、Collectorの構成をカスタマイズし、発生した問題のトラブルシューティングを行います。

このワークショップでは、これらの概念を解説するためにシンプルな.NETアプリケーションを使用します。それでは始めましょう！
