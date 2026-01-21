---
title: Machine Agent のデプロイ
time: 5 minutes
weight: 3
description: Server Agent を手動でインストールします。
---

この演習では、以下のアクションを実行します：

1. Machine Agent をインストールするスクリプトを実行する
2. Machine Agent を設定する
3. Machine Agent を起動する

{{% notice title="注意" style="orange"  %}}
スクリプトを使用して Machine Agent を EC2 インスタンスにダウンロードします。通常は [https://accounts.appdynamics.com/](https://accounts.appdynamics.com/) にログインして Machine Agent をダウンロードする必要がありますが、アクセス制限の可能性があるため、ポータルから直接ダウンロードするスクリプトを使用します。AppDynamics ポータルにアクセスでき、Machine Agent をダウンロードしたい場合は、以下のステップに従ってダウンロードし、APM ラボの Install Agent セクションで使用したステップを参照して VM に SCP してください。

1. [AppDynamics Portal](https://accounts.appdynamics.com/) にログインします
2. 左側のメニューで **Downloads** をクリックします
3. **Type** で **Machine Agent** を選択します
4. **Operating System** で **Linux** を選択します
5. **Machine Agent Bundle - 64-bit linux (zip)** を見つけて **Download** ボタンをクリックします
6. Install Agent セクションのステップに従って、ダウンロードしたファイルを EC2 インスタンスに SCP します
7. zip ファイルを /opt/appdynamics/machineagent ディレクトリに解凍し、このラボの設定セクションに進みます
{{% /notice %}}

## インストールスクリプトの実行

以下のコマンドを使用して、スクリプトが配置されているディレクトリに移動します。スクリプトは Machine Agent をダウンロードして解凍します。

```bash
cd /opt/appdynamics/lab-artifacts/machineagent/
```

以下のコマンドを使用してインストールスクリプトを実行します。

```bash
chmod +x install_machineagent.sh
./install_machineagent.sh
```

以下の画像のような出力が表示されるはずです。

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

Machine Agent の "controller-info.xml" ファイルを編集し、Java Agent 設定ファイルから取得した以下のプロパティの値を挿入します。

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

## Server Visibility Agent の起動

以下のコマンドを使用して、Server Visibility Agent を起動し、起動したことを確認します。

```bash
cd /opt/appdynamics/machineagent/bin
nohup ./machine-agent &
ps -ef | grep machine
```

以下の画像のような出力が表示されるはずです。

![Example Output](images/run-machine-agent.png)
