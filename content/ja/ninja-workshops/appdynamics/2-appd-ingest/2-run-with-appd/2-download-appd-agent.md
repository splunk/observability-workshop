---
title: 2. AppDエージェントのダウンロード
weight: 2
---

デュアルシグナルモードを使用するには、AppDynamics Javaエージェント（バージョン25.6.0以上）が必要です。インスタンスに追加します。

## エージェントの解凍

インスタンスにSSH接続し、ダウンロードスクリプトを実行すると、作成した `agent` ディレクトリにエージェントが展開されます。

```bash
cd ~/workshop/appd
mkdir -p agent
chmod +x ./download-appd-agent.sh
./download-appd-agent.sh
```

`~/workshop/appd/agent/javaagent.jar` にエージェントJARが配置されます。

## Account Access Keyの確認

アプリケーションを実行する際に [**Account Access Key**](https://se-lab.saas.appdynamics.com/controller/#/licensing/license-management-account?timeRange=last_15_minutes.BEFORE_NOW.-1.-1.15) が必要になります。AppDynamics Controllerで確認できます。

1. 画面右上の名前をクリックします
2. **Admin** → **License** に移動します
3. 左サイドバーの **Account** をクリックします
4. **Account** の下にある **Name**（`se-lab`）と **Access Key** を確認します

{{% notice title="手元に控えておきましょう" style="primary" icon="lightbulb" %}}
次のステップでAccount NameとAccess KeyをJVMプロパティとして使用します。これらはエージェントをControllerに認証するために必要です。
{{% /notice %}}
