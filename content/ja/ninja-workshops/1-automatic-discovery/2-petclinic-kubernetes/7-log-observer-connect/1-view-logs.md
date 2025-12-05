---
title: Viewing the Logs
linkTitle: 1. Viewing the Logs
weight: 2
---

ログを表示するには、左側のメニューで ![Logo](../images/logo-icon.png?classes=inline&height=25px) **Log Observer** をクリックします。Log Observer に入ったら、フィルターバー (filter bar) の **Index** が **splunk4rookies-workshop** に設定されていることを確認してください。**(1)**

次に、**Add Filter** をクリックし、*Fields* **(2)** オプションを使用して `deployment.environment` フィールド **(3)** を検索します。ドロップダウンリストから、あなたのワークショップインスタンスを選択し **(4)**、`=` (含める) をクリックします。これで、PetClinic アプリケーションからのログメッセージのみが表示されます。

![Log Observer sort](../../images/log-observer-sort.png)

次に、`service.name` フィールドを検索し、値 `customers-service` を選択して `=` (含める) をクリックします。これがフィルターバー **(1)** に表示されます。次に、**Run Search** ボタン **(2)** をクリックします。

![Log Observer run](../../images/log-observer-run.png)

これによりログエントリがリフレッシュされ、`customers-service` からのエントリのみが表示されるように絞り込まれます。

![Log Observer](../../images/log-observer-trace-info.png)

*"Saving pet"* で始まるエントリ **(1)** をクリックします。サイドペーンが開き、関連するトレース ID (trace ID) やスパン ID (span ID) **(2)** を含む詳細情報を確認できます。
