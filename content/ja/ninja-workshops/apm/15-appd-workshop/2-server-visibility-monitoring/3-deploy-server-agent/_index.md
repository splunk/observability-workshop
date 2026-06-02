---
title: Machine Agent のデプロイ
time: 5 minutes
weight: 3
description: サーバーエージェントを手動でインストールします。
---

この演習では、以下の作業を行います。

1. Machine Agent をインストールするスクリプトを実行する
2. Machine Agent を構成する
3. Machine Agent を起動する

{{% notice title="Note" style="orange"  %}}
スクリプトを使用して、EC2 インスタンスに Machine Agent をダウンロードします。通常は [https://accounts.appdynamics.com/](https://accounts.appdynamics.com/) にログインして Machine Agent をダウンロードする必要がありますが、アクセス制限の可能性があるため、ポータルから直接ダウンロードするスクリプトを使用します。AppDynamics ポータルへのアクセス権があり、Machine Agent をダウンロードしたい場合は、以下の手順でダウンロードし、APM ラボの Install Agent セクションで使用した手順を参照して VM に SCP で転送できます。

1. [AppDynamics Portal](https://accounts.appdynamics.com/) にログインします
2. 左側のメニューで **Downloads** をクリックします
3. **Type** で **Machine Agent** を選択します
4. **Operating System** で **Linux** を選択します
5. **Machine Agent Bundle - 64-bit linux (zip)** を見つけて **Download** ボタンをクリックします
6. Install Agent セクションの手順に従って、ダウンロードしたファイルを EC2 インスタンスに SCP で転送します
7. zip ファイルを /opt/appdynamics/machineagent ディレクトリに展開し、このラボの構成セクションに進みます
{{% /notice %}}

## インストールスクリプトの実行

以下のコマンドを使用して、スクリプトが配置されているディレクトリに移動します。スクリプトは Machine Agent をダウンロードして展開します。

```bash
cd /opt/appdynamics/lab-artifacts/machineagent/
```

以下のコマンドを使用して、インストールスクリプトを実行します。

```bash
chmod +x install_machineagent.sh
./install_machineagent.sh
```

以下の画像のような出力が表示されるはずです。

![Install Output](images/install-script-output.png)

## サーバーエージェントの構成

以下に記載されている構成プロパティの値を Java Agent の "controller-info.xml" から取得し、次の手順で使用できるように準備しておきます。

```bash
cat /opt/appdynamics/javaagent/conf/controller-info.xml
```

- controller-host
- controller-port
- controller-ssl-enabled
- account-name
- account-access-key

Machine Agent の "controller-info.xml" ファイルを編集し、Java Agent の構成ファイルから取得した以下のプロパティの値を入力します。

- controller-host
- controller-port
- controller-ssl-enabled
- account-name
- account-access-key

"sim-enabled" プロパティを true に設定してからファイルを保存する必要があります。以下の画像のようになるはずです。

```bash
cd /opt/appdynamics/machineagent/conf
nano controller-info.xml
```

![Example Config](images/controller-example.png)

## Server Visibility エージェントの起動

以下のコマンドを使用して、Server Visibility エージェントを起動し、起動したことを確認します。

```bash
cd /opt/appdynamics/machineagent/bin
nohup ./machine-agent &
ps -ef | grep machine
```

以下の画像のような出力が表示されるはずです。

![Example Output](images/run-machine-agent.png)
