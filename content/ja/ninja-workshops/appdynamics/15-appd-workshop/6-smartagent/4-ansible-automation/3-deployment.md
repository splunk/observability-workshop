---
title: デプロイメント
weight: 3
time: 5 minutes
---

## ステップ 4: Playbook の実行

Smart Agent をデプロイするには、プロジェクトディレクトリから次のコマンドを実行します

```bash
ansible-playbook -i inventory-cloud.yaml smartagent.yaml
```

インベントリファイルに別の名前を付けた場合は、`inventory-cloud.yaml` をご自身の設定に合った適切なインベントリファイル名に置き換えてください。

### 検証

Playbook が正常に完了したら、ターゲットホストの1つにログインしてサービスのステータスを確認することで、デプロイメントを検証できます

```bash
systemctl status smartagent
```

サービスが active (running) と表示されていれば正常です。
