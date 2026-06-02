---
title: ログの表示
linkTitle: 1. ログの表示
weight: 2
---

ログを確認するには、左側のメニューから ![Logo](../images/logo-icon.png?classes=inline&height=25px)  **Log Observer** をクリックします。Log Observer に入ったら、フィルターバーの **Index** が **splunk4rookies-workshop** に設定されていることを確認してください。**(1)**

次に、**Add Filter** をクリックし、*Fields* **(2)** オプションを使ってフィールド `deployment.environment` **(3)** を検索します。続いて、ドロップダウンリストから自分のワークショップインスタンスを選択し **(4)**、`=`（含める）をクリックします。これで、PetClinic アプリケーションからのログメッセージのみが表示されるようになります。

![Log Observer sort](../../images/log-observer-sort.png)

次に、フィールド `service.name` を検索し、値 `customers-service` を選択して `=`（含める）をクリックします。これがフィルターバーに表示されるはずです **(1)**。続いて **Run Search** ボタン **(2)** をクリックします。

![Log Observer run](../../images/log-observer-run.png)

これによりログエントリが更新され、`customers-service` のみのエントリに絞り込まれて表示されます。

![Log Observer](../../images/log-observer-trace-info.png)

*"Saving pet"* で始まるエントリをクリックします **(1)**。サイドペインが開き、関連するトレース ID およびスパン ID を含む詳細情報を確認できます **(2)**。
