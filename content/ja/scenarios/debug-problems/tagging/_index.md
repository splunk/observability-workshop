---
title: Tagging Workshop
linkTitle: Tagging Workshop
weight: 2
archetype: chapter
time: 2 minutes
authors: ["Derek Mitchell"]
description: このワークショップでは、タグを活用することで SRE がサービス間の問題を切り分ける時間を短縮し、トラブルシューティングを進めるためにどのチームを巻き込むべきかを把握し、エンジニアリングがデバッグを早期に開始するためのコンテキストを提供する方法を紹介します。

---

**Splunk Observability Cloud** には、SRE がサービス間の問題を切り分ける時間を大幅に短縮する強力な機能が備わっています。これにより、トラブルシューティングを進めるためにどのチームを巻き込むべきかを把握でき、エンジニアリングがデバッグを早期に開始するためのコンテキストを提供できます。

これらの機能を活用するには、アプリケーショントレースにタグを含める必要があります。しかし、どのタグがもっとも価値があり、それをどのように取得すればよいのでしょうか?

このワークショップでは、以下のトピックを扱います:

* **タグ** とは何か、そしてアプリケーションをオブザーバブルにするうえでなぜそれほど重要なのか。
* [**OpenTelemetry**](https://opentelemetry.io) を使用して、アプリケーションから必要なタグを取得する方法。
* **Splunk Observability Cloud** でタグをインデックス化する方法と、**Troubleshooting MetricSets** と **Monitoring MetricSets** の違い。
* **Splunk Observability Cloud** で **Tag Spotlight** および **Dynamic Service Map** 機能を使用してタグを活用し、「unknown unknowns(未知の未知)」を発見する方法。
* アラートやダッシュボードでタグを活用する方法。

このワークショップでは、これらの概念を説明するためにシンプルなマイクロサービスベースのアプリケーションを使用します。それでは始めましょう!
