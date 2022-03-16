---
title: Deploying NGINX in K3s
linkTitle: Deploy and Monitor NGIX
weight: 2
---

* NGINX ReplicaSet を K3s クラスタにデプロイし、NGINX デプロイメントのディスカバリーを確認します。
* 負荷テストを実行してメトリクスを作成し、Splunk Observability Cloudにストリーミングすることを確認します！

---

## 1. NGINX の起動

Splunk UI で **WORKLOADS** タブを選択して、実行中の Pod の数を確認します。これにより、クラスタ上のワークロードの概要がわかるはずです。

![ワークロードエージェント](../../../images/k8s-workloads.png)

デフォルトの Kubernetes Pod のうち、ノードごとに実行されている単一のエージェントコンテナに注目してください。この1つのコンテナが、このノードにデプロイされているすべての Pod とサービスを監視します！

次に、**MAP** タブを選択してデフォルトのクラスタノードビューに戻し、再度クラスタを選択します。

Multipass または AWS/EC2 のシェルセッションで、`nginx` ディレクトリに移動します。

=== "シェルコマンド"

    ```text
    cd ~/workshop/k3s/nginx
    ```
  
---

## 2. NGINXのデプロイメント作成

NGINX の `configmap`[^1] を `nginx.conf` ファイルを使って作成します。

=== "シェルコマンド"

    ```text
    kubectl create configmap nginxconfig --from-file=nginx.conf
    ```

=== "出力"

    ```
    configmap/nginxconfig created
    ```

続いて、デプロイメントを作成します。

=== "シェルコマンド"

    ```
    kubectl create -f nginx-deployment.yaml
    ```

=== "出力"

    ```
    deployment.apps/nginx created
    service/nginx created
    ```

次に、NGINXに対するロードテストを作成するための Locust[^2] をデプロイします。

=== "シェルコマンド"

    ```
    kubectl create -f locust-deployment.yaml
    ```

=== "出力"

    ```
    deployment.apps/nginx-loadgenerator created
    service/nginx-loadgenerator created
    ```

デプロイメントが成功し、Locust と NGINX Podが動作していることを確認します。

Splunk UI を開いていれば、新しい Pod が起動し、コンテナがデプロイされているのがわかるはずです。

Pod が実行状態に移行するまでには 20 秒程度しかかかりません。Splunk UIでは、以下のようなクラスタが表示されます。

![Back to Cluster](../../../images/cluster.png)

もう一度 **WORKLOADS** タブを選択すると、新しい ReplicaSet と NGINX 用のデプロイメントが追加されていることがわかります。

![NGINX loaded](../../../images/k8s-workloads-nginx.png)

---

これをシェルでも検証してみましょう。

=== "シェルコマンド"

    ```text
    kubectl get pods
    ```

=== "出力"

    ```text
    NAME                                                          READY   STATUS    RESTARTS   AGE
    splunk-otel-collector-k8s-cluster-receiver-77784c659c-ttmpk   1/1     Running   0          9m19s
    splunk-otel-collector-agent-249rd                             1/1     Running   0          9m19s
    svclb-nginx-vtnzg                                             1/1     Running   0          5m57s
    nginx-7b95fb6b6b-7sb9x                                        1/1     Running   0          5m57s
    nginx-7b95fb6b6b-lnzsq                                        1/1     Running   0          5m57s
    nginx-7b95fb6b6b-hlx27                                        1/1     Running   0          5m57s
    nginx-7b95fb6b6b-zwns9                                        1/1     Running   0          5m57s
    svclb-nginx-loadgenerator-nscx4                               1/1     Running   0          2m20s
    nginx-loadgenerator-755c8f7ff6-x957q                          1/1     Running   0          2m20s
    ```

---

## 3. Locustの負荷テストの実行

EC2 インスタンスの IP アドレスの8080番ポートで Locust が利用できます。Webブラウザで新しいタブを開き、`http://{==EC2-IP==}:8080/`にアクセスすると、Locust が動作しているのが確認できます。

![Locust](../../../images/nginx-locust.png)

**Spawn rate** を 2 に設定し、**Start Swarming** をクリックします。

![Locust Spawn Rate](../../../images/nginx-locust-spawn-rate.png)

これにより、アプリケーションに緩やかな連続した負荷がかかるようになります。

![Locust Statistics](../../../images/nginx-locust-statistics.png)

ハンバーガーメニューから **Dashboards → NGINX → NGINX Servers** を選択して、UIにメトリクスが表示されていることを確認します。**Overrides** フィルターを適用して、 `k8s.cluster.name:` に、ターミナルの　`echo $(hostname)-k3s-cluster` で返されるクラスタの名前を見つけます。

![NGINXダッシュボード](../../../images/nginx-dashboard.png)

[^1]: ConfigMap とは、キーと値のペアで非機密データを保存するために使用される API オブジェクトです。Pod は、環境変数、コマンドライン引数、またはボリューム内の構成ファイルとして ConfigMap を利用することができます。ConfigMap を使用すると、環境固有の構成をコンテナイメージから切り離すことができるため、アプリケーションの移植が容易になります。

[^2]: [Locust とは？](https://locust.io/).
