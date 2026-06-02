---
title: NVIDIA NIM Operator のデプロイ
linkTitle: 4. NVIDIA NIM Operator のデプロイ
weight: 4
time: 20 minutes
---

**NVIDIA GPU Operator** は、Kubernetes クラスター内で GPU をプロビジョニングするために必要な、すべての NVIDIA ソフトウェアコンポーネントのデプロイ、設定、管理を自動化する Kubernetes Operator です。

**NVIDIA NIM Operator** は、本ワークショップで先ほど作成した OpenShift クラスターのような Kubernetes 環境に LLM をデプロイするために使用します。

このワークショップのセクションでは、OpenShift クラスターに NVIDIA GPU Operator と NIM Operator の両方をデプロイするために必要な手順を順を追って説明します。

## NVIDIA NGC アカウントの作成

LLM をダウンロードして NVIDIA NIM Operator を使用してデプロイするには、NVIDIA GPU CLOUD (NGC) アカウントが必要です。アカウントは [こちら](https://ngc.nvidia.com/signin) から登録できます。

## NVIDIA Developer Program への登録

[NVIDIA Developer Program](https://developer.nvidia.com/) に登録することで、ワークショップの後半で LLM のデプロイに使用する NVIDIA NIM へのアクセスが可能になります。

NGC の NVIDIA サブスクリプション一覧に `NVIDIA Developer Program` が表示されていることを確認してください。

![NVIDIA Subscriptions](../../images/NVIDIA-Subscriptions.png)

## NGC API キーの生成

NGC ウェブサイトにログインしたら、画面右上のユーザーアカウントアイコンをクリックし、**Setup** を選択します。

次に **Generate API Key** をクリックし、指示に従ってください。キーが **NGC Catalog** および **Secrets Manager** サービスに関連付けられていることを確認してください。

生成されたキーは、ワークショップの後半で使用するため、安全な場所に保存しておきます。

NGC API キーの生成に関する詳細は、[NVIDIA ドキュメント](https://docs.nvidia.com/ngc/gpu-cloud/ngc-user-guide/index.html#generating-api-key) を参照してください。

## Node Feature Discovery Operator のインストール

このセクションの手順は、[Installing the NFD Operator using the CLI](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/specialized_hardware_and_driver_enablement/psap-node-feature-discovery-operator#install-operator-cli_psap-node-feature-discovery-operator) に基づいています。

次のスクリプトを実行して、Node Feature Discovery Operator をインストールします。

``` bash
cd nvidia
./install-nfd-operator.sh
```

Operator のデプロイが成功したことを確認するには、次のコマンドを実行します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
oc get pods
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                                      READY   STATUS    RESTARTS   AGE
nfd-controller-manager-7f86ccfb58-vgr4x   2/2     Running   0          10m
```

{{% /tab %}}
{{< /tabs >}}

## NodeFeatureDiscovery CR の作成

このセクションの手順は、[Creating a NodeFeatureDiscovery CR by using the CLI](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/specialized_hardware_and_driver_enablement/psap-node-feature-discovery-operator#creating-nfd-cr-cli_psap-node-feature-discovery-operator) に基づいています。

次のスクリプトを実行して、Node Feature Discovery CR を作成します。

``` bash
./create-nfd-cr.sh
```

## NVIDIA GPU Operator のインストール

このセクションの手順は、[Installing the NVIDIA GPU Operator on OpenShift](https://docs.nvidia.com/datacenter/cloud-native/openshift/latest/install-gpu-ocp.html#installing-the-nvidia-gpu-operator-on-openshift) に基づいています。

次のスクリプトを実行して、NVIDIA GPU Operator をインストールします。

``` bash
./install-nvidia-gpu-operator.sh
```

インストールプランが作成されるまで待機します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
oc get installplan -n nvidia-gpu-operator
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME            CSV                              APPROVAL   APPROVED
install-mmlxq   gpu-operator-certified.v25.3.4   Manual     false
```

{{% /tab %}}
{{< /tabs >}}

次のコマンドでインストールプランを承認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
INSTALL_PLAN=$(oc get installplan -n nvidia-gpu-operator -oname)
oc patch $INSTALL_PLAN -n nvidia-gpu-operator --type merge --patch '{"spec":{"approved":true }}'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
installplan.operators.coreos.com/install-rc9xq patched
```

{{% /tab %}}
{{< /tabs >}}

## クラスターポリシーの作成

このセクションの手順は、[Create the cluster policy using the CLI](https://docs.nvidia.com/datacenter/cloud-native/openshift/latest/install-gpu-ocp.html#create-the-cluster-policy-using-the-cli) に基づいています。

``` bash
./create-cluster-policy.sh
```

## NVIDIA GPU Operator のインストール確認

次のコマンドを使用して、NVIDIA GPU Operator が正常にインストールされていることを確認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
oc get pods,daemonset -n nvidia-gpu-operator
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                                                      READY   STATUS      RESTARTS      AGE
pod/gpu-feature-discovery-sblkn                           1/1     Running     0             5m5s
pod/gpu-feature-discovery-zpt94                           1/1     Running     0             4m58s
pod/gpu-operator-6579bc6fdc-cp28l                         1/1     Running     0             23m
pod/nvidia-container-toolkit-daemonset-qfcl9              1/1     Running     0             5m5s
pod/nvidia-container-toolkit-daemonset-zbwb6              1/1     Running     0             4m59s
pod/nvidia-cuda-validator-f7tl2                           0/1     Completed   0             78s
pod/nvidia-cuda-validator-t7n9g                           0/1     Completed   0             71s
pod/nvidia-dcgm-exporter-gk66x                            1/1     Running     0             4m59s
pod/nvidia-dcgm-exporter-w8kr8                            1/1     Running     2 (52s ago)   5m5s
pod/nvidia-dcgm-lrnzr                                     1/1     Running     0             4m58s
pod/nvidia-dcgm-tvrdm                                     1/1     Running     0             5m5s
pod/nvidia-device-plugin-daemonset-d62nk                  1/1     Running     0             5m5s
pod/nvidia-device-plugin-daemonset-fnv4j                  1/1     Running     0             4m59s
pod/nvidia-driver-daemonset-418.94.202509100653-0-5xbvq   2/2     Running     0             5m48s
pod/nvidia-driver-daemonset-418.94.202509100653-0-hmkdl   2/2     Running     0             5m48s
pod/nvidia-node-status-exporter-2kqwr                     1/1     Running     0             5m44s
pod/nvidia-node-status-exporter-n8d9s                     1/1     Running     0             5m44s
pod/nvidia-operator-validator-r2nm2                       1/1     Running     0             5m5s
pod/nvidia-operator-validator-w2fpn                       1/1     Running     0             4m59s

NAME                                                           DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR                                                                                                         AGE
daemonset.apps/gpu-feature-discovery                           2         2         2       2            2           nvidia.com/gpu.deploy.gpu-feature-discovery=true                                                                      5m45s
daemonset.apps/nvidia-container-toolkit-daemonset              2         2         2       2            2           nvidia.com/gpu.deploy.container-toolkit=true                                                                          5m48s
daemonset.apps/nvidia-dcgm                                     2         2         2       2            2           nvidia.com/gpu.deploy.dcgm=true                                                                                       5m46s
daemonset.apps/nvidia-dcgm-exporter                            2         2         2       2            2           nvidia.com/gpu.deploy.dcgm-exporter=true                                                                              5m46s
daemonset.apps/nvidia-device-plugin-daemonset                  2         2         2       2            2           nvidia.com/gpu.deploy.device-plugin=true                                                                              5m47s
daemonset.apps/nvidia-device-plugin-mps-control-daemon         0         0         0       0            0           nvidia.com/gpu.deploy.device-plugin=true,nvidia.com/mps.capable=true                                                  5m47s
daemonset.apps/nvidia-driver-daemonset-418.94.202509100653-0   2         2         2       2            2           feature.node.kubernetes.io/system-os_release.OSTREE_VERSION=418.94.202509100653-0,nvidia.com/gpu.deploy.driver=true   5m48s
daemonset.apps/nvidia-mig-manager                              0         0         0       0            0           nvidia.com/gpu.deploy.mig-manager=true                                                                                5m45s
daemonset.apps/nvidia-node-status-exporter                     2         2         2       2            2           nvidia.com/gpu.deploy.node-status-exporter=true                                                                       5m44s
daemonset.apps/nvidia-operator-validator                       2         2         2       2            2           nvidia.com/gpu.deploy.operator-validator=true                                                                         5m48s
```

{{% /tab %}}
{{< /tabs >}}

## Operator SDK のインストール

このセクションの手順は、[Install from GitHub release](https://sdk.operatorframework.io/docs/installation/#install-from-github-release) に基づいています。

### リリースバイナリのダウンロード

プラットフォーム情報を設定します。

``` bash
export ARCH=$(case $(uname -m) in x86_64) echo -n amd64 ;; aarch64) echo -n arm64 ;; *) echo -n $(uname -m) ;; esac)
export OS=$(uname | awk '{print tolower($0)}')
```

お使いのプラットフォーム向けのバイナリをダウンロードします。

``` bash
export OPERATOR_SDK_DL_URL=https://github.com/operator-framework/operator-sdk/releases/download/v1.41.1
curl -LO ${OPERATOR_SDK_DL_URL}/operator-sdk_${OS}_${ARCH}
```

### ダウンロードしたバイナリの検証

keyserver.ubuntu.com から operator-sdk リリースの GPG キーをインポートします。

``` bash
gpg --keyserver keyserver.ubuntu.com --recv-keys 052996E2A20B5C7E
```

チェックサムファイルとその署名をダウンロードし、署名を検証します。

``` bash
curl -LO ${OPERATOR_SDK_DL_URL}/checksums.txt
curl -LO ${OPERATOR_SDK_DL_URL}/checksums.txt.asc
gpg -u "Operator SDK (release) <cncf-operator-sdk@cncf.io>" --verify checksums.txt.asc
```

次のような出力が表示されるはずです。

``` bash
gpg: assuming signed data in 'checksums.txt'
gpg: Signature made Fri 30 Oct 2020 12:15:15 PM PDT
gpg:                using RSA key ADE83605E945FA5A1BD8639C59E5B47624962185
gpg: Good signature from "Operator SDK (release) <cncf-operator-sdk@cncf.io>" [ultimate]
```

チェックサムが一致することを確認します。

``` bash
grep operator-sdk_${OS}_${ARCH} checksums.txt | sha256sum -c -
```

次のような出力が表示されるはずです。

``` bash
operator-sdk_linux_amd64: OK
```

### リリースバイナリを PATH にインストール

``` bash
chmod +x operator-sdk_${OS}_${ARCH} && sudo mv operator-sdk_${OS}_${ARCH} /usr/local/bin/operator-sdk
```

## NGC CLI のインストール

このセクションの手順は、[NGC CLI Install](https://org.ngc.nvidia.com/setup/installers/cli) に基づいています。

Download CLI をクリックしてバイナリを含む zip ファイルをダウンロードし、権限のあるディレクトリに転送してから、解凍してバイナリを実行します。実行権限のあるディレクトリに移動して次のコマンドを実行することで、コマンドラインからダウンロード、解凍、インストールを行うこともできます。

``` bash
wget --content-disposition https://api.ngc.nvidia.com/v2/resources/nvidia/ngc-apps/ngc_cli/versions/4.3.0/files/ngccli_linux.zip -O ngccli_linux.zip && unzip ngccli_linux.zip
```

ダウンロード時にファイルが破損していないことを確認するため、バイナリの md5 ハッシュをチェックします。

``` bash
find ngc-cli/ -type f -exec md5sum {} + | LC_ALL=C sort | md5sum -c ngc-cli.md5
```

ダウンロード時にファイルが破損していないことを確認するため、バイナリの SHA256 ハッシュをチェックします。次のコマンドを実行してください。

``` bash
sha256sum ngccli_linux.zip
```

リソースのリリースノートにも記載されている、次の値と比較します。

``` bash
5f01eff85a66c895002f3c87db2933c462f3b86e461e60d515370f647b4ffc21
```

値を確認したら、NGC CLI バイナリを実行可能にし、現在のディレクトリを PATH に追加します。

``` bash
chmod u+x ngc-cli/ngc
echo "export PATH=\"\$PATH:$(pwd)/ngc-cli\"" >> ~/.bash_profile && source ~/.bash_profile
```

コマンドを実行できるようにするため、NGC CLI を設定する必要があります。

次のコマンドを入力し、プロンプトが表示されたら API キーを入力します。

``` bash
ngc config set
```

NGC API キーを環境変数として定義します。

``` bash
export NGC_API_KEY=<your NGC API key> 
```

## NVIDIA NIM Operator のインストール

このセクションの手順は、[Installing NIM Operator on Red Hat OpenShift Using operator-sdk (for Development-Only)](https://docs.nvidia.com/nim-operator/latest/install.html#installing-nim-operator-on-red-hat-openshift-using-operator-sdk-for-development-only) に基づいています。

次のスクリプトを実行して、NIM Operator をインストールします。

``` bash
./install-nim-operator.sh
```

コントローラー Pod が実行中であることを確認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
oc get pods -n nvidia-nim-operator
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                                                              READY   STATUS      RESTARTS   AGE
ec60a4439c710b89fc2582f5384382b4241f9aee62bb3182b8d128e69dx54dc   0/1     Completed   0          61s
ghcr-io-nvidia-k8s-nim-operator-bundle-latest-main                1/1     Running     0          71s
k8s-nim-operator-86d478b55c-w5cf5                                 1/1     Running     0          50s
```

{{% /tab %}}
{{< /tabs >}}
