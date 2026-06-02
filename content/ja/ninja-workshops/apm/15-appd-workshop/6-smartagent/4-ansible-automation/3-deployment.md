---
title: デプロイ
weight: 3
time: 5 minutes
---

## ステップ4: Playbook の実行

Smart Agent をデプロイするには、プロジェクトディレクトリから次のコマンドを実行します。

```bash
ansible-playbook -i inventory-cloud.yaml smartagent.yaml
```

別の名前で作成している場合は、 `inventory-cloud.yaml` をご利用の環境に合った inventory ファイルに置き換えてください。

### 検証

Playbook が正常に完了したら、対象ホストのいずれかにログインしてサービスの状態を確認することで、デプロイを検証できます。

```bash
systemctl status smartagent
```

サービスが active (running) になっていることが確認できるはずです。
