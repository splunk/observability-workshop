---
title: デプロイ
weight: 3
time: 5 minutes
---

## ステップ4: プレイブックを実行する

Smart Agent をデプロイするには、プロジェクトディレクトリから以下のコマンドを実行します：

```bash
ansible-playbook -i inventory-cloud.yaml smartagent.yaml
```

インベントリファイルに別の名前を付けた場合は、`inventory-cloud.yaml` を適切なファイル名に置き換えます。

### 確認

プレイブックが正常に完了したら、ターゲットホストの1つにログインしてサービスの状態を確認することで、デプロイを検証できます：

```bash
systemctl status smartagent
```

サービスが active (running) と表示されます。
