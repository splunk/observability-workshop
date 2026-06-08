---
title: Machine Agent のデプロイ
time: 5 minutes
weight: 3
description: サーバーエージェントを手動でインストールします。
---

この演習では、以下のアクションを実行します

1. Machine agent をインストールするスクリプトを実行する
2. Machine agent を設定する
3. Machine agent を起動する

{{% notice title="Note" style="orange"  %}}
スクリプトを使用して Machine agent を EC2 インスタンスにダウンロードします。通常は [https://accounts.appdynamics.com/](https://accounts.appdynamics.com/) にログインして Machine agent をダウンロードする必要がありますが、アクセス制限の可能性があるため、ポータルから直接ダウンロードするスクリプトを使用します。AppDynamics ポータルにアクセスでき、Machine agent をダウンロードしたい場合は、以下の手順に従ってダウンロードし、APM ラボの Install Agent セクションの手順を参考にして VM に SCP で転送してください。

1. [AppDynamics Portal](https://accounts.appdynamics.com/) にログインします
2. 左側のメニューで **Downloads** をクリックします
3. **Type** で **Machine Agent** を選択します
4. **Operating System** で **Linux** を選択します
5. **Machine Agent Bundle - 64-bit linux (zip)** を見つけて **Download** ボタンをクリックします
6. Install Agent セクションの手順に従って、ダウンロードしたファイルを EC2 インスタンスに SCP で転送します
7. zip ファイルを /opt/appdynamics/machineagent ディレクトリに展開し、このラボの設定セクションに進みます
{{% /notice %}}

## インストールスクリプトの実行

以下のコマンドを使用して、スクリプトが配置されているディレクトリに移動します。このスクリプトは Machine agent をダウンロードして展開します。

```bash
cd /opt/appdynamics/lab-artifacts/machineagent/
```

以下のコマンドを使用してインストールスクリプトを実行します。

```bash
chmod +x install_machineagent.sh
./install_machineagent.sh
```

以下の画像のような出力が表示されます。

![Install Output](images/install-script-output.png)

## Server Agent の設定

Java Agent の "controller-info.xml" から以下の設定プロパティ値を取得し、次のステップで使用できるようにしておきます。

```bash
cat /opt/appdynamics/javaagent/conf/controller-info.xml
```

- controller-host
- controller-port
- controller-ssl-enabled
- account-name
- account-access-key

Machine Agent の "controller-info.xml" ファイルを編集し、Java Agent の設定ファイルから取得した以下のプロパティの値を挿入します。

- controller-host
- controller-port
- controller-ssl-enabled
- account-name
- account-access-key

"sim-enabled" プロパティを true に設定してファイルを保存する必要があります。ファイルは以下の画像のようになります。

```bash
cd /opt/appdynamics/machineagent/conf
nano controller-info.xml
```

![Example Config](images/controller-example.png)

## Server Visibility agent の起動

以下のコマンドを使用して Server Visibility agent を起動し、起動したことを確認します。

```bash
cd /opt/appdynamics/machineagent/bin
nohup ./machine-agent &
ps -ef | grep machine
```

以下の画像のような出力が表示されます。

![Example Output](images/run-machine-agent.png)
