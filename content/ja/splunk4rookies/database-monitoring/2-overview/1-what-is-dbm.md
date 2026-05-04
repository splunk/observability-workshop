---
title: 1. Database Monitoring とは？
weight: 1
---

**Splunk Database Monitoring** は、複数のデータベースプラットフォームにわたる詳細なパフォーマンスの可視性を、単一の統合インターフェースで提供します。SQL Server Management Studio、Oracle Enterprise Manager、`pg_stat_statements` を行き来する代わりに、すべての監視対象インスタンスを同じ画面から調査できます。

DBA として関心のある3つの情報を収集します

- **クエリパフォーマンス分析** — 待機時間、CPU 時間、読み取り行数と返却行数、およびオプティマイザが実際に選択した実行プランです。
- **サーバーメトリクス** — 基盤となるデータベースサーバーの健全性とパフォーマンスです。
- **アプリケーションの相関** — 対象のクエリの発生元であるアプリケーション、ホスト、APM トレースを特定できます。

サポートされているプラットフォームは **Microsoft SQL Server**、**Oracle Database**、および **PostgreSQL** です。

{{% notice title="Realm の可用性" style="info" %}}
Database Monitoring の利用可否は Splunk の Realm に依存し、すべてのリージョンで有効になっているわけではありません。次の演習で Database Monitoring のエントリポイントが表示されない場合は、ワークショップの組織がサポートされている Realm にあるかどうかをインストラクターに確認してください。
{{% /notice %}}

{{% notice title="演習" style="green" icon="running" %}}

製品を開く前に、ご自身の環境について少し考えてみましょう。

{{< tabs >}}
{{% tab title="質問" %}}
**お使いのデータベースプラットフォーム（SQL Server、Oracle、PostgreSQL）のうち、統合パフォーマンスビューの恩恵を最も受けるのはどれですか？またその理由は何ですか？**
{{% /tab %}}
{{% tab title="回答" %}}
**クエリレベルのパフォーマンスを確認するために、現在ベンダー固有の別ツールに依存しているプラットフォームです。** 統合ビューは、複数のデータベースエンジンを担当している場合に最も効果を発揮します。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
