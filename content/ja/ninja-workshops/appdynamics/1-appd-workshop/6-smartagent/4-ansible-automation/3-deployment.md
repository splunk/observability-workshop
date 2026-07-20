---
title: Deployment
weight: 3
time: 5 minutes
---

## ステップ4: Playbookの実行

Smart Agentをデプロイするには、プロジェクトディレクトリから以下のコマンドを実行します。

```bash
ansible-playbook -i inventory-cloud.yaml smartagent.yaml
```

ファイル名を変更している場合は、`inventory-cloud.yaml` を適切なインベントリファイルに置き換えてください。

### 検証

Playbookが正常に完了したら、ターゲットホストの1つにログインしてサービスのステータスを確認することで、デプロイを検証できます。

```bash
systemctl status smartagent
```

サービスがactive (running)と表示されます。
