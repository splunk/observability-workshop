---
hide:
  - navigation # Hide navigation
  - toc        # Hide table of contents
---
# Multipassのインスタンスを起動する

---

## 1. 前提条件

お使いの OS に合わせて [Multipass](https://multipass.run/){: target=_blank}[^1] をインストールしてください。最低でもバージョン `1.6.0` を使用していることを確認してください。

Mac の場合は [Homebrew](https://brew.sh/){: target=_blank} でインストールすることもできます。

---

## 2. cloud-init YAMLのダウンロード

=== "Linux/Mac OS"

    ```text
    WSVERSION=2.32
    mkdir cloud-init
    curl -s \
    https://raw.githubusercontent.com/signalfx/observability-workshop/v$WSVERSION/cloud-init/k3s.yaml \
    -o cloud-init/k3s.yaml
    export INSTANCE=$(cat /dev/urandom | base64 | tr -dc 'a-z' | head -c4)
    ```

=== "Windows"

    !!! info
        このURL <https://github.com/signalfx/observability-workshop/archive/v2.32.zip> をから、zipファイルをダウンロードしてください。

        ダウンロードしたファイルを解凍し、ファイル名を「workshop」に変更します。次に、コマンドプロンプトから、そのディレクトリに入り、次のコマンドを実行してください。

    ```
    $INSTANCE = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".tochararray() | sort {Get-Random})[0..3] -join ''
    ```

---

## 3. Multipass インスタンスの起動

このセクションでは、ワークショップで使用するKubernetes（K3s）環境を実行するMultipassインスタンスを構築し、起動します。

=== "シェルコマンド"

    ```text
    multipass launch \
    --name ${INSTANCE} \
    --cloud-init cloud-init/k3s.yaml \
    --cpus 4 \
    --mem 4Gb \
    --disk 32Gb
    ```

    インスタンスが正常に作成されたら（数分かかることもあります）、シェルを起動します。

    === "シェルコマンド"

        ```text
        multipass shell ${INSTANCE}
        ```

    === "出力"
    
        ```text
        ███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗  
        ██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗ 
        ███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗
        ╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝
        ███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝ 
        ╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝  

        To run a command as administrator (user "root"), use "sudo <command>".
        See "man sudo_root" for details

        Waiting for cloud-init status...
        Your instance is ready!

        ubuntu@vmpe:~$
        ```

    インスタンスに Splunk のロゴが表示されたら、Multipass インスタンスの準備が完了したことになり、この時点で続行して [ワークショップを開始](../../otel/k3s/) することができます。

[^1]: Multipass は、Linux、Windows、macOS 用の軽量なVMマネージャーです。1つのコマンドで新鮮な Ubuntu 環境を手に入れたい開発者のために設計されています。Linux では KVM、Windows では Hyper-V、macOS では HyperKit を使用し、最小限のオーバーヘッドでVMを実行します。また、Windows および macOS では VirtualBox を使用することもできます。Multipass はあなたに代わってイメージを取得し、常に最新の状態に保ちます。
