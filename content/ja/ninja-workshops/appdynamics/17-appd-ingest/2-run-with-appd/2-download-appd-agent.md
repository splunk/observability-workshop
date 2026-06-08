---
title: 2. AppD エージェントのダウンロード
weight: 2
---

デュアルシグナルモードを使用するには、AppDynamics Java Agent（バージョン 25.6.0 以上）が必要です。インスタンスに追加しましょう。

## エージェントの解凍

インスタンスに SSH 接続し、ダウンロードスクリプトを実行すると、作成済みの `agent` ディレクトリにエージェントが展開されます

```bash
cd ~/workshop/appd
mkdir -p agent
chmod +x ./download-appd-agent.sh
./download-appd-agent.sh
```

これで `~/workshop/appd/agent/javaagent.jar` にエージェントの JAR ファイルが配置されているはずです。

## Account Access Key の確認

アプリを実行する際に [**Account Access Key**](https://se-lab.saas.appdynamics.com/controller/#/licensing/license-management-account?timeRange=last_15_minutes.BEFORE_NOW.-1.-1.15) が必要になります。AppDynamics Controller で確認できます

1. 画面右上の自分の名前をクリックします
2. **Admin** → **License** に移動します
3. 左側のサイドバーで **Account** をクリックします
4. **Account** の下にある **Name**（`se-lab`）と **Access Key** を控えます

{{% notice title="手元に控えておきましょう" style="primary" icon="lightbulb" %}}
次のステップで Account Name と Access Key を JVM プロパティとして使用します。これらはエージェントをコントローラーに認証するために必要です。
{{% /notice %}}
