var relearn_search_index=[{breadcrumb:"Splunk Observability Workshops > Splunk IM",content:` 5 分 各自に割り当てられたAWS/EC2インスタンスのIPアドレスを確認します SSH、Putty1、またはWebブラウザを使ってインスタンスに接続します クラウド上にある AWS/EC2 インスタンスへの接続を確認します 1. AWS/EC2 の IP アドレス ワークショップの準備として、Splunk は AWS/EC2 に Ubuntu Linux インスタンスを用意しています。
ワークショップで使用するインスタンスにアクセスするには、ワークショップの講師が提供する Google Sheets のURLにアクセスしてください。
AWS/EC2 インスタンスの検索には、本ワークショップの登録時にご記入いただいたお名前を入力してください。
ワークショップのインスタンスに接続するためのIPアドレス、SSHコマンド（Mac OS、Linux、最新のWindowsバージョン用）、パスワードが表示されています。
また、ssh や putty で接続できない場合に使用するブラウザアクセスのURLも記載されています。「ブラウザ経由でEC2に接続する」を参照してください。
Important 可能であれば、SSH または Putty を使用してEC2インスタンスにアクセスしてください。 ワークショップで必要になるので、IPアドレスをメモしておいてください。
2. SSH (Mac OS/Linux/Windows 10) Mac や Linux、または Windows10 以上の端末から SSH を使ってワークショップに接続することができます。
SSH を使用するには、お使いのシステムでターミナルを開き、ssh ubuntu@x.x.x.xと入力してください（x.x.x.xをステップ1で見つけたIPアドレスに置き換えてください）。
Are you sure you want to continue connecting (yes/no/[fingerprint])? というプロンプトが表示されたら yes と入力してください。
ステップ1の Google Sheets に記載されているパスワードを入力してください。
ログインに成功すると、Splunk のロゴと Linux のプロンプトが表示されます。
これで データを取り込む に進む準備が整いました。
3. SSH (Windows 10以降) 上記の手順はWindows 10でも同様で、コマンドはコマンドプロンプトかPowerShellで実行できます。 しかしWindowsはSSHを「オプション機能」として用意しているため、場合によっては有効化が必要です。
SSHが有効化されているかどうか確認するには単純に ssh を実行してください。
sshコマンドに関するヘルプテキスト（下のスクリーンショット）が表示されれば、実行可能です。
もしこのスクリーンショットとは異なる結果が表示された場合は「OpenSSH クライアント」機能の有効化が必要です。
「設定」メニューを開き「アプリ」をクリックします。「アプリと機能」セクションの「オプション機能」をクリックします。
ここでインストール済みの機能の一覧が表示されます。上部にプラスアイコンが付いた「機能の追加」ボタンがあるためクリックします。 検索欄で「OpenSSH」と入力し「OpenSSH クライアント」を探し、チェックし、インストールボタンをクリックします。
これで設定作業完了です。もしOpenSSH機能を有効にしてもインスタンスにアクセスできない場合、講師までご連絡ください
これで データを取り込む 準備が整いました。
4. Putty (Windows 10以前の場合) ssh がプリインストールされていない場合や、Windows システムを使用している場合、putty がおすすめです。Putty は こちら からダウンロードできます。
Important Putty がインストールできない場合は、 ブラウザ経由でEC2に接続する で進めてください。
Putty を開き、Host Name (or IP address) の欄に、Google Sheets に記載されているIPアドレスを入力してください。
名前を入力して Save を押すと、設定を保存することができます。
インスタンスにログインするには、Open ボタンをクリックします。
初めて AWS/EC2 ワークショップインスタンスに接続する場合は、セキュリティダイアログが表示されますので、Yes をクリックしてください。
接続されたら、ubuntu としてログインし、パスワードは Google Sheets に記載されているものを使用します。
接続に成功すると、以下のような画面が表示されます。
これで データを取り込む 準備が整いました。
5. ブラウザ経由でEC2に接続する SSH（ポート22） の使用が禁止されている場合や、Putty がインストールできない場合は、Webブラウザを使用してワークショップのインスタンスに接続することができます。
Note ここでは、6501番ポートへのアクセスが、ご利用のネットワークのファイアウォールによって制限されていないことを前提としています。
Webブラウザを開き、http:/x.x.x.x:6501 （X.X.X.Xは Google Sheetsに記載されたIPアドレス）と入力します。
接続されたら、ubuntu としてログインし、パスワードは Google Sheets に記載されているものを使用します。
接続に成功すると、以下のような画面が表示されます。
通常のSSHを使用しているときとは異なり、ブラウザセッションを使用しているときは、コピー＆ペースト を使うための手順が必要です。これは、クロスブラウザの制限によるものです。
ワークショップで指示をターミナルにコピーするように言われたら、以下のようにしてください。
通常通り指示をコピーし、ウェブターミナルにペーストする準備ができたら、以下のように Paste from browser を選択します。
すると、ウェブターミナルに貼り付けるテキストを入力するダイアログボックスが表示されます。
表示されているテキストボックスにテキストを貼り付け、OK を押すと、コピー＆ペーストができます。
Note 通常のSSH接続とは異なり、Webブラウザには60秒のタイムアウトがあり、接続が解除されると、Webターミナルの中央に Connect ボタンが表示されます。
この Connect ボタンをクリックするだけで、再接続され、次の操作が可能になります。
これで データを取り込む に進む準備が整いました。
6. Multipass (全員) AWSへはアクセスできないが、ローカルにソフトウェアをインストールできる場合は、「Multipassを使用する」の手順に従ってください。
Putty のダウンロード ↩︎
`,description:"",tags:null,title:"ワークショップ環境へのアクセス",uri:"/ja/imt/initial-setup/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector レシーバー",content:`Host Metrics レシーバー Host Metrics レシーバー は、さまざまなソースからスクレイピングされたホストシステムに関するメトリクスを生成します。これは、コレクターがエージェントとしてデプロイされるときに使用さます。
etc/otel-contrib/config.yaml ファイルを更新して、hostmetrics レシーバーを設定してみましょう。以下の YAML を receivers セクションの下に挿入します。
sudo vi /etc/otelcol-contrib/config.yaml ​ Host Metrics Receiver Configuration receivers: hostmetrics: collection_interval: 10s scrapers: # CPU utilization metrics cpu: # Disk I/O metrics disk: # File System utilization metrics filesystem: # Memory utilization metrics memory: # Network interface I/O metrics & TCP connection metrics network: # CPU load metrics load: # Paging/Swap space utilization and I/O metrics paging: # Process count metrics processes: # Per process CPU, Memory and Disk I/O metrics. Disabled by default. # process: `,description:"",tags:null,title:"OpenTelemetry Collector レシーバー",uri:"/ja/other/opentelemetry-collector/3-receivers/1-hostmetrics/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk APM",content:` 15分 Online BoutiqueアプリケーションをKubernetes(K3s)にデプロイします アプリケーションが動作していることを確認します Locustを使って人工的なトラフィックを生成します UI で APM のメトリクスを見ましょう 1. EC2サーバーを確認 これからの操作は、IMワークショップを実行した後で、まだEC2インスタンスにアクセスできる状態であることを想定しています。 もしアクセスできる場合は、 2. Online Boutiqueをデプロイする に進みます。 新しいインスタンスを受け取った場合は、 データを取り込む の最初の2つのセクションを実行して、システムをAPMワークショップのために準備し、次のセクションを続行してください。
2. Online Boutiqueをデプロイする Online BoutiqueアプリケーションをK3sにデプロイするには、以下のデプロイメントを適用します。
​ Deploy Online Boutique Deployment Output cd ~/workshop/apm kubectl apply -f deployment.yaml APM Only Deployment deployment.apps/recommendationservice created service/recommendationservice created deployment.apps/productcatalogservice created service/productcatalogservice created deployment.apps/cartservice created service/cartservice created deployment.apps/adservice created service/adservice created deployment.apps/paymentservice created service/paymentservice created deployment.apps/loadgenerator created service/loadgenerator created deployment.apps/shippingservice created service/shippingservice created deployment.apps/currencyservice created service/currencyservice created deployment.apps/redis-cart created service/redis-cart created deployment.apps/checkoutservice created service/checkoutservice created deployment.apps/frontend created service/frontend created service/frontend-external created deployment.apps/emailservice created service/emailservice created deployment.apps/rum-loadgen-deployment created 変数未セットに関するメッセージが表示された場合 kubectl delete -f deployment.yaml コマンドを実行しAPM環境のデプロイ削除します。 次にガイド、メッセージに表示されていた変数をexportし上記のデプロイスクリプトを再実行します。
Online Boutique アプリケーションが起動していることを確認するには:
​ Get Pods Get Pods Output kubectl get pods NAME READY STATUS RESTARTS AGE splunk-otel-collector-k8s-cluster-receiver-56585564cc-xclzj 1/1 Running 0 84s splunk-otel-collector-agent-hkshj 1/1 Running 0 84s svclb-frontend-external-c74n6 1/1 Running 0 53s currencyservice-747b74467f-xxrl9 1/1 Running 0 52s redis-cart-74594bd569-2jb6c 1/1 Running 0 54s adservice-6fb948b8c6-2xlrc 0/1 Running 0 53s recommendationservice-b5df8776c-sbt4h 1/1 Running 0 53s shippingservice-6d6f7b8d87-5lg9g 1/1 Running 0 53s svclb-loadgenerator-jxwct 1/1 Running 0 53s emailservice-9dd74d87c-wjdqr 1/1 Running 0 53s checkoutservice-8bcd56b46-bfj7d 1/1 Running 0 54s productcatalogservice-796cdcc5f5-vhspz 1/1 Running 0 53s paymentservice-6c875bf647-dklzb 1/1 Running 0 53s frontend-b8f747b87-4tkxn 1/1 Running 0 53s cartservice-59d5979db7-bqf64 1/1 Running 1 53s loadgenerator-57c8b84966-7nr4f 1/1 Running 3 53s Info 通常、ポッドがRunning状態に移行するのに1分30秒程度かかります。
3. UIで検証する Splunk UIでInfrastructure をクリックします。Infrastructure Overviewダッシュボードに遷移しますので、 Kubernetes をクリックします。
Cluster のドロップダウンを使用してクラスタを選択すると、新しいポッドが開始され、コンテナがデプロイされていることが確認できます。
Splunk UI で Cluster をクリックすると、次のような画面が表示されているはずです。
もう一度 WORKLOADS タブを選択すると、いくつかのデプロイメントとレプリカセットがあることがわかるはずです。
4. Online Boutique を閲覧する Online Boutique は、EC2インスタンスのIPアドレスの81番ポートで閲覧できます。このIPアドレスは、ワークショップの冒頭でインスタンスにSSH接続したときに使用したものと同じIPアドレスです。
ウェブブラウザを開き、 http://<EC2-IP>:81/ にアクセスすると、Online Boutique が起動しているのが確認できます。
`,description:"Online BoutiqueアプリケーションをKubernetes（K3s）にデプロイし、Locustを使って人工的なトラフィックを発生させます。",tags:null,title:"1. Online Boutiqueのデプロイ",uri:"/ja/apm/online-boutique/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > Pet Clinic Java ワークショップ",content:`1. はじめに OpenTelemetry Collectorは、インフラストラクチャーとアプリケーションを計装するためのコアコンポーネントです。 その役割は収集と送信です：
インフラストラクチャーのメトリクス（ディスク、CPU、メモリなど） アプリケーションパフォーマンスモニタリング（APM）のトレース情報 プロファイリングに関するデータ ホストおよびアプリケーションのログ Splunk Observability Cloudでは、インフラストラクチャーとアプリケーションの両方で Collector のセットアップを案内するウィザードを提供しています。デフォルトでは、ウィザードはコレクターのインストールのみを行うコマンドのみを提供します。
2. 環境変数を設定する すでに Splunk IM ワークショップを終了している場合は、既存の環境変数を利用することができます。そうでない場合は、ACCESS_TOKENとREALMの環境変数を設定して、OpenTelemetry Collectorのインストールコマンドを実行していきます。
例えば、Realmが us1 の場合、export REALM=us1 と入力し、eu0 の場合は export REALM=eu0 と入力します。
​ ACCESS TOKENを環境変数に設定する export ACCESS_TOKEN="<replace_with_O11y-Workshop-ACCESS_TOKEN>" ​ REALMを環境変数に設定する export REALM="<replace_with_REALM>" 既存のOpenTelemetryコレクターをすべて削除する 同じVMインスタンスにSplunk IM ワークショップのセットアップをしている場合、Otel Collectorをインストールする前に Kubernetes で実行中の Collector を削除していることを確認してください。これは、以下のコマンドを実行することで行うことができます：
helm delete splunk-otel-collector 3. OpenTelemetry Collectorをインストールする 次に、Collectorをインストールします。インストールスクリプトに渡される追加のパラメータは --deployment-environment です。
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \\ sudo sh /tmp/splunk-otel-collector.sh --deployment-environment $(hostname)-petclinic --realm $REALM -- $ACCESS_TOKEN AWS/EC2インスタンスの場合 。 AWS/EC2インスタンス上でこのワークショップを行う場合、インスタンスのホスト名を公開するためにコレクターにパッチを適用する必要があります：
sudo sed -i 's/gcp, ecs, ec2, azure, system/system, gcp, ecs, ec2, azure/g' /etc/otel/collector/agent_config.yamlagent_config.yaml にパッチを適用したあと、Collector を再起動してください：
sudo systemctl restart splunk-otel-collector インストールが完了したら、Splunk Observabilityの Hosts with agent installed ダッシュボードに移動して、Dashboards → Hosts with agent installed からホストのデータを確認してみましょう。
ダッシュボードのフィルタを使用して host.nameを選択し、仮想マシンのホスト名を入力または選択します。ホストのデータが表示されたら、APMコンポーネントを使用する準備が整いました。
`,description:"",tags:null,title:"OpenTelemetry Collectorをインストールする",uri:"/ja/other/pet-clinic/docs/imt/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する",content:`OpenTelemetry Collector の Contrib ディストリビューションをダウンロードする OpenTelemetry Collector のインストールのために、まずはダウンロードするのが最初のステップです。このラボでは、 wget コマンドを使って OpenTelemetry の GitHub リポジトリから .deb パッケージをダウンロードしていきます。
OpenTelemetry Collector Contrib releases page から、ご利用のプラットフォーム用の .deb パッケージを入手してください。
wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.80.0/otelcol-contrib_0.80.0_linux_amd64.debOpenTelemetry Collector の Contrib ディストリビューションをインストールする dpkg を使って、 .deb パッケージをインストールします。下記の dpkg Output のようになれば、インストールは成功です！
​ Install dpkg Output sudo dpkg -i otelcol-contrib_0.80.0_linux_amd64.deb Selecting previously unselected package otelcol-contrib. (Reading database ... 64218 files and directories currently installed.) Preparing to unpack otelcol-contrib_0.75.0_linux_amd64.deb ... Unpacking otelcol-contrib (0.75.0) ... Setting up otelcol-contrib (0.75.0) ... Created symlink /etc/systemd/system/multi-user.target.wants/otelcol-contrib.service → /lib/systemd/system/otelcol-contrib.service. `,description:"",tags:null,title:"OpenTelemetry Collector Contrib をインストールする",uri:"/ja/other/opentelemetry-collector/1-installation/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk RUM",content:`RUM ワークショップの概要 このSplunk Real User Monitoring (RUM) ワークショップの目的は以下の通りです。
素敵な商品を買えるOnline Boutiqueサイトでトラフィックを発生させ、 RUM ユーザーセッション1を作成し、Splunk Observability Suiteで確認します
Application Summary Dashboard (モバイル、Web両方) で アプリケーション全体のパフォーマンスの概要を確認します
RUM メトリクスで、特定のWebサイトやモバイルアプリのパフォーマンスを検証します
Webサイトやバックエンドサービスの問題を調査します
(オプション) あなたのWebサイトへの RUM の追加方法を学びます
この目的のため、Online Boutiqueで様々な商品を注文することになります。Online Boutiqueで買い物をするとき、あなたはユーザーセッション1と呼ばれるものを作成します。
この Web サイトでいくつかの問題に遭遇することがなりますが、Splunk RUM を使用して問題を特定し、開発者が問題を解決できるようにします。
RUM 単体のワークショップの場合、ワークショップ講師が RUM を導入しているOnline BoutiqueのURLをお知らせします。
IM/APM ワークショップの一環としてこのセッションを実施する場合、講師側でRUMを有効にした後、現在お使いのOnline Boutiqueを使用することが可能です。
これらのOnline Boutiqueには、それぞれ数人の合成ユーザー（シミュレートされたユーザーセッション）が訪問しており、これによって、後で分析するためのより多くのライブデータを生成することができます。
RUM ユーザーセッションは、アプリケーション上でのユーザーインタラクションの「記録」であり、基本的にはエンドユーザーのブラウザまたはモバイルアプリケーションから直接測定されたウェブサイトまたはアプリケーションのパフォーマンスを収集します。これを行うために、各ページに数行のJavaScriptが埋め込まれています。このスクリプトは、各ユーザーがページを探索する際にデータを収集し、解析のためにそのデータを転送します。 ↩︎ ↩︎
`,description:"",tags:null,title:"1. 概要",uri:"/ja/rum/1-overview/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector Contrib をインストールする",content:`Collector が動作していることを確認する これで、Collector が動いているはずです。root権限で systemctl コマンドを使って、それを確かめてみましょう。ステータス表示を中止するには q を押してください。
​ Command Status Output sudo systemctl status otelcol-contrib ● otelcol-contrib.service - OpenTelemetry Collector Contrib Loaded: loaded (/lib/systemd/system/otelcol-contrib.service; enabled; vendor preset: enabled) Active: active (running) since Tue 2023-05-16 08:23:23 UTC; 25s ago Main PID: 1415 (otelcol-contrib) Tasks: 5 (limit: 1141) Memory: 22.2M CPU: 125ms CGroup: /system.slice/otelcol-contrib.service └─1415 /usr/bin/otelcol-contrib --config=/etc/otelcol-contrib/config.yaml May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: NumberDataPoints #0 May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: Data point attributes: May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: -> exporter: Str(logging) May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: -> service_instance_id: Str(df8a57f4-abdc-46b9-a847-acd62db1001f) May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: -> service_name: Str(otelcol-contrib) May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: -> service_version: Str(0.75.0) May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: StartTimestamp: 2023-05-16 08:23:39.006 +0000 UTC May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: Timestamp: 2023-05-16 08:23:39.006 +0000 UTC May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: Value: 0.000000 May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: {"kind": "exporter", "data_type": "metrics", "name": "logging"} このワークショップでは、ここで設定した otelcol-contrib のスタンドアローンで動作するバイナリーを使っていきます。サービスを停止して、自動起動を無効化するために、次のコマンドを使ってください:
​ Command sudo systemctl stop otelcol-contrib ​ Command sudo systemctl disable otelcol-contrib Ninja: Open Telemetry Collector Builder (ocb) を使って、独自のコレクターを作る このパートでは、お使いのシステムに以下のものがインストールされている必要があります：
Go (latest version)
cd /tmp wget https://golang.org/dl/go1.20.linux-amd64.tar.gz sudo tar -C /usr/local -xzf go1.20.linux-amd64.tar.gz.profile を編集して、次の環境変数をセットします:
export GOROOT=/usr/local/go export GOPATH=$HOME/go export PATH=$GOPATH/bin:$GOROOT/bin:$PATHそして、シェルのセッションを更新します:
source ~/.profileGo のバージョンを確認します:
go version ocb のインストール
ocb バイナリーを project releases からダウンロードして、次のコマンドを実行します:
mv ocb_0.80.0_darwin_arm64 /usr/bin/ocb chmod 755 /usr/bin/ocb別のアプローチとして、Go のツールチェーンを使ってバイナリをローカルにビルドする方法もあります:
go install go.opentelemetry.io/collector/cmd/builder@v0.80.0 mv $(go env GOPATH)/bin/builder /usr/bin/ocb (Optional) Docker
なぜ独自のコレクターをビルドするの？ コレクターのデフォルトのディストリビューション（core および contrib）は、含まれれるコンポーネントが少なすぎたり、もしくは多すぎたりします。
本番環境で contrib コレクターを実行することはできますが、インストールされているコンポーネントの量が多く、デプロイに必要ではないものも含まれるため、一般的には推奨されません。
独自のコレクターをビルドする利点は？ 独自のコレクターバイナリー（通常は「ディストリビューション」と呼ばれる）を作成することで、必要なものだけをビルドすることができます。
メリットは次のとおりです:
バイナリーのサイズが小さい 一般的な Go の脆弱性スキャナーを利用できる 組織独自のコンポーネントを組み込むことができる カスタムコレクターをビルドするときの注意事項は？ さて、これは Ninja ゾーンの人たちにあえて言うことではないかもしれませんが:
Go の開発経験を、必須ではないが、推奨される Splunk の サポートがない ディストリビューションのライフサイクルを管理しなければならない プロジェクトは安定性に向けて進んでいますが、行われた変更がワークフローを壊す可能性があることに注意してください。Splunk チームは、より高い安定性とサポートを提供し、デプロイメントニーズに対応するためのキュレーションされた経験を提供しています。
Ninja ゾーン 必要なツールをすべてインストールしたら、以下のディレクトリ構造に従い、 otelcol-builder.yaml という新しいファイルを作成します:
. └── otelcol-builder.yamlファイルを作成したら、インストールするコンポーネントのリストと追加のメタデータを追加する必要があります。
この例では、導入設定に必要なコンポーネントのみをインストールするためのビルダーマニフェストを作成します:
dist: name: otelcol-ninja description: A custom build of the Open Telemetry Collector output_path: ./dist extensions: - gomod: go.opentelemetry.io/collector/extension/ballastextension v0.80.0 - gomod: go.opentelemetry.io/collector/extension/zpagesextension v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/httpforwarder v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/healthcheckextension v0.80.0 exporters: - gomod: go.opentelemetry.io/collector/exporter/loggingexporter v0.80.0 - gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/splunkhecexporter v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/signalfxexporter v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/sapmexporter v0.80.0 processors: - gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.80.0 - gomod: go.opentelemetry.io/collector/processor/memorylimiterprocessor v0.80.0 receivers: - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/jaegerreceiver v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/prometheusreceiver v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/zipkinreceiver v0.80.0ocb のためのyamlファイルを作成して更新したら、 次のコマンドを実行します:
ocb --config=otelcol-builder.yamlすると、次のようなディレクトリ構造が作成されます:
├── dist │ ├── components.go │ ├── components_test.go │ ├── go.mod │ ├── go.sum │ ├── main.go │ ├── main_others.go │ ├── main_windows.go │ └── otelcol-ninja └── otelcol-builder.yamlリファレンス https://opentelemetry.io/docs/collector/custom-collector/ デフォルト設定 OpenTelemetry Collector は YAML ファイルを使って設定をしていきます。これらのファイルには、必要に応じて変更できるデフォルト設定が含まれています。提供されているデフォルト設定を見てみましょう:
​ Command config.yaml cat /etc/otelcol-contrib/config.yaml 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 extensions: health_check: pprof: endpoint: 0.0.0.0:1777 zpages: endpoint: 0.0.0.0:55679 receivers: otlp: protocols: grpc: http: opencensus: # Collect own metrics prometheus: config: scrape_configs: - job_name: 'otel-collector' scrape_interval: 10s static_configs: - targets: ['0.0.0.0:8888'] jaeger: protocols: grpc: thrift_binary: thrift_compact: thrift_http: zipkin: processors: batch: exporters: logging: verbosity: detailed service: pipelines: traces: receivers: [otlp, opencensus, jaeger, zipkin] processors: [batch] exporters: [logging] metrics: receivers: [otlp, opencensus, prometheus] processors: [batch] exporters: [logging] extensions: [health_check, pprof, zpages] おめでとうございます！OpenTelemetry Collector のダウンロードとインストールに成功しました。あなたは OTel Ninja になる準備ができました。しかしまずは、設定ファイルと OpenTelemetry Collector の異なるディストリビューションについて見ていきましょう。
メモ Splunk は、自社で完全にサポートされた OpenTelemetry Collector のディストリビューションを提供しています。このディストリビューションは、Splunk GitHub Repository からインストールするか、Splunk Observability Cloud のウィザードを使用して、簡単なインストールスクリプトを作成し、コピー＆ペーストすることで利用できます。このディストリビューションには、OpenTelemetry Collector Contrib ディストリビューションにはない追加機能や強化が含まれています。
Splunk の OpenTelemetry Collector ディストリビューションは本番環境でテスト済みであり、多くの顧客が本番環境で使用しています。 このディストリビューションを使用する顧客は、公式の Splunk サポートから、SLA の範囲内で直接支援を受けることができます。 メトリクスとトレース収集のコア構成体験に将来的な破壊的変更がないことを心配せずに、Splunk の OpenTelemetry Collector ディストリビューションを使用または移行することができます（OpenTelemetry ログ収集の設定はベータ版です）。Collector 自身のメトリクスに破壊的変更がある可能性はあります。 このセクションでは、ホストメトリクスを Splunk Observability Cloud に送信するために、設定ファイルの各セクションを詳しく見ていき、変更する方法について説明します。
`,description:"",tags:null,title:"OpenTelemetry Collector Contribをインストールする",uri:"/ja/other/opentelemetry-collector/1-installation/1-confirmation/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector エクステンション",content:`Health Check エクステンション 他のコンポーネントと同様に、エクステンションは config.yaml ファイルで設定できます。ここでは実際に config.yaml ファイルを編集して、エクステンションを設定していきましょう。デフォルトの config.yaml では、すでに pprof エクステンションと zpages エクステンションが設定されていることを確認してみてください。このワークショップでは、設定ファイルをアップデートして health_check エクステンションを追加し、ポートを解放し、外部ネットワークからコレクターのヘルスチェックにアクセスできるようにしていきます。
​ Command sudo vi /etc/otelcol-contrib/config.yaml ​ Extensions Configuration extensions: health_check: endpoint: 0.0.0.0:13133 コレクターを起動します:
​ Command otelcol-contrib --config=file:/etc/otelcol-contrib/config.yaml このエクステンションはHTTPのURLを公開し、OpenTelemetory Collectorの稼働状況をチェックするプローブを提供します。このエクステンションはKubernetes環境でのLiveness/Readinessプローブとしても使われています。 curl コマンドの使い方は、curl man page を参照してください。
ターミナルを開いて、対象インスタンスにSSH接続し、次のコマンドを実行します:
​ curl Command curl Output curl http://localhost:13133 {"status":"Server available","upSince":"2023-04-27T10:11:22.153295874+01:00","uptime":"16m24.684476004s"} `,description:"",tags:null,title:"OpenTelemetry Collector エクステンション",uri:"/ja/other/opentelemetry-collector/2-extensions/1-health/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM > ダッシュボードを利用する",content:`1. チャートの編集 Sample Data ダッシュボードにある Latency histogram チャートの3点 ... をクリックして、Open をクリックします（または、チャートの名前をクリックしてください、ここでは Latency histogram です）。
チャートエディターのUIには、Latency histogram チャートのプロットオプション、カレントプロット、シグナル（メトリック）が表示されます。
Plot Editor タブの Signal には、現在プロットしている demo.trans.latency というメトリックが表示されます。
いくつかの Line プロットが表示されます。18 ts という数字は、18個の時系列メトリックをチャートにプロットしていることを示しています。
異なるチャートタイプのアイコンをクリックして、それぞれの表示を確認してください。スワイプしながらその名前を確認してください。例えば、ヒートマップのアイコンをクリックします。
チャートがヒートマップに変わります。
Note 様々なチャートを使用してメトリクスを視覚化することができます。自分が望む視覚化に最も適したチャートタイプを選択してください。
各チャートタイプの詳細については、 Choosing a chart type を参照してください。
チャートタイプの Line をクリックすると、線グラフが表示されます。
2. タイムウィンドウの変更 また、Time ドロップダウンから Past 15 minutes に変更することで、チャートの時間枠を変更することができます。
3. データテーブルの表示 Data Table タブをクリックします。
18行が表示され、それぞれがいくつかの列を持つ時系列メトリックを表しています。これらの列は、メトリックのディメンションを表しています。demo.trans.latency のディメンジョンは次のとおりです。
demo_datacenter demo_customer demo_host demo_datacenter 列では、メトリクスを取得している2つのデータセンター、Paris と Tokyo があることがわかります。
グラフの線上にカーソルを横に移動させると、それに応じてデータテーブルが更新されるのがわかります。チャートのラインの1つをクリックすると、データテーブルに固定された値が表示されます。
ここでもう一度 Plot editor をクリックしてデータテーブルを閉じ、このチャートをダッシュボードに保存して、後で使用しましょう。
`,description:"",tags:null,title:"チャートを編集する",uri:"/ja/imt/dashboards/editing/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector プロセッサー",content:`Batch プロセッサー デフォルトでは、batch プロセッサーだけが有効になっています。このプロセッサーは、データをエクスポートする前にバッチ処理して、エクスポーターへのネットワーク・コールの回数を減らすために使われます。このワークショップではデフォルトの設定を使用します：
send_batch_size (デフォルト = 8192): タイムアウトに関係なく、バッチを送信するスパン、メトリクスデータポイント、またはログレコードの数。パイプラインの次のコンポーネントに送信されるバッチサイズを制限する場合には、 send_batch_max_size を使います。 timeout (デフォルト = 200ms): サイズに関係なく、バッチが送信されるまでの時間。ゼロに設定すると、send_batch_size の設定を無視して send_batch_max_size だけが適用され、データは直ちに送信されます。 send_batch_max_size (デフォルト = 0): バッチサイズの上限。0 を設定すると、バッチサイズの上限がないことして扱われます。この設定は、大きなバッチが小さなユニットに分割されることを保証します。send_batch_size 以上でなければななりません。 `,description:"",tags:null,title:"OpenTelemetry Collector プロセッサー",uri:"/ja/other/opentelemetry-collector/4-processors/1-batch-processor/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM > ディテクターを利用する",content:` ミューティングルールを設定する 通知を再開する 1. ミューティングルールの設定 特定の通知をミュートする必要がある場合があります。例えば、サーバーやサーバー群のメンテナンスのためにダウンタイムを設定したい場合や、新しいコードや設定をテストしている場合などがあります。このような場合には、Splunk Observability Cloud でミューティングルールを使用できます。それでは作成してみましょう。
ナビバーにある ボタンをクリックし、Detectors を選択します。現在設定されているディテクターの一覧が表示されます。フィルタを使ってディテクターを探すこともできます。
Creating a Detector でディテクターを作成した場合は、右端の3つの点 ... をクリックすると、そのディテクターが表示されます。
ドロップダウンから Create Muting Rule… をクリックします。
Muting Rule ウィンドウで、 Mute Indefinitely をチェックし、理由を入力します。
Important この操作をすると、ここに戻ってきてこのボックスのチェックを外すか、このディテクターの通知を再開するまで、通知が永久的にミュートされます。
Next をクリックして、新しいモーダルウィンドウでミュートルールの設定を確認します。
Mute Indefinitely をクリックして、設定を確定させます。
これで、通知を再開するまで、ディテクターからのEメール通知は受け取ることがなくなりました。では、再開する方法を見てみましょう。
2. 通知を再開する Muting Rules をクリックして、Detector の見出しの下に、通知をミュートしたディテクターの名前が表示されます。
右端にあるドット ... を開いて、Resume Notifications をクリックします。
Resume をクリックして、このディテクターの通知を確認し、再開します。
おめでとうございます！ これでアラート通知が再開されました。
`,description:"",tags:null,title:"ミューティングルールを利用する",uri:"/ja/imt/detectors/muting/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector エクスポーター",content:`OTLP HTTP エクスポーター Splunk Observability Cloud へ HTTP 経由でメトリックスを送信するためには、otlphttp エクスポーターを設定する必要があります。
/etc/otelcol-contrib/config.yaml ファイルを編集し、otlphttp エクスポーターを設定しましょう。以下の YAML を exporters セクションの下に挿入し、例えば2スペースでインデントしてください。
また、ディスクの容量不足を防ぐために、ロギングエクスポーターの詳細度を変更します。デフォルトの detailed は非常に詳細です。
exporters: logging: verbosity: normal otlphttp/splunk:次に、metrics_endpoint を定義して、ターゲットURLを設定していきます。
メモ Splunk 主催のワークショップの参加者である場合、使用しているインスタンスにはすでに Realm 環境変数が設定されています。その環境変数を設定ファイルで参照します。それ以外の場合は、新しい環境変数を作成して Realm を設定する必要があります。例えば：
export REALM="us1" 使用するURLは https://ingest.\${env:REALM}.signalfx.com/v2/datapoint/otlp です。（Splunkは、データの居住地に応じて世界中の主要地域に Realm を持っています）。
otlphttp エクスポーターは、traces_endpoint と logs_endpoint それぞれのターゲットURLを定義することにより、トレースとログを送信するようにも設定できますが、そのような設定はこのワークショップの範囲外とします。
exporters: logging: verbosity: normal otlphttp/splunk: metrics_endpoint: https://ingest.\${env:REALM}.signalfx.com/v2/datapoint/otlpデフォルトでは、すべてのエンドポイントで gzip 圧縮が有効になっています。エクスポーターの設定で compression: none を設定することにより、圧縮を無効にすることができます。このワークショップでは圧縮を有効にしたままにし、データを送信する最も効率的な方法としてデフォルト設定を使っていきます。
Splunk Observability Cloud にメトリクスを送信するためには、アクセストークンを使用する必要があります。これは、Splunk Observability Cloud UI で新しいトークンを作成することにより行うことができます。トークンの作成方法についての詳細は、Create a token を参照してください。トークンは INGEST タイプである必要があります。
メモ Splunk　主催のワークショップの参加者である場合、使用しているインスタンスにはすでにアクセストークンが設定されています（環境変数として設定されています）ので、その環境変数を設定ファイルで参照します。それ以外の場合は、新しいトークンを作成し、それを環境変数として設定する必要があります。例えば：
export ACCESS_TOKEN=<replace-with-your-token> トークンは、設定ファイル内で headers: セクションの下に X-SF-TOKEN: \${env:ACCESS_TOKEN} を挿入することにで定義します：
exporters: logging: verbosity: normal otlphttp/splunk: metrics_endpoint: https://ingest.\${env:REALM}.signalfx.com/v2/datapoint/otlp headers: X-SF-TOKEN: \${env:ACCESS_TOKEN}設定を確認しましょう これで、エクスポーターもカバーできました。設定を確認していきましょう： Now that we’ve covered exporters, let’s check our configuration changes:
Check-in設定をレビューしてください ​ config.yaml 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 extensions: health_check: endpoint: 0.0.0.0:13133 pprof: endpoint: 0.0.0.0:1777 zpages: endpoint: 0.0.0.0:55679 receivers: hostmetrics: collection_interval: 10s scrapers: # CPU utilization metrics cpu: # Disk I/O metrics disk: # File System utilization metrics filesystem: # Memory utilization metrics memory: # Network interface I/O metrics & TCP connection metrics network: # CPU load metrics load: # Paging/Swap space utilization and I/O metrics paging: # Process count metrics processes: # Per process CPU, Memory and Disk I/O metrics. Disabled by default. # process: otlp: protocols: grpc: http: opencensus: # Collect own metrics prometheus/internal: config: scrape_configs: - job_name: 'otel-collector' scrape_interval: 10s static_configs: - targets: ['0.0.0.0:8888'] jaeger: protocols: grpc: thrift_binary: thrift_compact: thrift_http: zipkin: processors: batch: resourcedetection/system: detectors: [system] system: hostname_sources: [os] resourcedetection/ec2: detectors: [ec2] attributes/conf: actions: - key: participant.name action: insert value: "INSERT_YOUR_NAME_HERE" exporters: logging: verbosity: normal otlphttp/splunk: metrics_endpoint: https://ingest.\${env:REALM}.signalfx.com/v2/datapoint/otlp headers: X-SF-TOKEN: \${env:ACCESS_TOKEN} service: pipelines: traces: receivers: [otlp, opencensus, jaeger, zipkin] processors: [batch] exporters: [logging] metrics: receivers: [otlp, opencensus, prometheus] processors: [batch] exporters: [logging] extensions: [health_check, pprof, zpages] もちろん、OTLP プロトコルをサポートする他のソリューションを指すように metrics_endpoint を簡単に設定することができます。
次に、config.yaml のサービスセクションで、今設定したレシーバー、プロセッサー、エクスポーターを有効にしていきます。
`,description:"",tags:null,title:"OpenTelemetry Collector エクスポーター",uri:"/ja/other/opentelemetry-collector/5-exporters/otlphttp/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector サービス",content:`Hostmetrics レシーバー ワークショップのレシーバー部分で振り返ると、ホストシステムに関するメトリクスを生成するために、様々なソースからスクレイピングする Host Metrics レシーバーを定義しました。このレシーバーを有効にするためには、メトリクスパイプラインに hostmetrics レシーバーを含める必要があります。
metrics パイプラインで、メトリクスの receivers セクションに hostmetrics を追加します。
service: pipelines: traces: receivers: [otlp, opencensus, jaeger, zipkin] processors: [batch] exporters: [logging] metrics: receivers: [hostmetrics, otlp, opencensus, prometheus] processors: [batch] exporters: [logging]`,description:"",tags:null,title:"OpenTelemetry Collector サービス",uri:"/ja/other/opentelemetry-collector/6-service/1-hostmetrics/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM > 管理機能",content:` チームの管理 チームの作成とメンバーの追加 1. チームの管理 Observability Cloudを使用する際に、ユーザーに関連するダッシュボードやアラートが表示されるようにするために、ほとんどの組織ではObservability Cloudのチーム機能を使用して、メンバーを1つまたは複数のチームに割り当てます。
これは、仕事に関連した役割と一致するのが理想的で、たとえば、DevOpsグループやプロダクトマネジメントグループのメンバーは、Observability Cloudの対応するチームに割り当てられます。
ユーザーがObservability Cloudにログインすると、どのチームダッシュボードをホームページにするかを選択することができ、通常は自分の主な役割に応じたページを選択します。
以下の例では、ユーザーは開発、運用、プロダクトマネジメントの各チームのメンバーであり、現在は運用チームのダッシュボードを表示しています。
このダッシュボードには、NGINX、Infra、K8s用の特定のダッシュボード・グループが割り当てられていますが、どのダッシュボード・グループもチーム・ダッシュボードにリンクすることができます。
左上のメニューを使って割り当てられたチーム間を素早く移動したり、右側の ALL TEAMS ドロップダウンを使って特定のチームのダッシュボードを選択したり、隣のリンクを使って ALL Dashboards に素早くアクセスしたりすることができます。
アラートを特定のチームにリンクすることで、チームは関心のあるアラートだけをモニターすることができます。上記の例では、現在1つのアクティブなクリティカルアラートがあります。
チームダッシュボードの説明文はカスタマイズ可能で、チーム固有のリソースへのリンクを含むことができます（Markdownを使用します）。
2. 新しいチームの作成 Splunk のチーム UI を使用するには、左下の » を開き、 Settings → Teams を選択します。
Team を選択すると、現在のチームのリストが表示されます。
新しいチームを追加するには、 Create New Team ボタンをクリックします。これにより、Create New Team ダイアログが表示されます。
独自のチームを作ってみましょう。チーム名を [あなたのイニシャル]-Team のように入力し、あなた自身のユーザー選んで、Add リンクからチームに追加してみましょう。上手くいくと、次のような表示になるはずです。
選択したユーザーを削除するには、Remove または x を押します。
自分のイニシャルでグループを作成し、自分がメンバーとして追加されていることを確認して、 Done をクリックします。
これでチームリストに戻り、自分のチームと他の人が作成したチームが表示されます。
Note 自分がメンバーになっているチームには、グレーの Member アイコンが前に表示されています。
自分のチームにメンバーが割り当てられていない場合は、メンバー数の代わりに青い Add Members のリンクが表示されます。このリンクをクリックすると、Edit Team ダイアログが表示され、自分を追加することができます。
自分のチームの行末にある3つのドット … を押しても、Edit Team と同じダイアログが表示されます。
… メニューでは、チームの編集、参加、離脱、削除を行うことができます（離脱と参加は、あなたが現在メンバーであるかどうかによって異なります）。
3. 通知ルールの追加 チームごとに特定の通知ルールを設定することができます。Notification Policy タブをクリックすると、通知編集メニューが表示されます。
デフォルトでは、システムはチームの一般的な通知ルールを設定する機能を提供します。
Note Email all team members オプションは、アラートの種類に関わらず、このチームのすべてのメンバーにアラート情報のメールが送信されることを意味します。
3.1 受信者の追加 Add Recipient をクリックすると、他の受信者を追加することができます。これらの受信者は Observability Cloud のユーザーである必要はありません。
Configure separate notification tiers for different severity alerts をクリックすると、各アラートレベルを個別に設定できます。
上の画像のように、異なるアラートレベルに対して異なるアラートルールを設定することができます。
Critical と Major は Splunk On-Call インシデント管理ソリューションを使用しています。Minor のアラートはチームの Slack チャンネルに送信し、Warning と Info はメールで送信する、という管理もできるようになります。
3.2 通知機能の統合 Observability Cloud では、アラート通知をメールで送信するだけでなく、以下のようなサービスにアラート通知を送信するように設定することができます。
チームの事情に合わせて、通知ルールを作成してください。
`,description:"",tags:null,title:"チーム",uri:"/ja/imt/servicebureau/teams/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops",content:`このワークショップでは、Splunk Observabilityプラットフォームの以下のコンポーネントを構成するための、基本的なステップを体験できます：
Splunk Infrastructure Monitoring (IM) Splunk APM Endpoint Performance Database Query Performance AlwaysOn Profiling Splunk Real User Monitoring (RUM) Splunk LogObserver ワークショップの中では、Javaのサンプルアプリケーション（Spring Pet Clinic）をクローン（ダウンロード）し、アプリケーションのコンパイル、パッケージ、実行していきます。
アプリケーションを起動すると、OpenTelemetry Javaエージェントを通じて、Splunk APMでメトリクスとトレースが即座に表示されるようになります。
その後、Splunk OpenTelemetry Javascript Libraries (RUM)を使用して、Pet Clinicのエンドユーザーインターフェース（アプリケーションによってレンダリングされるHTMLページ）を計装し、エンドユーザーが実行する個々のクリックとページロードのすべてについて、RUMトレースを生成していきます。
前提条件 このワークショップは、ホスト/インスタンスが提供されるSplunk実行ワークショップ または 自前のホスト/Multipassインスタンス で行う、自己主導型のワークショップです。
ご自身のシステムには、以下のものがインストールされ、有効になっている必要があります：
JDK 17 ポート 8083 が開いていること（インバウンド/アウトバウンド） `,description:"JavaアプリケーションをつかったSplunk Oservabilityのワークショップです",tags:null,title:"Pet Clinic Java ワークショップ",uri:"/ja/other/pet-clinic/index.html"},{breadcrumb:"Splunk Observability Workshops",content:`この テクニカル Splunk Observability Cloud ワークショップでは、 lightweight Kubernetes1 クラスタをベースにした環境を構築します。
ワークショップのモジュールを簡素化するために、あらかじめ設定されたAWS/EC2インスタンスが提供されます。
このインスタンスには、ワークショップに必要となるソフトウェアが予め設定されています。これに対してOpenTelemetery Collector2 を Kubernetes 上でデプロイし、 NGINX3 の ReplicaSet4 をデプロイし、最後に OpenTelemetry を使用して計装されたマイクロサービスベースのアプリケーションをデプロイして、メトリクス、トレース、スパン、ログ5を送信していきます。
さらにこのワークショップでは、ダッシュボード、チャートの編集と作成、アラートを発するためのディテクターの作成、Monitoring as Code および Service Bureau6 についても紹介します。
このテクニカルワークショップを終える頃には、Splunk Observability Cloudの主要な機能や性能を十分に理解していることでしょう。
事前に設定された AWS/EC2 インスタンス へのアクセス方法をご紹介します。
Kubernetes は、コンテナ化されたワークロードやサービスを管理するためのポータブルで拡張可能なオープンソースのプラットフォームで、宣言的な構成と自動化の両方を促進します。 ↩︎
OpenTelemetry Collector は、遠隔測定データの受信、処理、およびエクスポートの方法について、ベンダーに依存しない実装を提供します。さらに、複数のオープンソースまたは商用バックエンドに送信するオープンソースの遠隔測定データ形式（Jaeger、Prometheusなど）をサポートするために、複数のエージェント/コレクターを実行、運用、保守する必要性を排除します。 ↩︎
NGINX は、リバースプロキシ、ロードバランサー、メールプロキシ、HTTPキャッシュとしても使用できるWebサーバーです。 ↩︎
Kubernetes ReplicaSet を使用しています。 ↩︎
Jaeger は、Dapper や OpenZipkin にインスパイアされた、Uber Technologies がオープンソースとして公開している分散型トレースシステムです。マイクロサービスベースの分散システムの監視とトラブルシューティングに使用されています。 ↩︎
Monitoring as Code and Service Bureau を使用しています。 ↩︎
`,description:"オンプレミス、ハイブリッド、マルチクラウドのいずれにおいても、Splunk はリアルタイムの監視とトラブルシューティングを提供し、完全な可視化によってインフラのパフォーマンスを最大化することを支援します。",tags:null,title:"Splunk IM",uri:"/ja/imt/index.html"},{breadcrumb:"",content:`Splunk Observabilityワークショップへようこそ Splunk Observability Cloud の監視、分析、対応ツールを使用して、アプリケーションとインフラストラクチャをリアルタイムで把握することができます。
このワークショップでは、メトリクス、トレース、ログを取り込み、監視し、可視化し、分析するためのクラス最高のオブザーバビリティ（可観測性）プラットフォームについて説明します。
OpenTelemetry このワークショップでOpenTelemetryをアプリケーションやインフラの分析に役立つテレメトリデータ（メトリクス、トレース、ログ）の計装、生成、収集、エクスポートに使用します。
GitHub このドキュメントには、issue や pull request で 貢献 することができます。より良いワークショップにするために、是非ご協力ください。
Twitter SplunkのTwitterチャンネルでは、アップデート情報や興味深い読み物を紹介しています。
Splunk IMオンプレミス、ハイブリッド、マルチクラウドのいずれにおいても、Splunk はリアルタイムの監視とトラブルシューティングを提供し、完全な可視化によってインフラのパフォーマンスを最大化することを支援します。
Splunk APMSplunk APM は、クラウドネイティブ、マイクロサービスベースのアプリケーションのための NoSample™ Full-fidelity アプリケーションパフォーマンス監視およびトラブルシューティングソリューションです。
Splunk RUMエンド・ツー・エンドの可視化により、Webブラウザやネイティブモバイルアプリからバックエンドサービスに至るまで、顧客に影響を与える問題をピンポイントで特定することができます。
Splunk Syntheticsユーザーフロー、ビジネストランザクション、APIにおけるパフォーマンスの問題を積極的に発見、修正し、より良いデジタル体験を提供します。
Ninja WorkshopsPet Clinic Java ワークショップJavaアプリケーションをつかったSplunk Oservabilityのワークショップです OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現するOpenTelemetry Collectorのコンセプトを学び、Splunk Observability Cloudにデータを送信する方法を理解しましょう。
その他のリソースよくある質問とその回答オブザーバビリティ、DevOps、インシデント対応、Splunk On-Callに関連する一般的な質問とその回答を集めました。 ディメンション、プロパティ、タグディメンションとプロパティの比較で、どちらかを使うべきかというのはよく議論されます。 OpenTelemetryとSplunkにおける、タグ付けのための命名規則大規模な組織で OpenTelemetry を展開する際には、タグ付けのための標準化された命名規則を定義し、規則が遵守されるようにガバナンスプロセスを確立することが重要です。
`,description:"Splunk を使用したオブザーバビリティソリューションの構築方法をご紹介します。",tags:null,title:"Splunk Observability Workshops",uri:"/ja/index.html"},{breadcrumb:"Splunk Observability Workshops > その他のリソース",content:`オブザーバビリティ、DevOps、インシデント対応、Splunk On-Callに関連する一般的な質問とその回答を集めました。
Q: アラートとインシデント対応、インシデント管理の違いは？ A: アラート、インシデント対応、インシデント管理は関連する機能です。これらは一緒にインシデント対応および解決プロセスを構成します。
モニタリングやオブザーバビリティのツールはインシデント対応プラットフォームにアラートを送信します。これらのプラットフォームはアラートのコレクションを収集し、それらをインシデントとして相関させます。
これらのインシデントは記録のためにインシデント管理（ITSM）プラットフォームに記録されます。アラートは何かが起こったことを示すトリガーであり、インシデントへのコンテキストを提供します。
インシデントには、アラートの内容、インシデントが作成されてから関連するすべての活動、およびフォローされるオンコールポリシーが含まれます。ITSMは、インシデントがアクティブであるときおよび解決された後のインシデントを記録するシステムです。
インシデント対応および管理をより良く実践するために、これらのコンポーネントが必要になります。
On-Call Q: オブザーバビリティはモニタリングとは違うものですか？ A: モニタリングとオブザーバビリティの主な違いは、「既知の未知」と「未知の未知」の違いです。
モニタリングでは、オペレーターは通常、システムのアーキテクチャと要素に関する事前の知識を持っています。彼らは要素間の関係とそれに関連するメタデータを確実に予測することができます。モニタリングは、頻繁に変更されない状態のインフラストラクチャに適しています。
オブザーバビリティは、オペレーターがシステム内のすべての要素とそれらの関係を予測し、追跡する能力が限定されているシステム向けです。
オブザーバビリティは、従来のメトリクスのモニタリングを含む一連のプラクティスと技術です。
これらのプラクティスと技術を組み合わせることで、オペレーターはシステムのすべての要素に関する事前の知識がなくても、頻繁に変更がある複雑な環境を理解することができます。オブザーバビリティ技術は、環境の変動やメタデータの変化（カーディナリティ）を従来のモニタリングよりもよく考慮できるため、より静的なモニタリングと比較して優れています。
Observability Q: トレースとスパンとは何ですか？ A: トレースとスパンは、メトリクスとログと共に、現代のオブザーバビリティツールにフィードされるコアタイプのデータを構成します。それらは特定の要素と機能を持っていますが、一緒にうまく機能します。
マイクロサービスベースのアーキテクチャは分散しているため、システム内のトランザクションは完了する前に複数のサービスにアクセスします。これにより、問題の場所を正確に特定することが困難になります。トレースは、分散システム内のすべてのサービスを通るリクエストの完全なパスを追跡するための方法です。スパンは、各サービスでの時間のかかる操作です。トレースはスパンの結合したものであり、一緒になると個々のサービスプロセスについてより詳細な情報を提供します。メトリクスはシステムの健康状態の良いスナップショットを提供し、ログは問題を調査する際に深さを提供しますが、トレースとスパンはオペレーターに問題の源泉をより多くのコンテキストでナビゲートするのに役立ちます。これにより、インシデントの調査にかかる時間が節約され、現代のアーキテクチャの複雑さがサポートされます。
APM Q: サイドカーパターンとは何ですか？ A: サイドカーパターンは、関連するサービスをインフラストラクチャによって直接接続するためのデザインパターンです。関連するサービスは、接続されているアプリケーションロジックに機能を追加したりサポートしたりすることができます。これは、管理計画に関連するエージェントをアプリケーションサービスと共に展開する方法として広く使用されます。
オブザーバビリティでは、サイドカーサービスはアプリケーションロジックであり、そのサービスからデータを収集するエージェントです。このセットアップには、アプリケーションサービスを含むコンテナと、エージェントを実行するコンテナの2つが必要です。コンテナはポッドを共有し、ディスク、ネットワーク、名前空間などのリソースを共有します。また、一緒にデプロイされ、同じライフサイクルを共有します。
Observability `,description:"オブザーバビリティ、DevOps、インシデント対応、Splunk On-Callに関連する一般的な質問とその回答を集めました。",tags:null,title:"よくある質問とその回答",uri:"/ja/resources/faq/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk Synthetics",content:`このラボでは Chrome Selenium IDE エクステンションを使用したSplunkデモインスタンスに対する合成トランザクションと、Splunk Synthetic Monitoring Real Browser Check (RBC)を作成します。
1. 前提 https://monitoring.rigor.com と https://optimization.rigor.com にログインできることを確認します。また、 O11y Workshop のようなアカウントにアサインされていることを確認します。
Splunk Synthetic Monitoring アカウントの個人情報を編集し、タイムゾーンとメール通知を編集します。Splunk Synthetic Monitoring はデフォルトで通知しますが、モニターの設定で通知をオフにすることができます。
Chrome Selenium IDE エクステンションをあなたの Chrome ブラウザーに追加します。インストールした後、エクステンションをクリックすることで次の画面が表示されます。
2. Selenium IDE の使用 http://splunk.o11ystore.com にアクセスし、Selenium IDEを使いウェブトランザクションを記録する準備が整いました。
Record a new test in a new project をクリックしプロジェクト名に [あなたのイニシャル] - O11y Store （例：RWC - O11y Store）と入力します。
!!! 質問 「Selenium IDEとは何ですか？」 - Selenium IDE は、オープンソースの Web 用の記録と再生のテスト自動化ツールです。 - SeleniumはWebアプリケーションをテストするためのポータブルなフレームワークです。 - Selenium はテストスクリプト言語 (Selenium IDE) を学ぶ必要なしに機能テストを作成するための再生ツールを提供します。 - C#、Groovy、Java、Perl、PHP、Python、Ruby、Scalaなどの多くの一般的なプログラミング言語でテストを記述するためのテストドメイン固有の言語（Selenese）を提供します。 - テストはほとんどの最新のWebブラウザで実行できます。 - Seleniumは、Windows、Linux、macOS上で動作します。 - Apache License 2.0の下で公開されているオープンソースソフトウェアです。
Base URLに http://splunk.o11ystore.com と入力します。
Start Recording をクリックすると splunk.o11ystore.com が開かれた新しいウインドウが立ち上がります。 Vintage Camera Lens をクリックし、 Add To Cart をクリックし、次に Place Order をクリックします。
ウインドウを閉じ、Selenium IDEに戻りレコーディングを停止します。最後にテストケースに名前を付けます。 [あなたのイニシャル] - Checkout Flow (Desktop) （例：RWC - Checkout Flow (Desktop)）
あなたのSelenium IDEプロジェクトは、このようになります。
再生ボタンを押してレコーディングをテストし、レコーディングがトランザクションを正常に完了することを確認してください。
Selenium IDE プロジェクトをダウンロードフォルダに Workshop.side という名前で保存します。
3. Real Browser Check の作成 https://monitoring.rigor.com からSplunk Synthetic Monitoringにログインします。 REAL BROWSER をクリックし、 +New{: .label-button .sfx-ui-button-blue} をクリックします。
「From File」をクリックしレコーディングファイルを選択し、Importをクリックします。
Frequency を 5 Minutes にセットします。
各Stepをクリックし、次のように分かりやすい名前を付けてあげます。
Step 1: Click Camera
Step 2: Add to Cart
Step 3: Place Order
次に + Add Step をクリックし、バリデーション用のステップを追加します。これはチェックアウトが成功したかどうかを確かめるものです。
Name に Confirm Order と入力し、 Action を Wait for text present に変更し、 Value に Your order is complete! と入力します。ここまでで Start Url と4つのステップが作られました。
Tip Step作成時には非常に強力な Business Transaction 機能の利用もご検討ください。「Business Transactionとは、Real Browserスクリプト内の連続したステップをまとめたものです。これらのトランザクションは、フローの類似部分を論理的にグループ化し、ユーザーは複数のステップとページ（複数可）のパフォーマンスを1つのビジネストランザクションにまとめて表示できるようにします。"
Advanced をクリックし、 Viewport Size が Default desktop: 1366 x 768 であることを確認します。
「Test」をクリックしモニター設定をテストします。テストが正常に完了した後、Step 4の「AFTER」をクリックし、注文完了のスクリーンショットを取得できたことを確認してください。
Create{: .label-button .sfx-ui-button-blue} をクリックし、Real Browser Monitorを保存します。5から10分後にモニターが動作し、以下のようなチェック成功が表示されることを確認します。
Tip Run Now を実行することでモニターを即座に実行できます。
Segment by location をクリックし、見た目の変化を確認してください。クリックすることで各ロケーションのon/offが可能です。
!!! 問題です！ Response Time が一番低いロケーションはどこでしょうか？
成功した円のうちどれかをクリックし、実行結果にドリルダウンします。
CONFIGURE METRICS/HIDE METRICS ドロップダウンで、取得しているメトリクスを確認してみてください。
ドロップダウンの Page 2 をクリックし、 Filmstrip と Waterfall Chart までスクロールダウンして結果を確認してください。
Click Here to Analyze with Optimization をクリックするとSplunk Synthetic Monitoring Optimizationへのログインができます。もし このオプションが表示されない場合 、この ページ にアクセスしてください。
「Best Practices Score」タブをクリックします。スクロールダウンし、結果を確認します。
時間をとって、結果をレビューしてみてください。他の項目もクリックしてみてください。
4. Mobile Check の作成 作成したRBC (Real Browser Check）をコピーします。
名前を RWC - Checkout Flow (Tablet) のように変更します。
Advanced タブ配下で以下の3つの設定を変更し、新しいモバイル用のRBCを作成します。
新しいモニター設定をテスト＆確認します。
Tip Step作成時には非常に強力な Business Transaction 機能の利用もご検討ください。「Business Transactionとは、Real Browserスクリプト内の連続したステップをまとめたものです。これらのトランザクションは、フローの類似部分を論理的にグループ化し、ユーザーは複数のステップとページ（複数可）のパフォーマンスを1つのビジネストランザクションにまとめて表示できるようにします。"
5. リソース Getting Started With Selenium IDE
Splunk Synthetic Monitoring Scripting Guide
How Can I Fix A Broken Script?
Introduction to the DOM (Document Object Model (DOM)
Selenium IDE
`,description:"",tags:null,title:"Real Browser Checks",uri:"/ja/synthetics/real-browser-checks/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk APM > 1. Online Boutiqueのデプロイ",content:` 5分 1. トラフィックを発生させる Online Boutique のデプロイメントには、Locust が動作するコンテナが含まれており、これを使用してウェブサイトに対する負荷トラフィックを生成し、メトリクス、トレース、スパンを生成することができます。
Locust は、EC2インスタンスのIPアドレスの82番ポートで利用できます。ウェブブラウザで新しいタブを開き、 http://<EC2-IP>:82/ にアクセスすると、Locust が動作しているのが確認できます。
Spawn rate を 2 に設定し、Start Swarming をクリックすると、アプリケーションに緩やかな負荷がかかり続けます。
それでは、 Dashboards → All Dashboards → APM Services → Service を開きましょう。
そのためには、アプリケーションの Environment 名を知る必要があります。このワークショップでは、<hostname>-workshop のような Environment 名で定義されています。
ホスト名を調べるには、AWS/EC2インスタンス上で以下のコマンドを実行します:
​ Echo Hostname Output Example echo $(hostname)-workshop bdzx-workshop 前のステップで見つけた Environment を選択し、「frontend」サービスを選択し、時間を「Past 15 minutes」に設定します。
この自動生成されたダッシュボードでは、RED (Rate, Error & Duration) メトリクスを使用して、サービスの状態を監視することができます。このダッシュボードでは、パフォーマンスに関連したさまざまなチャートのほか、基盤となるホストやKubernetesポッド（該当する場合）の相関情報も提供されます。
ダッシュボードの様々なチャートを見てみましょう。
2. Splunk APM のメトリクスを確認する 画面左のメニューからAPMをクリックするとAPM Overviewダッシュボードが表示されます。
右側の Explore を選択し、先ほど見つけた Environment を選択し、時間を15分に設定します。これにより、自動的に生成されたOnline BoutiqueアプリケーションのDependency/Service Mapが表示されます。
以下のスクリーンショットのように表示されます:
ページの下部にある凡例では、依存関係/サービスマップでの表記について説明しています。
サービスリクエスト、エラーレート、ルートエラーレート。 リクエストレート、レイテンシー、エラーレート また、このビューでは、全体的なエラー率とレイテンシー率のタイムチャートを見ることができます。
3. OpenTelemetry ダッシュボード Open Telemetery Collector がデプロイされると、プラットフォームは自動的に OpenTelemetry Collector のメトリクスを表示するダッシュボードを作成します。
左上のナブメニューから、 Dashboards → OpenTelemetry Collector を選択し、メトリクスとスパンが送信されていることを確認しましょう。
4. OpenTelemetry zpages 送信されたトレースをデバッグするには、zpages 拡張機能を使用できます。zpages は OpenTelemetry Collector の一種で、トラブルシューティングや統計用のライブデータを提供します。これらは、EC2インスタンスのIPアドレスのポート 55679 で利用できます。Webブラウザで新しいタブを開き、 http://{==EC2-IP==}:55679/debug/tracez と入力すると、zpages の出力を見ることができます。
また、シェルプロンプトから、テキストベースのブラウザを実行することもできます。
​ Lynx Command lynx http://localhost:55679/debug/tracez `,description:"",tags:null,title:"1.1 Locustでトラフィックを発生させる",uri:"/ja/apm/online-boutique/locust/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk Synthetics",content:`API Checkは、APIエンドポイントの機能およびパフォーマンスをチェックする柔軟な方法を提供します。APIファーストの開発へのシフトにより、フロントエンドのコア機能を提供するバックエンドサービスを監視する必要性が高まっています。複数ステップのAPIインタラクションのテストに興味がある場合でも、エンドポイントのパフォーマンスを可視化したい場合でも、API Checkは目標の達成に役立ちます。
1. グローバル変数の作成 API Checkを行うために使用するグローバル変数を表示します。 Admin Tools の下にある Global Variables をクリックします。 spotifyのAPIトランザクションを行うために使用するグローバル変数を確認してください。
2. API Check の作成 新しい API Check を作成し、<あなたのイニシャル> の後に Splunk REST API Check をつけた名前にします （例: AP - Spotify API）
チェックに名前を付けたら、notificationタブを開いて、どのような設定があるか眺めてみましょう。
次に、以下のAPI Check Stepsを追加します。
変数はこちらから選ぶことができます:
Request Step
リクエストステップは、あるエンドポイントにHTTPリクエストを行い、そのレスポンスからデータを取得します。他のチェックタイプとは異なり、APIチェックでは、チェックを開始するための初期URLは必要ありません。すべてのHTTPリクエストは、リクエストステップ内で設定されます。 Extract Step
Extractステップでは、JSON、XML、HTML形式のデータからデータを抽出します。
JSONからデータを抽出するには、次の3つを用意します:
JSONを含むソース
データを抽出するためのJSONPath式
保存先のカスタム変数名
ソースはどのようなJSONでもかまいませんが、たいていはレスポンスのBodyから取得するでしょう。レスポンスヘッダから取得することもできますし、また、カスタムの値も可能です。ソースは、整形されたJSONでなければなりません。
Save Step
Saveステップでは、チェックの後で再利用するためのデータを保存します。データを保存するには、ソースと保存先のカスタム変数名を指定します。ソースは、応答ヘッダを含むプリセットから選択するか、カスタム値を指定します。
その他の使用例としては、他のステップで簡単に再利用できるように情報を追加したり、リクエストの結果を保存して別のリクエストで再利用できるようにするなどがあります。
リクエスト変数は、リクエストが作成された後にのみ使用可能であることを覚えておくことが重要です。もし、リクエストから値を保存しようとしても、まだリクエストを行っていない場合は、空の文字列が保存されます。
Assert Step
Assertステップは、2つの値に対してアサーションを行います。アサーションを行うには、2つのパラメータと、その2つの比較方法を指定します。 Comparisons
現在、string（文字列）、 numeric（数値）、regular expression（正規表現） の3種類の比較をサポートしています。
string と numeric では、値が比較タイプに強制されます。
reqular expression での比較の場合、最初のパラメータは文字列で、2番目のパラメータは正規表現になります。
API Check に Splunk と API のタグを付けて SAVE します。
3. REST API Checkのテスト edit configuration に戻り、ページの下にある ’test’ を押して、エラーがないことを確認します。
ウィンドウを上にスライドさせると、正常に実行された場合の詳細が表示されます
さて、モニターにもう少し機能を追加してみましょう。詳細ウィンドウを下にスライドさせ、手順5～8を追加します。
BONUS：ステップ6を使用して、以下のレスポンスがタイムリーに戻ってきたことをアサートします（1000 ms)
ステップを追加したら、モニターをテストして保存します。
4. リソース How to Create an API Check
API Check Overview
How Do I Use Business Transactions?
`,description:"",tags:null,title:"API Checks",uri:"/ja/synthetics/api-checks/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > Pet Clinic Java ワークショップ",content:`1. Spring PetClinic アプリケーションを動かす APMをセットアップするためにまず必要なのは…そう、アプリケーションです！この演習では、Spring PetClinicアプリケーションを使用します。これはSpringフレームワーク（Spring Boot）で作られた、非常に人気のあるサンプルJavaアプリケーションです。
まずはPetClinicリポジトリをクローンし、そして、アプリケーションをコンパイル、ビルド、パッケージ、テストしていきます。
git clone https://github.com/spring-projects/spring-petclinicspring-petclinic ディレクトリに移動します:
cd spring-petclinicPetClinic が使用する MySQL データベースを起動します:
docker run -d -e MYSQL_USER=petclinic -e MYSQL_PASSWORD=petclinic -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=petclinic -p 3306:3306 docker.io/mysql:5.7.8そして、Splunk版のOpenTelemetry Java APMエージェントをダウンロードしておきましょう。
curl -L https://github.com/signalfx/splunk-otel-java/releases/latest/download/splunk-otel-javaagent.jar \\ -o splunk-otel-javaagent.jar次に、mavenコマンドを実行してPetClinicをコンパイル/ビルド/パッケージ化します:
./mvnw package -Dmaven.test.skip=true 情報 実際にアプリをコンパイルする前に、mavenが多くの依存ライブラリをダウンロードするため、初回実行時には数分かかるでしょう。2回目以降の実行はもっと短くなります。
そして、以下のコマンドでアプリケーションを実行することができます:
java -javaagent:./splunk-otel-javaagent.jar \\ -Dserver.port=8083 \\ -Dotel.service.name=$(hostname).service \\ -Dotel.resource.attributes=deployment.environment=$(hostname),version=0.314 \\ -Dsplunk.profiler.enabled=true \\ -Dsplunk.profiler.memory.enabled=true \\ -Dsplunk.metrics.enabled=true \\ -jar target/spring-petclinic-*.jar --spring.profiles.active=mysqlアプリケーションが動作しているかどうかは、http://<VM_IP_ADDRESS>:8083 にアクセスして確認することができます。 次に、トラフィックを生成し、クリックしまくり、エラーを生成し、ペットを追加するなどしてください。
-Dotel.service.name=$(hostname).service では、アプリケーションの名前を定義しています。サービスマップ上のアプリケーションの名前等に反映されます。 -Dotel.resource.attributes=deployment.environment=$(hostname),version=0.314 では、Environmentと、versionを定義しています。 deployment.environment=$(hostname) は、Splunk APM UIの上部「Environment」に反映されます。 version=0.314 はここでは、アプリケーションのバージョンを示しています。トレースをドリルダウンしたり、サービスマップの Breakdown の機能で分析したり、Tag Spotlightを開くと version 毎のパフォーマンス分析が使えます。 -Dsplunk.profiler.enabled=true および splunk.profiler.memory.enabled=true では、CPUとメモリのプロファイリングを有効にしています。Splunk APM UIから、AlwaysOn Profilingを開いてみてください。 -Dsplunk.metrics.enabled=true では、メモリやスレッドなどJVMメトリクスの送信を有効にしています。Dashboardsから、APM java servicesを開いてみてください。 その後、Splunk APM UIにアクセスして、それぞれのテレメトリーデータを確認してみましょう！
Troubleshooting MetricSetsを追加する サービスマップやTab Spotlightで、 version などのカスタム属性で分析できるようにするためには、Troubleshooting MetricSetsの設定をあらかじめ追加する必要があります。 左メニューの Settings → APM MetricSets で、設定を管理することができます。 もしお使いのアカウントで分析できなければ、設定を追加してみましょう。
次のセクションではカスタム計装を追加して、OpenTelemetryでは何ができるのか、さらに見ていきます。
`,description:"",tags:null,title:"OpenTelemetry Javaエージェントをインストールする",uri:"/ja/other/pet-clinic/docs/apm/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector レシーバー",content:`Prometheus レシーバー Prometheus のレシーバーも、もちろんあります。Prometheus は OpenTelemetry Collector で使われているオープンソースのツールキットです。このレシーバーは、OpenTelemetry Collector 自身からメトリクスをスクレイピングするためにも使われます。これらのメトリクスは、コレクタの健全性をモニタリングするために使用できる。
ここでは、prometheus レシーバーを変更して、コレクター自身からメトリクスを収集できるようにしてみます。レシーバーの名前を prometheus から prometheus/internal に変更して、レシーバーが何をしているのかをより明確しましょう。設定ファイルを以下のように更新します：
​ Prometheus Receiver Configuration prometheus/internal: config: scrape_configs: - job_name: 'otel-collector' scrape_interval: 10s static_configs: - targets: ['0.0.0.0:8888'] ダッシュボード例 - Prometheus メトリクス このスクリーンショットは、 prometheus/internal レシーバーが OpenTelemetry Collector から収集したメトリクスの、spmeのダッシュボードの例です。ここではスパン・メトリクス・ログの、それぞれの受信および送信の様子を見ることができます。
メモ このダッシュボードはSplunk Observability Cloud にある組み込みダッシュボードで、Splunk OpenTelemetry Collector のインストールの状況を簡単にモニタリングできます。
`,description:"",tags:null,title:"OpenTelemetry Collector レシーバー",uri:"/ja/other/opentelemetry-collector/3-receivers/2-prometheus/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する",content:`さて、OpenTelemetry Collector はインストールできました。次は OpenTelemetry Collector のエクステンション（拡張機能）を見てみましょう。エクステンションはオプションで、主にテレメトリーデータの処理を伴わないタスクで使用できます。例としては、ヘルスモニタリング、サービスディスカバリ、データ転送などがあります。
%%{ init:{ "theme": "base", "themeVariables": { "primaryColor": "#ffffff", "clusterBkg": "#eff2fb", "defaultLinkColor": "#333333" } } }%% flowchart LR; style E fill:#e20082,stroke:#333,stroke-width:4px,color:#fff subgraph Collector A[OTLP] --> M(Receivers) B[JAEGER] --> M(Receivers) C[Prometheus] --> M(Receivers) end subgraph Processors M(Receivers) --> H(Filters, Attributes, etc) E(Extensions) end subgraph Exporters H(Filters, Attributes, etc) --> S(OTLP) H(Filters, Attributes, etc) --> T(JAEGER) H(Filters, Attributes, etc) --> U(Prometheus) end `,description:"",tags:null,title:"OpenTelemetry Collector エクステンション",uri:"/ja/other/opentelemetry-collector/2-extensions/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM",content:` 15分 Splunk Helm chartを使用して、K3s に OpenTelemetry Collector をインストールします Kubernetes Navigatorでクラスタを探索します 1. Access Tokenの取得 Kubernetes が起動したら、Splunk の UI から Access Token1 を取得する必要があります。Access Token は、左下にある » を開き、 Settings → Access Tokens を選択すると表示されます。
主催者が指示したワークショップトークン（例： O11y-Workshop-ACCESS 等）を開き、 Show Token をクリックしてトークンを公開します。 Copy ボタンをクリックし、クリップボードにコピーしてください。 Default のトークンは使用しないでください。
独自のトークンを新たに作成しないようにしてください このワークショップのために設定のトークンを作成し、IngestとAPIの両方の権限を割り当てています。実運用でのベストプラクティスは、1つのTokenにはIngestまたはAPIまたはRUMのような単一のパーミッションを割り当て、必要な場合は複数のトークンを使用することです。
また、Splunk アカウントの Realm2 の名前を取得する必要があります。サイドメニューの最上部の名前をクリックし、Account Settings ページに移動します。Organizations タブをクリックします。Realm はページの中央に表示されています。 この例では「us0」となっています。
2. Helmによるインストール 環境変数 ACCESS_TOKEN と REALM を作成して、進行中の Helm のインストールコマンドで使用します。例えば、Realm が us1 の場合は、export REALM=us1 と入力し、eu0 の場合は、export REALM=eu0 と入力します。
​ Export ACCESS TOKEN export ACCESS_TOKEN="<replace_with_O11y-Workshop-ACCESS_TOKEN>" ​ Export REALM export REALM="<replace_with_REALM>" Splunk Helm チャートを使って OpenTelemetry Collector をインストールします。まず、Splunk Helm chart のリポジトリを Helm に追加してアップデートします。
​ Helm Repo Add Helm Repo Add Output helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update Using ACCESS_TOKEN={REDACTED} Using REALM=eu0 “splunk-otel-collector-chart” has been added to your repositories Using ACCESS_TOKEN={REDACTED} Using REALM=eu0 Hang tight while we grab the latest from your chart repositories… …Successfully got an update from the “splunk-otel-collector-chart” chart repository Update Complete. ⎈Happy Helming!⎈
以下のコマンドでOpenTelemetry Collector Helmチャートをインストールします。これは 変更しないでください。
​ Helm Install Helm Install Output helm install splunk-otel-collector \\ --set="splunkObservability.realm=$REALM" \\ --set="splunkObservability.accessToken=$ACCESS_TOKEN" \\ --set="clusterName=$(hostname)-k3s-cluster" \\ --set="splunkObservability.logsEnabled=true" \\ --set="splunkObservability.profilingEnabled=true" \\ --set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \\ --set="environment=$(hostname)-workshop" \\ splunk-otel-collector-chart/splunk-otel-collector \\ -f ~/workshop/k3s/otel-collector.yaml Using ACCESS_TOKEN={REDACTED} Using REALM=eu0 NAME: splunk-otel-collector LAST DEPLOYED: Fri May 7 11:19:01 2021 NAMESPACE: default STATUS: deployed REVISION: 1 TEST SUITE: None
約30秒程度待ってから kubectl get pods を実行すると、新しいポッドが稼働していることが報告され、デプロイメントの進捗を監視することができます。
続行する前に、ステータスがRunningと報告されていることを確認してください。
​ Kubectl Get Pods Kubectl Get Pods Output kubectl get pods NAME READY STATUS RESTARTS AGE splunk-otel-collector-agent-2sk6k 0/1 Running 0 10s splunk-otel-collector-k8s-cluster-receiver-6956d4446f-gwnd7 0/1 Running 0 10s OpenTelemetry Collector podのログを確認して、エラーがないことを確認します。出力は、以下の出力例にあるログに似ているはずです。
ログを確認するには、helm のインストールで設定したラベルを使用してください（終了するには ctrl+c を押します）。もしくは、インストールされている k9s ターミナル UI を使うとボーナスポイントがもらえます！
​ Kubectl Logs Kubectl Logs Output kubectl logs -l app=splunk-otel-collector -f --container otel-collector 2021-03-21T16:11:10.900Z INFO service/service.go:364 Starting receivers... 2021-03-21T16:11:10.900Z INFO builder/receivers_builder.go:70 Receiver is starting... {"component_kind": "receiver", "component_type": "prometheus", "component_name": "prometheus"} 2021-03-21T16:11:11.009Z INFO builder/receivers_builder.go:75 Receiver started. {"component_kind": "receiver", "component_type": "prometheus", "component_name": "prometheus"} 2021-03-21T16:11:11.009Z INFO builder/receivers_builder.go:70 Receiver is starting... {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"} 2021-03-21T16:11:11.009Z INFO k8sclusterreceiver@v0.21.0/watcher.go:195 Configured Kubernetes MetadataExporter {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster", "exporter_name": "signalfx"} 2021-03-21T16:11:11.009Z INFO builder/receivers_builder.go:75 Receiver started. {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"} 2021-03-21T16:11:11.009Z INFO healthcheck/handler.go:128 Health Check state change {"component_kind": "extension", "component_type": "health_check", "component_name": "health_check", "status": "ready"} 2021-03-21T16:11:11.009Z INFO service/service.go:267 Everything is ready. Begin running and processing data. 2021-03-21T16:11:11.009Z INFO k8sclusterreceiver@v0.21.0/receiver.go:59 Starting shared informers and wait for initial cache sync. {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"} 2021-03-21T16:11:11.281Z INFO k8sclusterreceiver@v0.21.0/receiver.go:75 Completed syncing shared informer caches. {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"} インストールに失敗した場合に削除する OpenTelemetry Collectorのインストールに失敗した場合は、次のようにしてインストールを削除することで、最初からやり直すことができます。
helm delete splunk-otel-collector 3. UI でメトリクスを確認する Splunk の UI で左下の » を開いて Infrastructure をクリックします。
Containers の下にある Kubernetes をクリックして Kubernetes Navigator Cluster Map を開き、メトリクスが送信されていることを確認します。
クラスタが検出され、レポートされていることを確認するには、自分のクラスタを探します（ワークショップでは、他の多くのクラスタが表示されます）。クラスタ名を見つけるには、以下のコマンドを実行し、出力をクリップボードにコピーしてください。
​ Echo Cluster Name echo $(hostname)-k3s-cluster 次に、UIで、Splunkロゴのすぐ下にある「Cluster: - 」メニューをクリックし、先程コピーしたクラスタ名を検索ボックスに貼り付け、チェックボックスをクリックしてクラスタを選択し、最後にメニューのその他の部分をクリックしてフィルタを適用します。
ノードの状態を確認するには、クラスターの淡いブルーの背景にカーソルを置き、左上に表示される青い虫眼鏡をクリックしてください 。 これで、ノードレベルまでドリルダウンできます。 次に、サイドバーボタンをクリックしてサイドバーを開き、Metricsサイドバーを開きます。
サイドのスライダーを使って、CPU、メモリ、ネットワーク、イベントなど、クラスタ/ノードに関連する様々なチャートを見ることができます。
Access Tokens (Org Tokensと呼ばれることもあります)は、長期間利用を前提とした組織レベルのトークンです。デフォルトでは、これらのトークンは 5 年間保存されます。そのため、長期間にわたってデータポイントを送信するエミッターに組み込んだり、Splunk API を呼び出す長期的なスクリプトに使用したりするのに適しています。 ↩︎
Realm とは、Splunk内部の管理単位ので、その中で組織がホストされます。異なる Realm には異なる API エンドポイントがあります (たとえば、データを送信するためのエンドポイントは、us1 realm では ingest.us1.signalfx.com 、eu0 レルムでは ingest.eu0.signalfx.com となります)。このrealm名は、Splunk UI のプロファイルページに表示されます。エンドポイントを指定する際にレルム名を含めない場合、Splunk は us0 レルムを指していると解釈します。 ↩︎
`,description:"",tags:null,title:"OpenTelemetry Collector を Kubernetes に導入する",uri:"/ja/imt/gdi/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk RUM",content:` Online Boutiqueのアドレスを探します Online Boutiqueのウェブショップで買い物しトラフィックを生成させます 1. RUMが有効化されたOnline BoutiqueのURL 前のセクションで説明したように、RUMホスト上で動作するOnline Boutiqueを使用します。 RUMのみのワークショップに参加される方は、使用するシステムは既に準備されていますので、RUMインスタンスのURLを受け取った後、セクション4 Online Boutiqueを使ってシステムに負荷を与える まで進むことができます。
2. RUM Access Token の入手 APMワークショップでサービスをインストールしました。これから、RUM機能もデプロイメントに追加していきます。
まず、RUM Authorization スコープを持つ RUM_ACCESS_TOKEN を取得する必要があります。ワークショップのRUM Access Tokenは、 settings メニューボタンをクリックし、 Access Tokens を選択することで見つけることができます。
講師が使用するように指示したRUMワークショップトークン（例： O11y-Workshop-RUM-TOKEN ）を展開し、 Show Token をクリックしてトークンを表示します。 Copy ボタンをクリックし、クリップボードにコピーしてください。 Default トークンは使用しないでください。トークンのAuthorization ScopeがRUMであることを確認してください。
自分のトークンを作らないでください このワークショップのために、皆さんが行う演習に適した設定をしたRUM Tokenを作成ししています。
進行中のシェルスクリプトで環境変数 RUM_TOKEN を作成し、デプロイメントをパーソナライズします。
​ Export Variables export RUM_TOKEN=<replace_with_O11y-Workshop-RUM-TOKEN> 3. RUMを組み込んだOnline Boutiqueのデプロイ EC2インスタンスのkubernetes（K3s）にOnline Boutiqueのアプリケーションをデプロイするには、元のデプロイメントを削除し、RUM用のapm configスクリプトを実行し、RUMのデプロイメントを適用します。
​ Deploy Online Boutique with RUM Partial Deployment Output cd ~/workshop/apm kubectl delete -f deployment.yaml kubectl apply -f deployment.yaml ...... Adding RUM_TOKEN to deployment deployment.apps/recommendationservice created service/recommendationservice created deployment.apps/productcatalogservice created service/productcatalogservice created deployment.apps/cartservice created service/cartservice created deployment.apps/adservice created service/adservice created deployment.apps/paymentservice created service/paymentservice created deployment.apps/loadgenerator created service/loadgenerator created deployment.apps/shippingservice created service/shippingservice created deployment.apps/currencyservice created service/currencyservice created deployment.apps/redis-cart created service/redis-cart created deployment.apps/checkoutservice created service/checkoutservice created deployment.apps/frontend created service/frontend created service/frontend-external created deployment.apps/emailservice created service/emailservice created deployment.apps/rum-loadgen-deployment created 変数未セットに関するメッセージが表示された場合 kubectl delete -f deployment.yaml コマンドを実行しAPM環境のデプロイ削除します。 次にガイド、メッセージに表示されていた変数をexportし上記のデプロイスクリプトを再実行します。
4. Online Boutiqueを使ってシステムに負荷を与える 皆さんと一緒にOnline Boutiqueに接続し買い物をシミュレートする合成ユーザーもいます。これにより、複数の場所からのトラフィックが発生し、よりリアルなデータが得られます。
ワークショップ講師からURLを受け取っているはずです。 新しいWebブラウザを立ち上げ http://{==RUM-HOST-EC2-IP==}:81/ にアクセスするとRUMが有効化されたOnline Boutiqueが表示されます。
5. トラフィックを発生させる この演習の目的は、RUMが有効化されたOnline Boutiqueを閲覧し、さまざまな商品と数量の組み合わせで購入することです。 さらに別のブラウザやスマートフォンからアクセスすることもできます。
これにより複数のセッションが作成され、調査することができます。じっくりと吟味して、いろいろな商品を購入しカートに入れてください。
Home Barista Kitかっこよくないですか？… ショッピングを楽しんでください！
`,description:"",tags:null,title:"2. Online BoutiqueでのRUMの利用例",uri:"/ja/rum/2-showcase/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk APM > 2. トレースとスパン",content:`サービスマップ サービスマップの paymentservice をクリックし、paymentservice の下にあるbreakdownのドロップダウンフィルタから version を選択します。これにより、カスタムスパンタグの version でサービスマップがフィルタリングされます。
これで、サービスマップが以下のスクリーンショットのように更新され、paymentservice の異なるバージョンが表示されていることがわかります。
`,description:"",tags:null,title:"2.1 サービスマップ",uri:"/ja/apm/using-splunk-apm/service_map/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector エクステンション",content:`Performance Profiler エクステンション Performance Profiler エクステンションは、Go の net/http/pprof エンドポイントを有効化します。これは通常、開発者がパフォーマンスプロファイルを収集し、サービスの問題を調査するために使用します。このワークショップでは詳しく紹介はしません。
`,description:"",tags:null,title:"OpenTelemetry Collector エクステンション",uri:"/ja/other/opentelemetry-collector/2-extensions/2-performance/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM > ダッシュボードを利用する",content:`1. チャートの保存 チャートの保存するために、名前と説明をつけましょう。チャートの名前 Copy of Latency Histogram をクリックして、名前を “現在のレイテンシー” に変更します。
説明を変更するには、 Spread of latency values across time. をクリックし、 リアルタイムでのレイテンシー値 に変更します。
Save As ボタンをクリックします。チャートに名前が付いていることを確認します。前のステップで定義した 現在のレイテンシー という名前が使用されますが、必要に応じてここで編集することができます。
Ok ボタンを押して続行します。
2. ダッシュボードの作成 Choose dashboard ダイアログでは、新しいダッシュボードを作成する必要があります。 New Dashboard ボタンをクリックしてください。
これで、New Dashboard ダイアログが表示されます。ここでは、ダッシュボードの名前と説明を付け、Write Permissions で書き込み権限を設定します。
ダッシュボードの名前には、自分の名前を使って YOUR_NAME-Dashboard の形式で設定してください。
YOUR_NAME を自分の名前に置き換えてから、編集権限をEveryone can Read or Write からRestricted Read and Write access に変更してみてください。
ここには、自分のログイン情報が表示されます。つまり、このダッシュボードを編集できるのは自分だけということになります。もちろん、ダッシュボードやチャートを編集できる他のユーザーやチームを下のドロップボックスから追加することもできますが、今回は、Everyone can Read or Write に 再設定 して制限を解除し、 Save ボタンを押して続行してください。
新しいダッシュボードが利用可能になり、選択されましたので、チャートを新しいダッシュボードに保存することができます。
ダッシュボードが選択されていることを確認して、 Ok ボタンを押します。
すると、下図のようにダッシュボードが表示されます。左上に、YOUR_NAME-DASHBOARD がダッシュボードグループ YOUR_NAME-Dashboard の一部であることがわかります。このダッシュボードグループに他のダッシュボードを追加することができます。
3. チームページへの追加 チームに関連するダッシュボードは、チームページにリンクさせるのが一般的です。そこで、後で簡単にアクセスできるように、ダッシュボードをチームページに追加してみましょう。 ナビバーのアイコンを再びクリックします。 これでチームダッシュボードに遷移します。ここでは、チーム Example Team を例にしていますが、ワークショップのものは異なります。
を押し、 Add Dashboard Group ボタンを押して、チームページにダッシュボードを追加します。
すると、 Select a dashboard group to link to this team ダイアログが表示されます。 検索ボックスにご自身のお名前（上記で使用したお名前）を入力して、ダッシュボードを探します。ダッシュボードがハイライトされるように選択し、Ok ボタンをクリックしてダッシュボードを追加します。
ダッシュボードグループがチームページの一部として表示されます。ワークショップを進めていくと、さらに多くのダッシュボードがここに表示されていくはずです。
次のモジュールでは、ダッシュボードのリンクをクリックして、チャートをさらに追加していきます！
`,description:"",tags:null,title:"チャートを保存する",uri:"/ja/imt/dashboards/savingcharts/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector プロセッサー",content:`Resource Detection プロセッサー resourcedetection プロセッサーは、ホストからリソース情報を検出して、テレメトリーデータ内のリソース値をこの情報で追加または上書きすることができます。
デフォルトでは、可能であればホスト名を FQDN に設定し、そうでなければ OS が提供するホスト名になります。このロジックは hostname_sources オプションを使って変更できます。FQDN を取得せず、OSが提供するホスト名を使用するには、hostname_sourcesをosに設定します。
​ System Resource Detection Processor Configuration processors: batch: resourcedetection/system: detectors: [system] system: hostname_sources: [os] If the workshop instance is running on an AWS/EC2 instance we can gather the following tags from the EC2 metadata API (this is not available on other platforms). ワークショップのインスタンスが AWS/EC2 インスタンスで実行されている場合、EC2 のメタデータ API から以下のタグを収集します（これは他のプラットフォームでは利用できないものもあります）。
cloud.provider ("aws") cloud.platform ("aws_ec2") cloud.account.id cloud.region cloud.availability_zone host.id host.image.id host.name host.type これらのタグをメトリクスに追加するために、別のプロセッサーとして定義してみましょう。
​ EC2 Resource Detection Processor Configuration processors: batch: resourcedetection/system: detectors: [system] system: hostname_sources: [os] resourcedetection/ec2: detectors: [ec2] `,description:"",tags:null,title:"OpenTelemetry Collector プロセッサー",uri:"/ja/other/opentelemetry-collector/4-processors/2-resource-detection/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector サービス",content:`Prometheus Internal レシーバー ワークショップの前半で、prometheus レシーバーの名前を変更し、コレクター内部のメトリクスを収集していることを反映して、prometheus/internal という名前にしました。
現在、メトリクスパイプラインの下で prometheus/internal レシーバーを有効にする必要があります。metrics パイプラインの下の receivers セクションを更新して、prometheus/internal を含めます：
service: pipelines: traces: receivers: [otlp, opencensus, jaeger, zipkin] processors: [batch] exporters: [logging] metrics: receivers: [hostmetrics, otlp, opencensus, prometheus/internal] processors: [batch] exporters: [logging]`,description:"",tags:null,title:"OpenTelemetry Collector サービス",uri:"/ja/other/opentelemetry-collector/6-service/2-prometheus/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM > 管理機能",content:` 個別のアクセストークンを作成し、制限を設けることで利用を制限する方法を紹介します 1. アクセストークン ホスト、コンテナ、カスタムメトリクス、高解像度メトリクスの使用量をコントロールしたい場合は、複数のアクセストークンを作成し、組織内の異なる部分に割り当てることができます。
左下の » を開いて、General Settings 配下の Settings → Access Tokens を選択します。
Access Tokens インターフェースでは、生成されたアクセストークンのリストで概要が表示されます。すべての組織では、最初のセットアップ時に Default のトークンが生成され、その他のトークンを追加・削除できるようになっています。
各トークンは一意であり、消費できるホスト、コンテナ、カスタムメトリクス、高解像度メトリクスの量に制限を設けることができます。
Usage Status 欄は、トークンが割り当てられた制限値を上回っているか下回っているかを素早く表示します。
2. 新しいトークンの作成 New Token ボタンをクリックして、新しいトークンを作成しましょう。Name Your Access Token ダイアログが表示されます。
ここでは、Ingest Token と API Token の両方のチェックボックスにチェックを入れてください。
OK を押すと、Access Token のUIに戻ります。ここでは、既存のトークンの中に、あなたの新しいトークンが表示されているはずです。
名前を間違えたり、トークンを無効/有効にしたり、トークンの制限を設定したい場合は、トークンの制限の後ろにある省略記号(…)のメニューボタンをクリックして、トークンの管理メニューを開きます。
タイプミスがあった場合は、Rename Token オプションを使用して、トークンの名前を修正することができます。
3. トークンの無効化 トークンがメトリクスの送信に使用できないようにする必要がある場合は、トークンを無効にすることができます。
Disable ボタンを押すことで、トークンを無効化できます。これにより、トークンがSplunk Observability Cloudへのデータ送信に使用できなくなります。
以下のスクリーンショットのように、トークンの行がグレーになり、無効化されたことを示しています。
省略記号(…)のメニューボタンをクリックして、トークンの無効化と有効化を行ってください。
4. トークンの使用制限の管理 … メニューの Manage Token Limit をクリックして、使用量を制限してみましょう。
トークン制限管理ダイアログが表示されます。
このダイアログでは、カテゴリごとに制限を設定することができます。
先に進み、各使用指標に対して以下のように制限を指定してください。
リミット 値 ホストの制限 5 コンテナ制限 15 カスタムメトリクスの制限 20 高解像度メトリックの制限 0 また、上の表に示すように、ダイアログボックスに正しい数字が表示されていることを再確認してください。
トークンリミットは、5分間の使用量がリミットの90％を超えたときに、1人または複数の受信者に通知するアラートのトリガーとして使用されます。
受信者を指定するには、 Add Recipient をクリックして、使用する受信者または通知方法を選択します（受信者の指定は任意ですが、強くお勧めします）。
トークンアラートの重要度は常に「Critical」です。
Update をクリックすると、アクセストークンの制限とアラートの設定が保存されます。
Note: トークンの上限を超えると、何が起こるのか トークンが使用カテゴリの上限に達したとき、または上限を超えたとき、その使用カテゴリの新しいメトリクスはObservability Cloudに保存されず、処理されません。これにより、チームが無制限にデータを送信することによる予期せぬコストが発生しないようになります。
Note: 高度なアラート通知 90%に達する前にアラートを取得したい場合は、必要な値を使用して追加のディテクターを作成できます。これらのディテクターは、特定のアクセストークンを消費しているチームをターゲットにすることができ、管理者が関与する必要がある前に行動を起こすことができます。
これらの新しいアクセストークンを様々なチームに配布し、Observability Cloudに送信できる情報やデータの量をコントロールできるようになります。
これにより、Observability Cloudの使用量を調整することができ、過剰な使用を防ぐことができます。
おめでとうございます！ これで、管理機能のモジュールは終わりです！
`,description:"",tags:null,title:"使用量を管理する",uri:"/ja/imt/servicebureau/tokens/index.html"},{breadcrumb:"Splunk Observability Workshops",content:`Splunk APM は、クラウドネイティブなマイクロサービスベースのアプリケーション向けの NoSample™ で 完全忠実なアプリケーションパフォーマンスモニタリングおよびトラブルシューティングソリューションです。
サンプリングされた部分的な情報ではなく、すべてのトレースを収集することで、異常が検出されないことはありません。ユーザーがエラーを経験しても、通常より長いレイテンシーを経験しても、数秒以内にそれを知り、対処することができます。ときに、悪い動作がエラーとして扱われないこともあります。開発者が新しいアプリケーションを作成する際には、そのカナリアリリースが期待通りの結果をもたらすかどうかを知る必要があります。すべてのトレースデータを収集して、初めて、クラウドネイティブアプリケーションが想定通り動作していることを確信できるようになります。
インフラとアプリケーションのパフォーマンスは相互に依存しています。全体像を把握するために、Splunk APM はクラウドのインフラとその上で動作するマイクロサービスをシームレスに相関付けます。メモリリーク、ノイズの多い隣のコンテナ、その他のインフラ関連の問題が原因でアプリケーションが動作した場合、Splunk がすぐに知らせてくれます。さらに、Splunk のログやイベントにインコンテキストでアクセスすることで、より詳細なトラブルシューティングや根本原因の分析が可能になります。
1. Online BoutiqueのデプロイOnline BoutiqueアプリケーションをKubernetes（K3s）にデプロイし、Locustを使って人工的なトラフィックを発生させます。
2. トレースとスパンSplunk APMの概要と使用方法
`,description:"Splunk APM は、クラウドネイティブ、マイクロサービスベースのアプリケーションのための NoSample™ Full-fidelity アプリケーションパフォーマンス監視およびトラブルシューティングソリューションです。",tags:null,title:"Splunk APM",uri:"/ja/apm/index.html"},{breadcrumb:"Splunk Observability Workshops > その他のリソース",content:`メトリクスにコンテキストを与える ディメンションとプロパティの違いや、どちらを使うべきかというのは、よく話題にされます。それぞれの説明から始めるのではなく、私たちがどのように使い、どのように似ているのかを理解してから、それぞれの違いや、なぜどちらかを使うのかの例を見ていくことにしましょう。
ディメンションとプロパティの類似点 最も単純な答えは、ディメンションとプロパティはともに、メトリクスにコンテキスト（状況）を追加するメタデータの key:value ペアであるということです。メトリクス自体は、cpu.utilization のような標準的なインフラストラクチャメトリクスであろうと、API呼び出しの回数のようなカスタムメトリクスであろうと、実際に測定しているものなら全てに当てはまります。
cpu.utilization メトリクスの値が50%であっても、それがどこから来たのかなどのコンテキストを知らなければ、それは単なる数字であり、私たちにとって有用ではありません。少なくとも、どのホストから来たのかを知る必要があります。
現在では、個々のホストのパフォーマンスや利用率よりも、クラスターやデータセンター全体のパフォーマンスや利用率をより気にすることが多く、ホストのクラスター全体の平均 cpu.utilization、あるホストの cpu.utilization が同じサービスを実行する他のホストと比べて外れ値である場合、あるいは環境間での平均 cpu.utilization を比較することに興味を持っています。
このように cpu.utilization メトリクスをスライス、集約、またはグループ化するためには、受け取る cpu.utilization メトリクスのメタデータに、ホストが属するクラスター、ホスト上で実行されているサービス、およびそれが属する環境などの情報が必要です。このメタデータは、ディメンションまたはプロパティの key:value ペアの形で存在することができます。
例えば、ダッシュボードでフィルターを適用したり、分析関数を実行する際にグループ化機能を使用したりするとき、プロパティまたはディメンションを使用することができます。
では、ディメンションとプロパティはどう違うの？ ディメンションはメトリクスと共に取り込み時に送信されるのに対し、プロパティは取り込み後にメトリクスやディメンションに適用されます。これは、\`cpu.utilization\`\` の値がどのホストから来ているかのような、データポイント（メトリクスの単一の報告値）をユニークにするために必要なメタデータはディメンションでなければならないことを意味します。メトリクス名 + ディメンションは MTS（メトリクスの時間系列）をユニークに定義します。
例：特定のホスト（server1）によって送信される cpu.utilization メトリクスで、ディメンション host:server1 があれば、それはユニークな時間系列と見なされます。もし 10 台のサーバーがそのメトリクスを送信していれば、メトリクス名 cpu.utilization を共有し、ディメンションのキー値ペア（host:server1, host:server2…host:server10）でユニークに識別される 10 の時間系列があります。
しかし、サーバー名がデータセンター内でのみユニークである場合、データセンターの場所を示す 2 番目のディメンション dc を追加する必要があります。これにより、可能な MTS の数は倍になります。受信された cpu.utilization メトリクスは、2 組のディメンションのキー値ペアによってユニークに識別されます。
cpu.utilization に dc:east と host:server1 を加えたものは、cpu.utilization に dc:west と host:server1 を加えたものとは異なる時間系列を作り出します。
ディメンションは不変だが、プロパティは可変である 上記で述べたように、メトリクス名 + ディメンションの組み合わせで、ユニークな MTS を作ります。したがって、ディメンションの値が変わると、メトリクス名 + ディメンション値の新しいユニークな組み合わせが生まれ、新しい MTS が作成されます。
一方、プロパティはメトリクス（またはディメンション）が取り込まれた後に適用されます。メトリクスにプロパティを適用すると、そのメトリクスが属するすべての MTS に伝播して適用されます。または、ディメンションにプロパティを適用する場合、例えば host:server1 とすると、そのホストからのすべてのメトリクスにそのプロパティが添付されます。プロパティの値を変更すると、そのプロパティが添付されているすべての MTS のプロパティ値が更新されます。これが重要な理由は何でしょうか？ プロパティの歴史的な値にこだわる場合、それをディメンションにする必要があることを意味しています。
例：私たちはアプリケーションに関するカスタムメトリクスを収集しています。1つのメトリクスは latency で、アプリケーションへのリクエストのレイテンシーをカウントします。顧客ごとにレイテンシーを分類して比較できるように customer ディメンションを持っています。私たちは、顧客が使用しているバージョン別にアプリケーションの latency を分類して比較したいと考え、プロパティ version を customer ディメンションに添付しました。最初はすべての顧客がアプリケーションバージョン1を使用しているので、version:1 です。
現在、いくつかの顧客がアプリケーションのバージョン2を使用しているため、それらの顧客に対してプロパティを version:2 に更新します。これらの顧客の version プロパティの値を更新すると、その顧客に関連するすべての MTS に伝播します。これにより、これらの顧客が以前に version:1 を使用していたという歴史が失われるため、歴史的な期間にわたって version:1 と version:2 の latency を比較する場合、正確なデータを得ることはできません。この場合、メトリクスの時間系列をユニークにするためにアプリケーションの version が必要ではないかもしれませんが、歴史的な値にこだわるために version をディメンションにする必要があります。
結局、いつ、ディメンションじゃなくてプロパティを使うの？ メトリクスに添付したいメタデータがあるが、取り込み時にはそれを知らない場合が第一の理由です。第二の理由は、ベストプラクティスとして、ディメンションである必要がなければ、それをプロパティにすることです。なぜでしょうか？
一つの理由は、現在、分析ジョブやチャートレンダリングあたりの MTS の上限が 5K であり、ディメンションが多いほど多くの MTS を生成することです。プロパティは完全に自由形式であり、MTS の数を増やすことなく、メトリクスやディメンションに必要な情報を追加することができます。
ディメンションは各データポイントと共に送信されるため、ディメンションが多いほど、より多くのデータを送信することになります。これは、クラウドプロバイダーがデータ転送に料金を請求する場合、コストが高くなる可能性があります。
プロパティを使う良い例としては、ホスト情報の追加などがあります。 machine_type, processor, os などの情報を確認することが重要ですが、これらをディメンションとして設定し、各ホストからのすべてのメトリクスと共に送信するのではなく、プロパティとして設定し、ホストディメンションに添付することができます。
例えば host:server1 では、プロパティ machine_type:ucs, processor:xeon-5560, os:rhel71 を設定します。host:server1 というディメンションを持つメトリクスが入ってくるたびに、上記のすべてのプロパティが自動的に適用されます。
プロパティの使用例としては、各サービスのエスカレーション連絡先や、各顧客の SLA レベルを知りたい場合があります。これらの項目は、メトリクスをユニークに識別するために必要ではなく、歴史的な値にも関心がないため、プロパティにすることができます。プロパティはサービスディメンションや顧客ディメンションに追加され、これらのディメンションを持つすべてのメトリクスや MTS に適用されます。
タグについてはどうですか？ タグは、メトリクスにコンテキストを与えたり整理するのに使われる、メタデータの 3 番目のタイプです。ディメンションやプロパティとは異なり、タグは key:value ペアではありません。タグはラベルやキーワードとして考えることができます。プロパティと同様に、タグは取り込み後に UI の Catalog や API を通じてプログラム的にデータに適用されます。タグはメトリクス、ディメンション、ディテクターなどの他のオブジェクトに適用することができます。
タグを使う場面はどこですか？ タグが必要とされるのは、タグとオブジェクトの間に多対一の関係がある場合や、タグとそれに適用されるオブジェクト間に一対多の関係がある場合です。本質的に関連していないメトリクスをまとめるのに役立ちます。
例として、複数のアプリケーションを実行しているホストがある場合です。各アプリケーションに対してタグ（ラベル）を作成し、それぞれのホストに複数のタグを適用して、その上で実行されているアプリケーションをラベル付けします。
例：Server1 は 3 つのアプリケーションを実行しています。タグ app1, app2, app3 を作成し、ディメンション host:server1 にこれら 3 つのタグをすべて適用します。
上記の例を拡張すると、アプリケーションからのメトリクスも収集しているとします。作成したタグを、アプリケーション自体から来るメトリクスに適用することができます。タグに基づいてフィルタリングすることで、アプリケーションに基づいてフィルタリングしながら、アプリケーションと関連するホストメトリクスの全体像を得ることができます。
例：App1 は service:application1 というディメンションでメトリクスを送信します。service:application1 のディメンションにタグ app1 を適用します。その後、チャートやダッシュボードでタグ app1 でフィルタリングすることができます。
タグの他の使用例には、単一の可能な値を持つ二進状態があります。例として、カナリアテストを行い、カナリアデプロイを行った際に新しいコードを受け取ったホストをマークして、新しいコードを受け取らなかったホストとのパフォーマンスを比較しやすくすることがあります。単一の値 canary しかないため、key:value ペアは必要ありません。
ただし、タグでフィルタリングはできますが、groupBy 関数では使用できないことに注意してください。groupBy 関数は key:value ペアのキー部分を指定して実行され、そのキーの値に基づいて結果がグループ化されます。
さらなる情報 カスタムメトリクスのディメンションを送信する方法に関する情報については、お使いのライブラリに関するクライアントライブラリのドキュメントをご覧ください。
API を通じてメトリクスやディメンションにプロパティやタグを適用する方法については、 /metric/:name、/dimension/:key/:value に関する API ドキュメントを参照してください。
UI のメタデータカタログでプロパティやタグを追加または編集する方法については、Search the Metric Finder and Metadata catalogで、​Add or edit metadata セクションをご覧ください。
`,description:"ディメンションとプロパティの比較で、どちらかを使うべきかというのはよく議論されます。",tags:null,title:"ディメンション、プロパティ、タグ",uri:"/ja/resources/dimensions_properties_tags/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk APM",content:` 15分 APM の概要 - RED メトリクス サービスマップを利用する タグスポットライトの紹介 トレースの例 インフラとのリンク トレースとスパンについて トレースは、同じトレースIDを共有するスパンの集合体であり、アプリケーションとその構成サービスが処理する固有のトランザクションを表します。
各スパンには、そのスパンでキャプチャされた操作を表す名前と、その操作がどのサービス内で行われたかを表すサービス名があります。
さらにスパンは、その親として別のスパンを参照することができ、そのトランザクションを処理するために実行されたトレースでキャプチャされた処理の関係を定義します。
各スパンには、キャプチャされたメソッド、オペレーション、コードブロックに関する以下のような多くの情報が含まれています。例えば:
処理名 処理の開始時間（マイクロ秒単位の精度） 処理の実行時間（マイクロ秒単位の精度） 処理が行われたサービスの論理名 処理が行われたサービスインスタンスのIPアドレス `,description:"Splunk APMの概要と使用方法",tags:null,title:"2. トレースとスパン",uri:"/ja/apm/using-splunk-apm/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM > OpenTelemetry Collector を Kubernetes に導入する",content:` NGINX ReplicaSet を K3s クラスタにデプロイし、NGINX デプロイメントのディスカバリーを確認します。 負荷テストを実行してメトリクスを作成し、Splunk Observability Cloudにストリーミングすることを確認します！ 1. NGINX の起動 Splunk UI で WORKLOADS タブを選択して、実行中の Pod の数を確認します。これにより、クラスタ上のワークロードの概要がわかるはずです。
デフォルトの Kubernetes Pod のうち、ノードごとに実行されている単一のエージェントコンテナに注目してください。この1つのコンテナが、このノードにデプロイされているすべての Pod とサービスを監視します！
次に、MAP タブを選択してデフォルトのクラスタノードビューに戻し、再度クラスタを選択します。
Multipass または AWS/EC2 のシェルセッションで、nginx ディレクトリに移動します。
​ Change Directory cd ~/workshop/k3s/nginx 2. NGINXのデプロイメント作成 NGINX の ConfigMap1 を nginx.conf ファイルを使って作成します。
​ Kubectl Configmap Create Kubectl Create Configmap Output kubectl create configmap nginxconfig --from-file=nginx.conf configmap/nginxconfig created 続いて、デプロイメントを作成します。
​ Kubectl Create Deployment Kubectl Create Deployment Output kubectl create -f nginx-deployment.yaml deployment.apps/nginx created service/nginx created
次に、NGINXに対する負荷テストを作成するため、 Locust2 をデプロイします。
​ Kubectl Create Deployment Kubectl Create Deployment Output kubectl create -f locust-deployment.yaml deployment.apps/nginx-loadgenerator created service/nginx-loadgenerator created デプロイメントが成功し、Locust と NGINX Pod が動作していることを確認しましょう。
Splunk UI を開いていれば、新しい Pod が起動し、コンテナがデプロイされているのがわかるはずです。
Pod が実行状態に移行するまでには 20 秒程度しかかかりません。Splunk UIでは、以下のようなクラスタが表示されます。
もう一度 WORKLOADS タブを選択すると、新しい ReplicaSet と NGINX 用のデプロイメントが追加されていることがわかります。
これをシェルでも検証してみましょう。
​ Kubectl Get Pods Kubectl Get Pods Output kubectl get pods NAME READY STATUS RESTARTS AGE splunk-otel-collector-k8s-cluster-receiver-77784c659c-ttmpk 1/1 Running 0 9m19s splunk-otel-collector-agent-249rd 1/1 Running 0 9m19s svclb-nginx-vtnzg 1/1 Running 0 5m57s nginx-7b95fb6b6b-7sb9x 1/1 Running 0 5m57s nginx-7b95fb6b6b-lnzsq 1/1 Running 0 5m57s nginx-7b95fb6b6b-hlx27 1/1 Running 0 5m57s nginx-7b95fb6b6b-zwns9 1/1 Running 0 5m57s svclb-nginx-loadgenerator-nscx4 1/1 Running 0 2m20s nginx-loadgenerator-755c8f7ff6-x957q 1/1 Running 0 2m20s 3. Locust の負荷テストの実行 Locust はオープンソースの負荷テストツールで、EC2 インスタンスの IP アドレスの8083番ポートで Locust が利用できるようになりました。Webブラウザで新しいタブを開き、http://{==EC2-IP==}:8083/にアクセスすると、Locust が動作しているのが確認できます。
Spawn rate を 2 に設定し、Start Swarming をクリックします。
これにより、アプリケーションに緩やかな連続した負荷がかかるようになります。
上記のスクリーンショットからわかるように、ほとんどのコールは失敗を報告しています。これはアプリケーションをまだデプロイしていないため予想されることですが、NGINXはアクセス試行を報告しており、これらのメトリックも見ることができます。
サイドメニューから Dashboards → Built-in Dashboard Groups → NGINX → NGINX Servers を選択して、UIにメトリクスが表示されていることを確認します。さらに Overrides フィルターを適用して、 k8s.cluster.name: に、ターミナルの echo $(hostname)-k3s-cluster で返されるクラスタの名前を見つけます。
ConfigMap とは、キーと値のペアで非機密データを保存するために使用される API オブジェクトです。Pod は、環境変数、コマンドライン引数、またはボリューム内の構成ファイルとして ConfigMap を利用することができます。ConfigMap を使用すると、環境固有の構成をコンテナイメージから切り離すことができるため、アプリケーションの移植が容易になります。 ↩︎
Locust とは？. ↩︎
`,description:"",tags:null,title:"K3s に NGINX をデプロイする",uri:"/ja/imt/gdi/nginx/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk APM > 2. トレースとスパン",content:`タグスポットライト 画面の右側にある Tag Spotlight をスクロールダウンし、ドロップダウンから Top Across All Indexed Tags を選択します。選択したら、下のスクリーンショットにあるように をクリックします。
タグスポットライトのページが表示されます。このページでは、アプリケーションの上位のタグと、それに対応するエラー率や秒間リクエスト数を確認できます。
version スパンタグでは、バージョン 350.10 のエラー率が100%であることがわかります。また、tenant.level スパンタグでは、3つのテナント（Gold、Silver、Bronze）すべてにエラーがあることがわかります。
タグスポットライトのページはインタラクティブに、目的のタグをクリックするだけでフィルタとしてタグを追加することができます。tenant.level の下の gold をクリックして、フィルターとして追加します。これを行うと、ページには tenant.level が gold のデータのみが表示されます。
タグスポットライトは、データを分析して傾向を見極めるのに非常に便利です。Gold Tenantでは、リクエストの総数のうち55件がエラーであることがわかります。（この数字はワークショップの実施時刻により異なります）
これをバージョンタグと関連付けると、バージョン 350.10 が55件、バージョン 350.9 が17件のリクエストに対応していることがわかります。つまり、バージョン 350.10 を経由したリクエストは、すべてエラー状態になったということになります。
paymentservice のバージョン 350.10 からのすべてのリクエストがエラーになるというこの理論をさらに検証するために、タグセレクタを使用して、フィルタを別のテナントに変更することができます。フィルターを gold テナントから silver テナントに変更します。
ここで、silver テナントのエラーのあるリクエスト数を見て、バージョン番号と相関させることで、同様の分析を行うことができます。silver テナントのエラー数は、バージョン 350.10 のリクエスト数と一致していることに注目してください。
タグスポットライトでは、秒間リクエスト数やエラー率だけでなく、サービスごとのレイテンシーも見ることができます。これを行うには、レイテンシーボタンを選択し、silver テナントタグを削除することで、すべての paymentservice のレイテンシーを確認することができます。
右端の Clear All の下にある X ボタンを押して、サービスマップに戻りましょう。
`,description:"",tags:null,title:"2.2 Tag Spotlight",uri:"/ja/apm/using-splunk-apm/tag_spotlight/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector エクステンション",content:`zPages エクステンション zPages は、外部エクスポータに代わるプロセス内部の機能です。有効化すると、バックグラウンドでトレースとメトリクス情報を収集し、集計し、どのようなデータを扱ったかの Web ページを公開します。zpages は、コレクターが期待どおりに動作していることを確認するための非常に便利な診断機能です。
​ ServiceZ PipelineZ ExtensionZ ServiceZ は、コレクターサービスの概要と、pipelinez、extensionz、featurez zPages へのクイックアクセスを提供します。このページでは、ビルドとランタイムの情報も提供します。
URL: http://localhost:55679/debug/servicez (localhost は、適切なホスト名に切り替えてください)
PipelineZ は、コレクターで実行中のパイプラインに関する情報を提供します。タイプ、データが変更されているか、各パイプラインで使用されているレシーバー、プロセッサー、エクスポーターの情報を見ることができます。
URL: http://localhost:55679/debug/pipelinez (localhost は、適切なホスト名に切り替えてください)
ExtensionZ は、コレクターで有効化されたエクステンションを確認できます。
Example URL: http://localhost:55679/debug/extensionz (localhost は、適切なホスト名に切り替えてください)
情報 ついていけない場合は、ブラウザーでzPagesの情報を発信しているテスト環境にアクセスしてください：
ServiceZ: http://63.33.64.193:55679/debug/servicez PipelineZ: http://63.33.64.193:55679/debug/pipelinez ExtensionZ: http://63.33.64.193:55679/debug/extensionz Ninja: storage エクステンションでデータの耐久性を向上させる これをこなうには、ディストリビューションに file_storage エクステンションモジュールがインストールされていることを確認する必要があります。確認するには、otelcol-contrib components コマンドを実行します:
​ Truncated Output Full Output # ... truncated for clarity extensions: - file_storage buildinfo: command: otelcol-contrib description: OpenTelemetry Collector Contrib version: 0.80.0 receivers: - prometheus_simple - apache - influxdb - purefa - purefb - receiver_creator - mongodbatlas - vcenter - snmp - expvar - jmx - kafka - skywalking - udplog - carbon - kafkametrics - memcached - prometheus - windowseventlog - zookeeper - otlp - awsecscontainermetrics - iis - mysql - nsxt - aerospike - elasticsearch - httpcheck - k8sobjects - mongodb - hostmetrics - signalfx - statsd - awsxray - cloudfoundry - collectd - couchdb - kubeletstats - jaeger - journald - riak - splunk_hec - active_directory_ds - awscloudwatch - sqlquery - windowsperfcounters - flinkmetrics - googlecloudpubsub - podman_stats - wavefront - k8s_events - postgresql - rabbitmq - sapm - sqlserver - redis - solace - tcplog - awscontainerinsightreceiver - awsfirehose - bigip - filelog - googlecloudspanner - cloudflare - docker_stats - k8s_cluster - pulsar - zipkin - nginx - opencensus - azureeventhub - datadog - fluentforward - otlpjsonfile - syslog processors: - resource - batch - cumulativetodelta - groupbyattrs - groupbytrace - k8sattributes - experimental_metricsgeneration - metricstransform - routing - attributes - datadog - deltatorate - spanmetrics - span - memory_limiter - redaction - resourcedetection - servicegraph - transform - filter - probabilistic_sampler - tail_sampling exporters: - otlp - carbon - datadog - f5cloud - kafka - mezmo - skywalking - awsxray - dynatrace - loki - prometheus - logging - azuredataexplorer - azuremonitor - instana - jaeger - loadbalancing - sentry - splunk_hec - tanzuobservability - zipkin - alibabacloud_logservice - clickhouse - file - googlecloud - prometheusremotewrite - awscloudwatchlogs - googlecloudpubsub - jaeger_thrift - logzio - sapm - sumologic - otlphttp - googlemanagedprometheus - opencensus - awskinesis - coralogix - influxdb - logicmonitor - signalfx - tencentcloud_logservice - awsemf - elasticsearch - pulsar extensions: - zpages - bearertokenauth - oidc - host_observer - sigv4auth - file_storage - memory_ballast - health_check - oauth2client - awsproxy - http_forwarder - jaegerremotesampling - k8s_observer - pprof - asapclient - basicauth - headers_setter このエクステンションは、エクスポーターが設定されたエンドポイントにデータを送信できない事象が発生したときに、データをディスクにキューイングする機能をエクスポーターに提供します。
このエクステンションを設定するには、以下の情報を含むように設定を更新する必要があります。まず、 /tmp/otel-data ディレクトリを作成し、読み取り/書き込み権限を与えてください：
extensions: ... file_storage: directory: /tmp/otel-data timeout: 10s compaction: directory: /tmp/otel-data on_start: true on_rebound: true rebound_needed_threshold_mib: 5 rebound_trigger_threshold_mib: 3 # ... truncated for clarity service: extensions: [health_check, pprof, zpages, file_storage]なぜキューデータをディスクに書くの？ コレクターはネットワークの不調（および、コレクターの再起動）を乗り切って、アップストリームプロバイダーに確実にデータを送信できるようになります。
キューデータをディスクに書く時の注意事項は？ ディスクの性能により、データスループットの性能に影響を与える可能性があります
参照 https://community.splunk.com/t5/Community-Blog/Data-Persistence-in-the-OpenTelemetry-Collector/ba-p/624583 https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage 設定を確認しましょう さて、エクステンションについて説明したので、設定の変更箇所を確認していきましょう。
Check-in設定ファイルを確認してください ​ config.yaml 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 extensions: health_check: endpoint: 0.0.0.0:13133 pprof: endpoint: 0.0.0.0:1777 zpages: endpoint: 0.0.0.0:55679 receivers: otlp: protocols: grpc: http: opencensus: # Collect own metrics prometheus: config: scrape_configs: - job_name: 'otel-collector' scrape_interval: 10s static_configs: - targets: ['0.0.0.0:8888'] jaeger: protocols: grpc: thrift_binary: thrift_compact: thrift_http: zipkin: processors: batch: exporters: logging: verbosity: detailed service: pipelines: traces: receivers: [otlp, opencensus, jaeger, zipkin] processors: [batch] exporters: [logging] metrics: receivers: [otlp, opencensus, prometheus] processors: [batch] exporters: [logging] extensions: [health_check, pprof, zpages] さて、エクステンションについて復習したところで、ワークショップのデータパイプラインの部分に飛び込んでみましょう。パイプラインとは、コレクター内でデータがたどる経路を定義するもので、レシーバーから始まり、追加の処理や変更をし、最終的にエクスポーターを経由してコレクターを出ます。
OpenTelemetry Collector のデータパイプラインは、レシーバー、プロセッサー、エクスポーターで構成されています。まずは、レシーバーから見ていきましょう。
`,description:"",tags:null,title:"OpenTelemetry Collector エクステンション",uri:"/ja/other/opentelemetry-collector/2-extensions/3-zpages/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector レシーバー",content:`その他のレシーバー デフォルトの設定には、他のレシーバーがあることに気づくはずです。 otlp、opencensus、jaeger、zipkin が定義されています。これらは他のソースからテレメトリーデータを受信するために使われます。このワークショップでは、これらのレシーバーについては取り上げませんので、そのままにしておきましょう。
Ninja: レシーバーを動的に生成する dockerコンテナ、kubernetesポッド、sshセッションのような短時間のタスクを観測するために、receiver creator レシーバーと observer エクステンションを使って、対象のサービスが起動するタイミングで新しいレシーバーを作成することができます。
何が必要なの？ receiver creator とそれに関連する observer エクステンションの使用を開始するには、collector build manifest に追加する必要があります。
詳細は installation を参照してください。
注意事項はある？ 短命なタスクの中には、username や password のような追加設定を必要とするものがあります。それらの値は環境変数 を参照したり、 \${file:./path/to/database/password} のようなスキーム展開構文を使うこともできます。
組織における機密情報の取り扱い規定に従って、どのような方法を取るかを検討してください。
Ninja ゾーン この Ninja ゾーンに必要なものは2つだけです:
builder manifestに、 receiver creator レシーバーと observer エクステンションを追加する 検出されたエンドポイントを検出するように、設定を作成する 次のようにすると、設定をテンプレート化できます:
receiver_creator: watch_observers: [host_observer] receivers: redis: rule: type == "port" && port == 6379 config: password: \${env:HOST_REDIS_PASSWORD}他の例は receiver creator’s examples にあります。
設定を確認しましょう これで、レシーバーをカバーできました。ここで、設定のの変更内容をチェックしてみましょう。
Check-in設定をレビューしてください ​ config.yaml 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 extensions: health_check: endpoint: 0.0.0.0:13133 pprof: endpoint: 0.0.0.0:1777 zpages: endpoint: 0.0.0.0:55679 receivers: hostmetrics: collection_interval: 10s scrapers: # CPU utilization metrics cpu: # Disk I/O metrics disk: # File System utilization metrics filesystem: # Memory utilization metrics memory: # Network interface I/O metrics & TCP connection metrics network: # CPU load metrics load: # Paging/Swap space utilization and I/O metrics paging: # Process count metrics processes: # Per process CPU, Memory and Disk I/O metrics. Disabled by default. # process: otlp: protocols: grpc: http: opencensus: # Collect own metrics prometheus/internal: config: scrape_configs: - job_name: 'otel-collector' scrape_interval: 10s static_configs: - targets: ['0.0.0.0:8888'] jaeger: protocols: grpc: thrift_binary: thrift_compact: thrift_http: zipkin: processors: batch: exporters: logging: verbosity: detailed service: pipelines: traces: receivers: [otlp, opencensus, jaeger, zipkin] processors: [batch] exporters: [logging] metrics: receivers: [otlp, opencensus, prometheus/internal] processors: [batch] exporters: [logging] extensions: [health_check, pprof, zpages] これで、レシーバーを通して OpenTelemetry Collector にデータがどのように取り込まれるかを確認しました。次に、コレクターが受信したデータをどのように処理するかを見てみましょう。
警告 ここではコレクターを再起動しないでください！ /etc/otelcol-contrib/config.yaml の変更はまだ完了していません。
`,description:"",tags:null,title:"OpenTelemetry Collector レシーバー",uri:"/ja/other/opentelemetry-collector/3-receivers/3-other-receivers/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM",content:` 20分 ダッシュボードとチャートの紹介 チャートの編集と作成 フィルタリングと分析関数 数式の使用 ダッシュボードでのチャートの保存 SignalFlowの紹介 1. ダッシュボード ダッシュボードとは、チャートをグループ化し、メトリクスを視覚化したものです。適切に設計されたダッシュボードは、システムに関する有益で実用的な洞察を一目で提供します。ダッシュボードは複雑なものもあれば、見たいデータだけを掘り下げたいくつかのチャートだけのものもあります。
このモジュールでは、次のようなチャートとダッシュボードを作成し、それをチームページに接続します。
2. あなたのチームのページ 左のナビゲーションから を開きます。あなたはすでにチームに割り当てられているので、チームダッシュボードが表示されます。
ここでは、チーム Example Team を例に挙げています。実際のワークショップでは、別のチーム名かも知れません。
このページには、チームメンバーの総数、チームのアクティブなアラートの数、チームに割り当てられているすべてのダッシュボードが表示されます。現在、ダッシュボードは割り当てられていませんが、この後で、あなたが作成する新しいダッシュボードをチームページに追加していきます。
3. サンプルチャート 続けて、画面右上の All Dashboards をクリックします。事前に作成されたもの（プレビルドダッシュボード）も含め、利用可能なすべてのダッシュボードが表示されます。
すでにSplunk Agentを介してCloud APIインテグレーションや他のサービスからメトリクスを受信している場合は、これらのサービスに関連するダッシュボードが表示されます。
4. サンプルデータの確認 ダッシュボードの中に、 Sample Data というダッシュボードグループがあります。Sample Data ダッシュボードグループをクリックして展開し、Sample Charts ダッシュボードをクリックします。
Sample Charts ダッシュボードでは、ダッシュボードでチャートに適用できる様々なスタイル、色、フォーマットのサンプルを示すチャートが表示されます。
このダッシュボードグループのすべてのダッシュボード（PART 1、PART 2、PART 3、INTRO TO SPLUNK OBSERVABILITY CLOUD）に目を通してみてください。
`,description:"",tags:null,title:"ダッシュボードを利用する",uri:"/ja/imt/dashboards/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > Pet Clinic Java ワークショップ",content:`1. 依存ライブラリを追加する 前のセクション足したような、プロセス全体に渡る属性は便利なのですが、ときにはさらに、リクエストの内容に応じた状況を知りたくなるかもしれません。 心配ありません、OpenTelemetryのAPIを通じてそれらを計装し、データを送り、Splunk Observabilityで分析できるようになります。
最初に、JavaアプリケーションがOpenTelemetryのAPIを使えるように、ライブラリの依存を追加していきます。 もちろん、vimなどのお好みのエディタをお使い頂いても大丈夫です！
アプリケーションが起動中であれば、一旦停止しましょう。ターミナルで Ctrl-c を押すと、停止することができます。
nano pom.xmlそして、<dependencies> セクションの中（33行目）に↓を追加してください。 ファイル修正後、 ctrl-O のあとに Enter で、ファイルを保存します。次に ctrl-X で、nanoを終了します。
<dependency> <groupId>io.opentelemetry</groupId> <artifactId>opentelemetry-api</artifactId> </dependency>念のため、コンパイルできるか確かめてみましょう:
./mvnw package -Dmaven.test.skip=true Tips: nanoの使い方と壊れたファイルの直し方 nanoはLinux環境でよく使われる、シンプルなエディタの一つです。
Alt-U で、アンドゥができます。Macの場合は Esc キーを押したあとに U を押してください！ ctrl-_ のあとに数字を入力すると、指定した行数にジャンプします。 ctrl-O のあとに Enter で、ファイルを保存します。 ctrl-X で、nanoを終了します。 もしファイルをどうしようもなく壊してしまって元に戻したい場合は、gitを使って次のようにするとよいでしょう。
git checkout pom.xml これで、JavaのアプリケーションでOpenTelemetryのAPIが使う準備ができました。
2. Javaのコードにマニュアル計装を追加する では、アプリケーションコードをちょっと変更して、リクエストのコンテキストのデータをスパン属性に追加してみましょう。
ここでは Pet Clinic アプリケーションの中で Find Owners が使われたときに、どのような検索文字列が指定されたのかを調査できるようにしていきます。 検索条件によってパフォーマンスが劣化してしまうケース、よくありませんか？そんなときは OwnerController に計装を追加していきましょう！
nano src/main/java/org/springframework/samples/petclinic/owner/OwnerController.javaこのコードを 変更するのは2箇所 です。
まず、import jakarta.validation.Valid; の下、37行目付近に↓を足します:
import io.opentelemetry.api.trace.Span;次に、 // find owners by last name のコメントがある箇所（おそらく95行目付近にあります）の下に、次のコードを足していきましょう:
Span span = Span.current(); span.setAttribute("lastName", owner.getLastName());このコードで、Last Nameとして指定された検索条件が、スパン属性 lastName としてSplunk Observabilityに伝えるようになりました。
アプリケーションをコンパイルし直ししますが、Javaコードを多少汚してしまったかもしれません。 spring-javaformat:apply を指定しながらコンパイルしてみましょう。
./mvnw spring-javaformat:apply package -Dmaven.test.skip=trueアプリケーションを起動します。せっかくなので、バージョンを一つあげて version=0.315 としましょう。
java -javaagent:./splunk-otel-javaagent.jar \\ -Dserver.port=8083 \\ -Dotel.service.name=$(hostname).service \\ -Dotel.resource.attributes=deployment.environment=$(hostname),version=0.315 \\ -Dsplunk.profiler.enabled=true \\ -Dsplunk.profiler.memory.enabled=true \\ -Dsplunk.metrics.enabled=true \\ -jar target/spring-petclinic-*.jar --spring.profiles.active=mysqlhttp://<VM_IP_ADDRESS>:8083 にアクセスして、オーナー検索をいくつか試してましょう。そしてSplunk APM UIからExploreを開き、アプリケーションのトレースを見ていきます。
さらなる情報: マニュアル計装について マニュアル計装で何ができるか、他の言語でのやり方などは、OpenTelemetryの公式ウェブサイトにある Instrumentation ページをご覧ください。
検証が完了したら、ターミナルで Ctrl-c を押すと、アプリケーションを停止することができます。
次のセクションでは、RUMを使ってブラウザ上のパフォーマンスデータを収集してみましょう。
`,description:"",tags:null,title:"マニュアル計装",uri:"/ja/other/pet-clinic/docs/manual_instrumentation/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する",content:`レシーバーワークショップへようこそ！OpenTelemetry Collectorのデータパイプラインのスタート地点です。さあ、始めましょう。
レシーバーはデータをCollectorに取り込む方法で、プッシュベースとプルベースのものがあります。レシーバーは1つ以上のデータソースをサポートします。一般的に、レシーバーは指定されたフォーマットでデータを受け入れ、内部フォーマットに変換し、該当するパイプラインで定義されたプロセッサやエクスポータにデータを渡します。
プッシュまたはプルベースのレシーバは、データをCollectorに取り込む方法です。レシーバは 1 つまたは複数のデータソースをサポートします。通常、レシーバは指定されたフォーマットでデータを受け入れ、内部フォーマットに変換し、該当するパイプラインで定義されたプロセッサーや エクスポーターにデータを渡します。
%%{ init:{ "theme":"base", "themeVariables": { "primaryColor": "#ffffff", "clusterBkg": "#eff2fb", "defaultLinkColor": "#333333" } } }%% flowchart LR; style M fill:#e20082,stroke:#333,stroke-width:4px,color:#fff subgraph Collector A[OTLP] --> M(Receivers) B[JAEGER] --> M(Receivers) C[Prometheus] --> M(Receivers) end subgraph Processors M(Receivers) --> H(Filters, Attributes, etc) E(Extensions) end subgraph Exporters H(Filters, Attributes, etc) --> S(OTLP) H(Filters, Attributes, etc) --> T(JAEGER) H(Filters, Attributes, etc) --> U(Prometheus) end `,description:"",tags:null,title:"OpenTelemetry Collector レシーバー",uri:"/ja/other/opentelemetry-collector/3-receivers/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk RUM",content:` ブラウザでOnline BoutiqueのウェブページのオリジナルのHEADセクション（またはここにある例を使用）をチェックします ワークショップ Online Boutique の Webアドレスを検索します Online Boutiqueに加えられた変更を確認します 1. RUMなしのOnline Boutiqueのオリジナルコードを確認する APMセッションの一部でEC2インスタンスにOnline Boutiqueをインストールしていれば、ポート番号81でサイトにアクセスできます。
Online BoutiqueがインストールされたEC2インスタンスにアクセスできない場合は、講師からRUMがインストールされていないOnline BoutiqueのURLを教えてもらい、次のステップに進んでください。
2. RUM Access Tokenの入手 これから行うデプロイメントは、RUM ワークショップセクションの一部としても使用されます。Splunk UIからRUM Access Tokenを取得する必要があります。ワークショップのアクセストークンは、左下の » をクリックし メニューをクリックして、 Settings → Access Tokens を選択すると見つけることができます。
講師が使用するように指示したRUMワークショップトークン（例： O11y-Workshop-RUM-TOKEN ）を展開し、 Show Token をクリックしてトークンを公開します。 Copy ボタンをクリックし、クリップボードにコピーしてください。 Default のトークンは使用しないでください。トークンのAuthorization ScopeがRUMであることを確認してください。
新規にトークンを作らないでください このワークショップのために、皆さんが行う演習に適した設定をしたRUM Tokenを作成しています。
EC2にSSHアクセスしているシェルスクリプトで環境変数 RUM_TOKEN を作成し、デプロイメントをパーソナライズします。
​ Export Variables export RUM_TOKEN=<replace_with_O11y-Workshop-RUM-TOKEN> 2. Online Boutiqueのデプロイ Online BoutiqueアプリケーションをK3sにデプロイするには、apm configスクリプトを実行し、デプロイを適用してください。
​ Deploy Online Boutique Deployment Output cd ~/workshop/apm kubectl apply -f deployment.yaml deployment.apps/checkoutservice created service/checkoutservice created deployment.apps/redis-cart created service/redis-cart created deployment.apps/productcatalogservice created service/productcatalogservice created deployment.apps/loadgenerator created service/loadgenerator created deployment.apps/frontend created service/frontend created service/frontend-external created deployment.apps/paymentservice created service/paymentservice created deployment.apps/emailservice created service/emailservice created deployment.apps/adservice created service/adservice created deployment.apps/cartservice created service/cartservice created deployment.apps/recommendationservice created service/recommendationservice created deployment.apps/shippingservice created service/shippingservice created deployment.apps/currencyservice created service/currencyservice created 変数未セットに関するメッセージが表示された場合 kubectl delete -f deployment.yaml コマンドを実行しAPM環境のデプロイ削除します。 次にガイド、メッセージに表示されていた変数をexportし上記のデプロイスクリプトを再実行します。
ウェブブラウザーを起動し、Online Boutiqueにアクセスします。 (以前使用したもの、または新しくワークショップ講師が提供したもの）。RUMなしのOnline Boutiqueが起動していることが確認できます。
下記のお使いのブラウザの説明に従ってください。
1.1 Chrome, FireFox & Microsoft Edge ユーザー - ページのソースを確認 Chrome、Firefox、Microsoft Edgeでは、Online Boutiqueのサイト上で右クリックすると、 「ページのソースを表示」 のオプションが表示されます。
これを選択すると、HTMLページのソースコードが別のタブで表示されます。
成功すれば、 2 - 変更前のHEADセクションの確認 へ進みます。
1.2 Safari ユーザー - ページのソースを確認 Safariでは機能を有効化する必要がある場合があります。OS Xメニューバーの Safari の配下にある 「設定」 をクリックします。
ダイアログがポップアップしますので、 「詳細」 ペイン内の 「メニューバーに"開発"メニューを表示」 にチェックをいれ、ダイアログボックスを閉じます。
Online Boutiqueを右クリックすると、「ページのソースを表示する」オプションが表示されるようになります。
Online Boutiqueでそのオプションを選択すると、以下のようなHTMLソースコードが表示されます。
成功すれば、 2 - 変更前のHEADセクションの確認 へ進みます。
1.3 Internet Explorer ユーザー - ページのソースを確認 Internet Explorer 11 をお使いの場合、この演習では Web/RUM 用のSplunk Open Telemetry JavaScriptの特定のバージョンが必要になるため、問題が発生する可能性があります。 ただし、Online Boutiqueサイトを右クリックすると、「ソースを表示」 のオプションが表示され、必要な変更を確認することができます。
Online Boutiqueでそのオプションを選択すると、以下のようなHTMLソースコードが表示されます。
2 - 変更前のHEADセクションの確認 RUMのための変更は、WebページのHEADセクションで実施します。以下は、あなたのローカルのBaseバージョンにあるべきオリジナルの行です。
Splunk または Open Telemetry Beacon (RUM Metrics と Traces を送信するために使用される関数) への参照はありません。
3. RUM有効Online Boutiqueのウェブ（URL）を探す RUMで使用するOnline Boutiqueは、RUM有効インスタンスのIPアドレスの81番ポートで見ることができます。URLはワークショップの講師から提供されます。
このRUMのセッションでは、講師が用意したRUM有効Online Boutiqueにアクセスできます。新しいウェブブラウザを開き、 http://{==RUM-HOST-EC2-IP==}:81/ にアクセスすると、RUM有効Online Boutiqueが動作しているのが見えます。ここでも、前のセクションで説明したように、HTMLページのソースを表示します。
4. RUMを有効にするために行った変更をHEADセクションで確認 RUMに必要な変更は、WebページのHEADセクションに配置されます。以下は、RUMを有効にするために必要な変更を加えたhostsの更新されたHEADセクションです。
最初の3行（赤色でマーク）は、RUMトレースを有効にするためにWebページのHEADセクションに追加されています。最後の3行（青色でマーク）はオプションで、カスタムRUMイベントを有効にするために使用します。
<script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" type="text/javascript"></script> <script>window.SplunkRum && window.SplunkRum.init({beaconUrl: "https://rum-ingest.eu0.signalfx.com/v1/rum", rumAuth: "1wCqZVUWIP5XSdNjPoQRFg", app: "ksnq-store", environment: "ksnq-workshop"});</script> <script> const Provider = SplunkRum.provider; var tracer=Provider.getTracer('appModuleLoader'); </script> 最初の行は、Splunk Open Telemetry Javascript ファイルをダウンロードする場所を指定しています。https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js (必要であれば、ローカルに読み込むこともできます) 2行目は、Beacon URLでトレースの送信先を定義しています。 {beaconUrl: "https://rum-ingest.eu0.signalfx.com/v1/rum" また、Access Tokenを追加しています。 rumAuth: "1wCqZVUWIP5XSdNjPoQRFg" (もちろんこれは例です。全てのアプリケーションに対して、複数のRUM Access Tokenを作成することができます。) * また、SPLUNK RUM UIで使用するために、アプリケーション名や環境などの識別タグをRUMトレースに追加するために使用されます。 app: "ksnq-store", environment: "ksnq-workshop"} Info この例ではアプリ名は ksnq-store ですが、これはワークショップでは異なるでしょう。RUMセッションで使用するアプリ名と環境は講師に確認し、メモしておいてください。
上記の2行だけであなたのWebサイトでRUMを有効にすることができます。
(青色の)オプションのセクションでは、 var tracer=Provider.getTracer('appModuleLoader'); を使用して、すべてのページ変更に対してカスタムイベントを追加し、ウェブサイトのコンバージョンと使用状況をよりよく追跡できるようにします。
`,description:"",tags:null,title:"3. 自分のWebサイトでRUMを有効化する場合の例",uri:"/ja/rum/3-setup/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM > ダッシュボードを利用する",content:`1 新しいチャートの作成 それでは、新しいチャートを作成し、ダッシュボードに保存してみましょう。
UIの右上にある + アイコンを選択し、ドロップダウンから Chart を選択します。 または、 New Chart ボタンをクリックすると、新しいチャートが作成されます。
これで、以下のようなチャートのテンプレートが表示されます。
プロットするメトリックを入力してみましょう。ここでは、demo.trans.latency というメトリックを使用します。
Plot Editor タブの Signal に demo.trans.latency を入力します。
すると、折れ線グラフが表示されるはずです。時間を15分に切り替えてみてください。
2. フィルタリングと分析 次に、Paris データセンターを選択して分析を行ってみましょう。そのためにはフィルタを使用します。
Plot Editor タブに戻り、 Add Filter をクリックして、入力補助として選択肢が出てくるので、そこから demo_datacenter を選択し、Paris を選択します。
F(x) 欄に分析関数 Percentile:Aggregation を追加し、値を 95 にします（枠外をクリックすると設定が反映されます）。
Percentile 関数やその他の関数の情報は、Chart Analytics を参照してください。
3. タイムシフト分析を追加 それでは、以前のメトリックと比較してみましょう。... をクリックして、ドロップダウンから Clone をクリックし、Signal A をクローンします。
A と同じような新しい行が B という名前で表示され、プロットされているのがわかります。
シグナル B に対して、F(x) 列に分析関数 Timeshift を追加し、1w（もしくは 7d でも同じ意味です）と入力し、外側をクリックして反映させます。
右端の歯車をクリックして、Plot Color を選択（例：ピンク）すると、 B のプロットの色を変更できます。
Close をクリックして、設定を終えます。
シグナル A （過去15分）のプロットが青、1週間前のプロットがピンクで表示されています。
より見やすくするために、Area chart アイコンをクリックして表示方法を変更してみましょう。
これで、前週にレイテンシーが高かった時期を確認することができます。
次に、Override バーの Time の隣にあるフィールドをクリックし、ドロップダウンから Past Hour を 選択してみましょう。
4. 計算式を使う ここでは、1日と7日の間のすべてのメトリック値の差をプロットしてみましょう。
Enter Formula をクリックして、A-B （AからBを引いた値）を入力し、C を除くすべてのシグナルを隠します（目アイコンの選択を解除します）。
これで、 A と B のすべてのメトリック値の差だけがプロットされているのがわかります。B のメトリック値が、その時点での A のメトリック値よりも何倍か大きな値を持っているためです。
次のモジュールで、チャートとディテクターを動かすための SignalFlow を見てみましょう。
`,description:"",tags:null,title:"3.3 フィルタと数式の使い方",uri:"/ja/imt/dashboards/filtering/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector プロセッサー",content:`Attributes プロセッサー attribute プロセッサーを使うと、スパン、ログ、またはメトリクスの属性を変更できます。また、このプロセッサーは、入力データをフィルタリングし、マッチさせ、指定されたアクションに含めるべきか、除外すべきかを決定する機能もサポートしています。
アクションを設定するには、指定された順序で実行されるアクションのリストを記述します。サポートされるアクションは以下の通りです：
insert: その属性がない場合に、新しい属性値を挿入します。 update: その属性がある場合に、その属性値を更新します。 upsert: insert または update を実行します。属性がない場合には新しい属性値を挿入し、属性がある場合にはその値を更新します。 delete: 入力データから属性値を削除します。 hash: 属性値をハッシュ化 (SHA1) します。 extract: 入力キーの値を正規表現ルールを使って抽出し、対象キーの値を更新します。対象キーがすでに存在する場合は、その値は上書きされます。 次の例のように、attribute プロセッサーを使って、キーは participant.name、あたいはあなたの名前（例: marge_simpson）という新しい属性を追加してみましょう。
警告 INSERT_YOUR_NAME_HERE の箇所は、自分の名前に置き換えてください。また、自分の名前に スペースを使わない ようにしてください。
このワークショップの後半では、この属性を使用して Splunk Observability Cloud でメトリクスをフィルタリングします。
​ Attributes Processor Configuration processors: batch: resourcedetection/system: detectors: [system] system: hostname_sources: [os] resourcedetection/ec2: detectors: [ec2] attributes/conf: actions: - key: participant.name action: insert value: "INSERT_YOUR_NAME_HERE" Ninja: コネクターを使って内部への洞察を加速する 最近追加されたものの一つとして、connector というコンセプトがあります。これを使うと、あるパイプラインの出力を別のパイプラインの入力に結合できるようになります。
利用シーンとして、送信するデータポイントの量、エラーステータスを含むログの数をメトリクスをとして出力するサービスがあります。他には、あるデプロイ環境から送信されるデータ量のメトリクスを生成するサービスがあります。このような場合に、count コネクターですぐに対応できます。
プロセッサーではなくコネクターなのはなぜ？ プロセッサーは、処理したデータを次に渡すものであり、追加の情報を出力することはできません。コネクターはレシーバーで受け取ったデータを出力せずに、私たちが求める洞察を作り出す機会を提供します。
たとえば、count コネクターを使うと、環境変数 deployment を持たないログ、メトリクス、トレースの数をカウントすることができます。
また、非常にシンプルな例として、deployment 別にデータ使用量を分解して出力することもできます。
コネクターの注意事項 コネクターは、あるパイプラインからエクスポートされ、別のパイプラインでレシーバーで定義されたデータのみを受け入れます。コレクターをどう構築してどう利用するか、設定を検討する必要があります。
参照 https://opentelemetry.io/docs/collector/configuration/#connectors https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/countconnector 設定を確認しましょう これで、プロセッサーがカバーできました。ここで、設定のの変更内容をチェックしてみましょう。
Check-in設定をレビューしてください ​ config.yaml 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 extensions: health_check: endpoint: 0.0.0.0:13133 pprof: endpoint: 0.0.0.0:1777 zpages: endpoint: 0.0.0.0:55679 receivers: hostmetrics: collection_interval: 10s scrapers: # CPU utilization metrics cpu: # Disk I/O metrics disk: # File System utilization metrics filesystem: # Memory utilization metrics memory: # Network interface I/O metrics & TCP connection metrics network: # CPU load metrics load: # Paging/Swap space utilization and I/O metrics paging: # Process count metrics processes: # Per process CPU, Memory and Disk I/O metrics. Disabled by default. # process: otlp: protocols: grpc: http: opencensus: # Collect own metrics prometheus/internal: config: scrape_configs: - job_name: 'otel-collector' scrape_interval: 10s static_configs: - targets: ['0.0.0.0:8888'] jaeger: protocols: grpc: thrift_binary: thrift_compact: thrift_http: zipkin: processors: batch: resourcedetection/system: detectors: [system] system: hostname_sources: [os] resourcedetection/ec2: detectors: [ec2] attributes/conf: actions: - key: participant.name action: insert value: "INSERT_YOUR_NAME_HERE" exporters: logging: verbosity: detailed service: pipelines: traces: receivers: [otlp, opencensus, jaeger, zipkin] processors: [batch] exporters: [logging] metrics: receivers: [otlp, opencensus, prometheus] processors: [batch] exporters: [logging] extensions: [health_check, pprof, zpages] `,description:"",tags:null,title:"OpenTelemetry Collector プロセッサー",uri:"/ja/other/opentelemetry-collector/4-processors/3-attributes/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector サービス",content:`Resource Detection プロセッサー また、コレクターがインスタンスのホスト名やAWS/EC2のメタデータを取得できるように、resourcedetection/system および resourcedetection/ec2 プロセッサーを追加しました。これらのプロセッサーをメトリクスパイプライン下で有効にする必要があります。
metrics パイプラインの下の processors セクションを更新して、resourcedetection/system および resourcedetection/ec2 を追加します：
service: pipelines: traces: receivers: [otlp, opencensus, jaeger, zipkin] processors: [batch] exporters: [logging] metrics: receivers: [hostmetrics, otlp, opencensus, prometheus/internal] processors: [batch, resourcedetection/system, resourcedetection/ec2] exporters: [logging]`,description:"",tags:null,title:"OpenTelemetry Collector サービス",uri:"/ja/other/opentelemetry-collector/6-service/3-resourcedetection/index.html"},{breadcrumb:"Splunk Observability Workshops > その他のリソース",content:`はじめに 大規模な組織で OpenTelemetry を展開する際には、タグ付けのための標準化された命名規則を定義し、その規則が遵守されるようにガバナンスプロセスを設定することが非常に重要です。
これにより、OpenTelemetry を通じて収集される MELT データ（メトリクス、イベント、ログ、トレース）を、アラート、ダッシュボード作成、トラブルシューティングの目的で効率的に活用することが可能になります。また、Splunk Observability Cloud のユーザーが探しているデータを迅速に見つけることができます。
命名規則はまた、データを効果的に集約するためにも重要です。例えば、環境ごとのユニークなホストの数を数えたい場合、ホスト名と環境名を捉えるための標準化された規則を使用する必要があります。
属性 vs タグ 先に進む前に、用語についての注意をしておきましょう。OpenTelemetry の「タグ」は「属性（attribute）」と呼ばれます。属性は、手動または自動の計装を通じて、メトリクス、ログ、トレースに添付することができます。
属性はまた、Resource Detection processorなどのさまざまなプロセッサを使用して、OpenTelemetry コレクターレベルでメトリクス、ログ、トレースに添付することもできます。
Splunk Observability Cloud に属性付きのトレースが取り込まれると、それらは「タグ」として利用可能になります。オプションとして、トレースの一部として収集された属性は、Troubleshooting Metric Setsの作成に使用され、Tag Spotlightなどのさまざまな機能と共に使用することができます。
また、属性はMonitoring Metric Setsの作成に使用され、アラートのトリガーとして使用することもできます。
リソースに関するセマンティック規約 OpenTelemetry リソースセマンティック規約は、組織が標準化すべき属性を決定する際の出発点として使用できます。以下のセクションでは、よく使用される属性のいくつか見ていきましょう。
サービス属性 監視されるサービスを記述するために多くの属性が使用されます。
service.name はサービスの論理名を定義する必須の属性です。OpenTelemetry SDK によって自動的に追加されますが、カスタマイズすることができます。これはシンプルに保つことが最善です（例えば、inventoryservice は inventoryservice-prod-hostxyz よりも良いでしょう。他の属性を使用してサービスの他の側面を捉えることができます）。
以下のサービス属性が推奨されます：
service.namespace はサービスを所有するチームを識別するために使用されます service.instance.id はサービスのユニークなインスタンスを識別するために使用されます service.version はサービスのバージョンを識別するために使用されます テレメトリSDK これらの属性はSDKによって自動的に設定され、使用されている計測ライブラリに関する情報を記録します：
telemetry.sdk.name は通常 opentelemetry に設定されます。 telemetry.sdk.language は SDK の言語で、例えば java です。 telemetry.sdk.version は使用されている SDK のバージョンを識別します。 コンテナ コンテナで実行されるサービスには、container.id、container.name、container.image.name など、コンテナのランタイムを記述するための多くの属性が使用されます。完全なリストはこちらで確認できます。
ホスト これらの属性は、サービスが実行されているホストを記述し、host.id、host.name、host.arch などの属性を含みます。完全なリストはこちらで確認できます。
デプロイ環境 deployment.environment 属性は、サービスがデプロイされている環境（ staging や production など）を識別するために使用されます。
Splunk Observability Cloud は、この属性を使用して関連コンテンツを有効する（詳細はこちら）ため、この属性を含めることが重要です。
クラウド AWS などのパブリッククラウド環境で実行されるサービスに関する情報を捉えるための属性もあります。これには、cloud.provider、cloud.account.id、cloud.region が含まれます。
属性の完全なリストはこちらで確認できます。
一部のクラウドプロバイダー、例えば GCP は、独自のセマンティック規則を定義しています。
Kubernetes Kubernetesで実行されるアプリケーションにも、いくつかの標準化された属性があります。これらの多くは、Splunk の OpenTelemetry コレクター配布によって自動的に追加されます（詳細はこちら）。
属性は、例えば k8s.cluster.name、k8s.node.name、k8s.pod.name、k8s.namespace.name、kubernetes.workload.name などがあります。
カスタム属性のベストプラクティス 多くの組織では、OpenTelemetryのリソースセマンティック規約で定義されているもの以上の属性が欲しくなります。
この場合、セマンティック規約にすでに含まれている属性名との命名競合を避けることが重要です。つまり、特定の属性名を命名規則に決定する前に、セマンティック規約をチェックすると良いでしょう。
属性名の命名規則に加えて、属性値も考慮する必要があります。例えば、アプリケーションが属する特定のビジネスユニットをキャプチャしたい場合、簡単にかつ効果的にフィルタリングするために、標準化されたビジネスユニット値のリストも持ちたいでしょう。
OpenTelemetryコミュニティでは、属性の命名に従うべきガイドラインも提供しています。こちらで見つけることができます。
Recommendations for Application Developersは、私たちの議論に最も関連しています。
そこでは、以下を推奨しています：
com.acme.shopname のように、会社のドメイン名で属性名を接頭辞として付けること（属性が社内だけでなく外部で使用される可能性がある場合） 属性が特定のアプリケーションに固有であり、組織内でのみ使用される場合は、アプリケーション名で属性名に接頭辞を付けること 既存の OpenTelemetry セマンティック規約の名前を属性名の接頭辞として使用しないこと 異なる組織や業界全体で一般的なニーズがある場合は、あなたの属性名を OpenTelemetry 仕様に追加する提案を検討すること otel.* で始まる属性名は避けること。これは OpenTelemetry 仕様の使用に予約されています カーディナリティに関する考慮事項 属性名と値の命名基準を決定する際に考慮すべき最後の点は、メトリクスのカーディナリティに関連しています。
のカーディナリティは、メトリクス名とそれに関連する次元の組み合わせによって生成されるユニークなメトリクス時系列（MTS: Metric Time Series）の数として定義されます。
メトリクスは、ディメンションの数とそれらのディメンションが持つユニークな値の数が多い場合に、高いカーディナリティを持つことになります。
例えば、あなたのアプリケーションが custom.metric という名前のメトリクスのデータを送信するとします。属性がない場合、custom.metric は単一のメトリクス時系列（MTS）を生成します。
一方で、custom.metricが customer.id という属性を含み、数千の顧客ID値がある場合、これは数千のメトリクス時系列を生成し、コストやクエリ性能に影響を与える可能性があります。
Splunk Observability Cloud は、メトリクスの使用量を管理するためのレポートを提供しています。そして、望ましくないディメンションを削除するルールを作成することができます。しかし、最初の防衛線は、属性名と値の組み合わせがどのようにメトリクスのカーディナリティを増加させるかを理解することです。
まとめ このドキュメントでは、大規模な OpenTelemetry インストゥルメンテーションの展開を開始する前に、OpenTelemetry タグの命名規則を定義することの重要性を強調しました。
OpenTelemetry のリソースセマンティック規約がいくつかの属性の命名規則を定義し、多くの属性が OpenTelemetry SDKや OpenTelemetry コレクター内で動作するプロセッサーを通じて自動的に収集される方法について説明しました。
最後に、リソースセマンティック規約が組織のニーズに十分でない場合に、属性名を作成するためのベストプラクティスを共有しました。
`,description:"大規模な組織で OpenTelemetry を展開する際には、タグ付けのための標準化された命名規則を定義し、規則が遵守されるようにガバナンスプロセスを確立することが重要です。",tags:null,title:"OpenTelemetryとSplunkにおける、タグ付けのための命名規則",uri:"/ja/resources/otel_tagging/index.html"},{breadcrumb:"Splunk Observability Workshops",content:`Splunk RUM は、業界唯一のエンド・ツー・エンドで完全忠実なリアルユーザーモニタリングソリューションです。パフォーマンスを最適化し、トラブルシューティングを迅速に行い、エンドユーザーエクスペリエンスを完全に可視化するために構築されています。
Splunk RUM は、ユーザーエクスペリエンスに影響を与える Web およびモバイルアプリケーションのパフォーマンス問題を特定することができます。Core Web Vitalによるページパフォーマンスのベンチマークと計測をサポートします。W3C タイミング、長時間実行されるタスクの特定、ページロードに影響を与える可能性のあるあらゆるものが含まれますが、これらに限定されるものではありません。
Splunk のエンドツーエンドモニタリング機能を使用すると、アプリケーションを構成する、サービス自身を始めとしてデータベースコール数などのインフラメトリクスやその他関与するすべてに対して、サービス間の遅延を表示することができます。
私たちの完全忠実なエンドツーエンドモニタリングソリューションは、お客様のSpanデータを100％取得します。サンプリングは行わず、フレームワークにとらわれず、Open Telemetryに標準化されています。
フロントエンドとバックエンドのアプリケーションのパフォーマンスは相互に依存していることがよくあります。バックエンドサービスとユーザーエクスペリエンスとの関連性を十分に理解し、可視化できることがますます重要になっています。 全体像を把握するために、Splunk RUM は当社のフロントエンドとバックエンドのマイクロサービス間のシームレスな相関関係を提供します。マイクロサービスやインフラストラクチャに関連する問題によって、ユーザーが Web ベースのアプリケーションで最適とは言えない状態を経験している場合、Splunk はこの問題を検出して警告することができます。
また、Splunk は、より深いトラブルシューティングと根本原因の分析を可能にするために、インコンテキストログとイベントを表示することができます。
`,description:"エンド・ツー・エンドの可視化により、Webブラウザやネイティブモバイルアプリからバックエンドサービスに至るまで、顧客に影響を与える問題をピンポイントで特定することができます。",tags:null,title:"Splunk RUM",uri:"/ja/rum/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk APM > 2. トレースとスパン",content:`サンプルトレース 右上にある「Services by Error Rate」グラフのピンク色の線上をクリックします。選択すると、サンプルトレースのリストが表示されます。Initiating Operation ofが frontend: POST /cart/checkout であるサンプルトレースの1つをクリックしてください。
スパンとともに、選択したトレースの全体が表示されます。エラーが発生したスパンは、その横に赤い！マークが表示されます。グレーのボックスにx6などの数字が表示されている場合は、それをクリックするとpaymentservice スパンを展開することができます。
赤い！マークが表示されたpaymentservice スパンの一つをクリックすると展開され、関連するメタデータやエラーの詳細が表示されます。このエラーが401エラーによるものであることがわかります。また、「テナント」や「バージョン」などの有用な情報も表示されています。
エラーの原因が 無効なリクエスト であることがわかりましたが、正確なリクエストが何であるかはわかりません。ページの下部に、ログへのコンテキストリンクが表示されます。このリンクをクリックすると、このスパンに関連付けられているログが表示されます。
下の画像と同様の Log Observer ダッシュボードが表示されます。
フィルタを使用して、エラーログのみを表示できます。右上にあるERRORをクリックしてから、Add to filterをクリックします。
severityがERRORであるログエントリに絞り込まれます。
いずれかのエントリを選択して詳細を表示します。これで、開発者が誤って本番環境にプッシュした 無効なAPIトークン の使用によってエラーがどのように発生したかを確認できます。
おめでとうございます。これで、このAPMワークショップは完了です。
`,description:"",tags:null,title:"2.3 サンプルトレース",uri:"/ja/apm/using-splunk-apm/example_trace/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM > ダッシュボードを利用する",content:`1. はじめに ここでは、Observability Cloud の分析言語であり、Monitoring as Codeを実現するために利用する SignalFlow について見てみましょう。
Splunk Infrastructure Monitoring の中心となるのは、Python ライクな、計算を実行する SignalFlow 分析エンジンです。SignalFlow のプログラムは、ストリーミング入力を受け取り、リアルタイムで出力します。SignalFlow には、時系列メトリック（MTS）を入力として受け取り、計算を実行し、結果の MTS を出力する分析関数が組み込まれています。
過去の基準との比較する（例：前週との比較） 分布したパーセンタイルチャートを使った母集団の概要を表示する 変化率（またはサービスレベル目標など、比率で表されるその他の指標）が重要な閾値を超えたかどうか検出する 相関関係にあるディメンジョンの発見する（例：どのサービスの挙動がディスク容量不足の警告と最も相関関係にあるかの判断する） Infrastructure Monitoring は、Chart Builder ユーザーインターフェイスでこれらの計算を行い、使用する入力 MTS とそれらに適用する分析関数を指定できます。また、SignalFlow API を使って、SignalFlow のプログラムを直接実行することもできます。
SignalFlow には、時系列メトリックを入力とし、そのデータポイントに対して計算を行い、計算結果である時系列メトリックを出力する、分析関数の大規模なライブラリが組み込まれています。
Info SignalFlow の詳細については、 Analyze incoming data using SignalFlow を参照してください。
2. SignalFlow の表示 チャートビルダーで View SignalFlow をクリックします。
作業していたチャートを構成する SignalFlow のコードが表示されます。UI内で直接 SignalFlow を編集できます。ドキュメントには、SignalFlow の関数やメソッドの 全てのリスト が掲載されています。
また、SignalFlow をコピーして、API や Terraform とやり取りする際に使用して、Monitoring as Code を実現することもできます。
​ SignalFlow A = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).publish(label='A', enable=False) B = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).timeshift('1w').publish(label='B', enable=False) C = (A-B).publish(label='C') View Builder をクリックすると、Chart Builder の UI に戻ります。
この新しいチャートをダッシュボードに保存してみましょう！
`,description:"",tags:null,title:"3.4 SignalFlow",uri:"/ja/imt/dashboards/signalflow/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM",content:` 10 分 チャートからディテクターを作成する アラート条件を設定する プリフライトチェックを実行する ミューティングルールを設定する 1. はじめに Splunk Observability Cloud では、ディテクター（検出器）、イベント、アラート、通知を使用して、特定の条件が満たされたときに情報を提供することができます。たとえば、CPU使用率が95%に達したときや、同時ユーザー数が制限値に近づいてAWSインスタンスを追加で立ち上げなければならない可能性があるときに、Slack チャンネルや Ops チームのメールアドレスにメッセージを送信したいと考えるでしょう。
これらの条件は1つまたは複数のルールとして表現され、ルール内の条件が満たされたときにアラートが発生します。ディテクターに含まれる個々のルールは、重要度に応じてラベル付けされています。Info、Warning、Minor、Major、Criticalとなっています。
2. ディテクターの作成 Dashboards で、前のモジュールで作成した Custom Dashboard Group をクリックし、ダッシュボードの名前をクリックします。
このチャートから、新しいディテクターを作成していきます。Latency vs Load チャート上のベルのアイコンをクリックし、 New Detector From Chart をクリックします。
Detector Name の横にあるテキストフィールドで、提案されたディテクター名の最初に、あなたのイニシャル を追加してください。
ディテクターの名前を決める 提案されたディテクター名の前に自分のイニシャルを追加することをお忘れなく。
次のような名前にしてください: XY’s Latency Chart Detector
Click on Create Alert Rule Detector ウィンドウの Alert signal の中で、アラートするシグナルは Alert on 欄に青のベルが表示されています。このベルは、どのシグナルがアラートの生成に使用されているかを示しています。
Click on Proceed to Alert Condition 3. アラート条件の設定 Alert condition で、Static Threshold をクリックし、 Proceed to Alert Settings をクリックしてください。
Alert Settings で、 Threshold フィールドに値 290 を入力します。同じウィンドウで、右上の Time を過去1日（-1d）に変更します。
4. プリフライトチェックの警告 5秒後にプリフライトチェックが行われます。Estimated alert count に、アラート回数の目安が表示されます。現在のアラート設定では、1日に受信するアラート量は 3 となります。
プリフライトチェックについて アラート条件を設定すると、UIは現在の設定に基づいて、右上に設定された時間枠（ここでは過去1日）の中で、どのくらいのアラートが発生するかを予測します。
すぐに、プラットフォームは現在の設定でシグナルの分析を開始し、「プリフライトチェック」と呼ばれる作業を行います。これにより、プラットフォーム内の過去のデータを使用してアラート条件をテストし、設定が妥当であり、誤って大量のアラートを発生させないようにすることができます。Splunk Observability Cloud を使用してのみ利用できるシンプルかつ非常に強力な方法で、アラートの設定から推測作業を取り除くことができます。
ディテクターのプレビューについての詳細は、こちらのリンクをご覧ください。 Preview detector alerts
Proceed to Alert Message をクリックし、次に進みます。
5. アラートメッセージ Alert message の Severity で Major を選択します。
Proceed to Alert Recipients をクリックします。
Add Recipient（受信者の追加）をクリックし、最初の選択肢として表示されているメールアドレスをクリックします。
通知サービス これは、そのメールアドレスを入力したときと同じです。または、E-mail… をクリックして別のメールアドレスを入力することもできます。
これは、予め用意されている多くの Notification Services の一例です。全てを確認するには、トップメニューの Integrations タブに移動し、Notification Services を参照してください。
6. アラートの有効化 Proceed to Alert Activation をクリックします。
Activivate… で Activate Alert Rule をクリックします。
アラートをより早く取得したい場合は、Alert Settings をクリックして、値を 290 から 280 に下げてみてください。
Time を -1h に変更すると、過去1時間のメトリクスに基づいて、選択した閾値でどれだけのアラートを取得できるかを確認できます。
ナビバーにある ボタンをクリックして、その後 Detectors をクリックすると、ディテクターの一覧が表示されます。あなたのイニシャルでフィルタして、作成したディテクターを確認しましょう。表示されない場合は、ブラウザをリロードしてみてください。
おめでとうございます！ 最初のディテクターが作成され、有効化されました。
`,description:"",tags:null,title:"ディテクターを利用する",uri:"/ja/imt/detectors/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > Pet Clinic Java ワークショップ",content:`1. RUMを有効にする Real User Monitoring (RUM)計装のために、Open Telemetry Javascript https://github.com/signalfx/splunk-otel-js-web スニペットをページ内に追加します。再度ウィザードを使用します Data Management → Add Integrationボタン → Monitor user experience（画面上部タブ） → Browser Instrumentationを開きます。
ドロップダウンから設定済みの RUM ACCESS TOKEN を選択し、Next をクリックします。以下の構文で App name とEnvironment を入力します：
次に、ワークショップのRUMトークンを選択し、 App nameとEnvironmentを定義します。ウィザードでは、ページ上部の <head> セクションに配置する必要のある HTML コードの断片が表示されます。この例では、次のように記述していますが、ウィザードでは先程入力した値が反映されてるはずです。
Application Name: <hostname>-petclinic-service Environment: <hostname>-petclinic-env ウィザードで編集済みコードスニペットをコピーするか、以下のスニペットをコピーして適宜編集してください。ただし：
[hostname]-petclinic-service - [hostname] をお使いのホスト名に書き換えてください [hostname]-petclinic-env - [hostname] をお使いのホスト名に書き換えてください <script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" crossorigin="anonymous"></script> <script> SplunkRum.init({ beaconUrl: "https://rum-ingest.<REALM>.signalfx.com/v1/rum", rumAuth: "<RUM_ACCESS_TOKEN>", app: "<hostname>.service", environment: "<hostname>" }); </script>Spring PetClinicアプリケーションでは、1つのHTMLページを「レイアウト」ページとして使用し、アプリケーションのすべてのページで再利用しています。これは、Splunk RUM計装ライブラリを挿入するのに最適な場所であり、すべてのページで自動的に読み込まれます。
では、レイアウトページを編集してみましょう：
nano src/main/resources/templates/fragments/layout.htmlそして、上で生成したスニップをページの <head> セクションに挿入してみましょう。さて、アプリケーションを再構築して、再び実行する必要があります。
2. PetClinicを再ビルドする mavenコマンドを実行して、PetClinicをコンパイル/ビルド/パッケージ化します：
./mvnw package -Dmaven.test.skip=trueそして、アプリケーションを動かしてみましょう。バージョンを version=0.316 とするのをお忘れなく。
java -javaagent:./splunk-otel-javaagent.jar \\ -Dserver.port=8083 \\ -Dotel.service.name=$(hostname).service \\ -Dotel.resource.attributes=deployment.environment=$(hostname),version=0.316 \\ -Dsplunk.profiler.enabled=true \\ -Dsplunk.profiler.memory.enabled=true \\ -Dsplunk.metrics.enabled=true \\ -jar target/spring-petclinic-*.jar --spring.profiles.active=mysql versionを自動で設定する ここまできて version を毎回変えるためにコマンドラインを修正するのは大変だと思うことでしょう。実際、修正が漏れた人もいるかもしれません。 本番環境では、環境変数でアプリケーションバージョンを与えたり、コンテナイメージの作成時にビルドIDを与えたりすることになるはずです。
次に、より多くのトラフィックを生成するために、アプリケーションに再度アクセスしてみましょう。 http://<VM_IP_ADDRESS>:8083 にアクセスすると、今度はRUMトレースが報告されるはずです。
RUMにアクセスして、トレースとメトリクスのいくつかを見てみましょう。左のメニューから RUM を選ぶと、Spring Pet Clinicでのユーザー（あなたです！）が体験したパフォーマンスが表示されます。
`,description:"",tags:null,title:"Real User Monitoring",uri:"/ja/other/pet-clinic/docs/rum/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk RUM",content:` RUMランディングページにアクセスし、アプリケーションサマリーダッシュボード（モバイルおよびウェブベース）でRUM対応アプリケーションすべてのパフォーマンスの概要を確認します。 1. RUMランディングページにアクセス Splunk IM/APM/RUM ウェブサイトにログインします。左側のメニューバーから RUM を選択します。 RUMのランディングページが表示されます。
このページの目的は、アプリケーションの健全性、パフォーマンス、潜在的なエラーを1つのページで明確に示し、Webページ/アプリケーションから収集したユーザーセッションに関する情報をより深く掘り下げることができるようにすることです。アクティブなRUMアプリケーションごとにペインが表示されます。(以下のビューは、デフォルトの拡張ビューです。）
複数のアプリケーションがある場合（RUMワークショップの参加者全員が自分のec2インスタンスを使用する場合）、以下のようにペインを折りたたむことで自動的にペインビューが縮小される場合があります。
アプリケーション名の前にある左側の赤い矢印で強調されている または アイコン(アプリケーションの種類が モバイル か ブラウザー かによる）をクリックすると、RUM Application Summryビューをフルダッシュボードに展開することが可能です。
まず、ワークショップに使用する適切なアプリケーションを見つけます。
単独のRUMワークショップに参加する場合、ワークショップ講師が使用するアプリケーションの名前を教えてくれます。複合ワークショップの場合、IMとAPMで使用した命名規則に従い、上のスクリーンショットの一番最後に表示されているように、 jmcj-store のようにユニークIDとしてEC2ノードの名前に従います。
2. RUM Application Summary ダッシュボード のヘッダーセクションを設定する RUM Application Summary ダッシュボードは5つの主要なセクションで構成されています。一つ目は選択ヘッダーで、多くのオプションを設定/フィルタリングすることができます。
表示対象時間のための タイム・ウィンドウ ドロップダウン（デフォルトでは過去15分間） Environment1 を選択するためのドロップダウン。これにより、その環境に属するアプリケーションのサブセットのみにフォーカスすることができます。 監視対象のさまざまな Apps を含むドロップダウンリスト。ワークショップ講師によって提供されたものを使用するか、あなた自身のものを選択することができます。これにより、1つのアプリケーションにフォーカスすることができます。 Source 、 Browser 、 Mobile アプリケーションを選択するためのドロップダウン。ワークショップの場合は、 All を選択したままにしてください。 ヘッダーの右側にあるハンバーガーメニューで、Splunk RUM アプリケーションのいくつかの設定を行うことができます(これについては、後のセクションで説明します)。 次のセクションでは「Application Summary」画面をより深く掘り下げて説明します。
デプロイメント環境（Environment）は、システムまたはアプリケーションの個別のデプロイメントであり、同じアプリケーションの他のデプロイメントの設定と重複しないように設定を行うことができます。開発、ステージング、本番など、開発プロセスの段階ごとに別々のデプロイメント環境を使用することがよくあります。 一般的なアプリケーションのデプロイメントパターンとして、互いに直接影響し合わない複数の異なるアプリケーション環境を持ち、それらをすべて Splunk APM または RUM で監視することがあります。たとえば、品質保証 (QA) 環境と本番環境、または異なるデータセンター、地域、クラウドプロバイダーでの複数の異なるデプロイメントが挙げられます。 ↩︎
`,description:"",tags:null,title:"4. RUMランディングページの確認",uri:"/ja/rum/4-rum-landing/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する",content:`プロセッサーは、レシーバーとエクスポーターとの間で、データに対して実行される処理です。プロセッサーはオプションですが、いくつかは推奨されています。OpenTelemetry Collector Contrib には多数のプロセッサーが含まれています。
%%{ init:{ "theme":"base", "themeVariables": { "primaryColor": "#ffffff", "clusterBkg": "#eff2fb", "defaultLinkColor": "#333333" } } }%% flowchart LR; style Processors fill:#e20082,stroke:#333,stroke-width:4px,color:#fff subgraph Collector A[OTLP] --> M(Receivers) B[JAEGER] --> M(Receivers) C[Prometheus] --> M(Receivers) end subgraph Processors M(Receivers) --> H(Filters, Attributes, etc) E(Extensions) end subgraph Exporters H(Filters, Attributes, etc) --> S(OTLP) H(Filters, Attributes, etc) --> T(JAEGER) H(Filters, Attributes, etc) --> U(Prometheus) end `,description:"",tags:null,title:"OpenTelemetry Collector プロセッサー",uri:"/ja/other/opentelemetry-collector/4-processors/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector サービス",content:`Attributes プロセッサー また、このワークショップのプロセッサーセクションでは、attributes/conf プロセッサーを追加し、コレクターがすべてのメトリクスに participant.name という新しい属性を挿入するようにしました。これをメトリクスパイプライン下で有効にする必要があります。
metrics パイプラインの下の processors セクションを更新して、attributes/conf を追加します：
service: pipelines: traces: receivers: [otlp, opencensus, jaeger, zipkin] processors: [batch] exporters: [logging] metrics: receivers: [hostmetrics, otlp, opencensus, prometheus/internal] processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf] exporters: [logging]`,description:"",tags:null,title:"OpenTelemetry Collector サービス",uri:"/ja/other/opentelemetry-collector/6-service/4-attributes/index.html"},{breadcrumb:"Splunk Observability Workshops",content:`Splunk Synthetic Monitoring は、完全なオブザーバビリティスイートである Splunk Observability Cloud の一部として、アップタイムと Webパフォーマンスの最適化のための最も包括的で詳細な機能を提供します。
API、サービスエンドポイント、エンドユーザーエクスペリエンスの監視を簡単に設定できます。Splunk Synthetic Monitoringを使用すれば、基本的な稼働時間やパフォーマンスの監視にとどまらず、問題の発見と修正、Web パフォーマンスの最適化、顧客が最高のユーザーエクスペリエンスを得られるようにすることに注力することができます。
Splunk Synthetic Monitoringによって得られるもの:
重要なユーザーフロー、ビジネストランザクション、APIエンドポイントにおける問題を迅速に検出し解決 インテリジェンスなWeb最適化エンジンで、Webパフォーマンスの問題が顧客に影響を与えることを防止 すべてのページリソースとサードパーティの依存関係のパフォーマンスを向上 `,description:"ユーザーフロー、ビジネストランザクション、APIにおけるパフォーマンスの問題を積極的に発見、修正し、より良いデジタル体験を提供します。",tags:null,title:"Splunk Synthetics",uri:"/ja/synthetics/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM > ダッシュボードを利用する",content:`1. 既存のダッシュボードに保存する 右上に YOUR_NAME-Dashboard と表示されていることを確認しましょう
これは、あなたのチャートがこのダッシュボードに保存されることを意味します。
チャートの名前を Latency History とし、必要に応じてチャートの説明を追加します。
Save And Close をクリックします。これで、ダッシュボードに戻ると2つのチャートが表示されているはずです！
では、先ほどのチャートを元に、もう一つのチャートをさくっと追加してみましょう。
2. チャートのコピー＆ペースト ダッシュボードの Latency History チャート上の3つのドット ... をクリックし、 Copy をクリックします。
ページ左上の + の横に赤い円と白い1が表示されていれば、チャートがコピーされているということになります。
ページ上部の をクリックし、メニューの Paste Charts をクリックしてください (また、右側に 1 が見える赤い点があるはずです)。
これにより、先程のチャートのコピーがダッシュボードに配置されます。
3. 貼り付けたチャートを編集する ダッシュボードの Latency History チャートの3つの点 ... をクリックし、Open をクリックします（または、チャートの名前（ここでは Latency History）をクリックすることもできます）。
すると、再び編集できる環境になります。
まず、チャートの右上にあるタイムボックスで、チャートの時間を -1h（1時間前から現在まで） に設定します。そして、シグナル「A」の前にある目のアイコンをクリックして再び表示させ、「C」 を非表示にし、Latency history の名前を Latency vs Load に変更します。
Add Metric Or Event ボタンをクリックします。これにより、新しいシグナルのボックスが表示されます。シグナル D に demo.trans.count と入力・選択します。
これにより、チャートに新しいシグナル D が追加され、アクティブなリクエストの数が表示されます。demo_datacenter:Paris のフィルタを追加してから、 Configure Plot ボタンをクリックしロールアップを Auto (Delta) から Rate/sec に変更します。名前を demo.trans.count から Latency vs Load に変更します。
最後に Save And Close ボタンを押します。これでダッシュボードに戻り、3つの異なるチャートが表示されます。
次のモジュールでは、「説明」のメモを追加して、チャートを並べてみましょう！
`,description:"",tags:null,title:"ダッシュボードにチャートを追加する",uri:"/ja/imt/dashboards/adding-charts/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM",content:` 10分 Terraform1 を使用して Observability Cloud のダッシュボードとディテクターを管理します。 Terraform のSplunk Provider2 を初期化します Terraformを実行して、Splunk Terraform Provider を使用してコードからディテクターとダッシュボードを作成します。 Terraformでディテクターやダッシュボードを削除する方法を確認します。 1. 初期設定 Monitoring as Codeは、infrastructure as Codeと同じアプローチを採用しています。アプリケーション、サーバー、その他のインフラコンポーネントと同じようにモニタリングを管理できます。
Monitoring as Codeでは、可視化したり、何を監視するか定義したり、いつアラートを出すかなどを管理します。つまり、監視設定、プロセス、ルールをバージョン管理、共有、再利用することができます。
Splunk Terraform Providerの完全なドキュメントはこちらにあります。
AWS/EC2 インスタンスにログインして、o11y-cloud-jumpstart ディレクトリに移動します
​ Change directory cd observability-content-contrib/integration-examples/terraform-jumpstart 必要な環境変数は、Helmによるインストール ですでに設定されているはずです。そうでない場合は、以下の Terraform のステップで使用するために、以下の環境変数を作成してください。
​ Export ACCESS TOKEN export ACCESS_TOKEN="<replace_with_O11y-Workshop-ACCESS_TOKEN>" ​ Export REALM export REALM="<replace_with_REALM>" Terraform を初期化し、Splunk Terraform Provider を最新版にアップグレードします。
Note: SignalFx Terraform Provider のアップグレード Splunk Terraform Provider の新バージョンがリリースされるたびに、以下のコマンドを実行する必要があります。リリース情報は GitHub で確認できます。
​ Initialise Terraform Initialise Output terraform init -upgrade Upgrading modules... - aws in modules/aws - azure in modules/azure - docker in modules/docker - gcp in modules/gcp - host in modules/host - kafka in modules/kafka - kubernetes in modules/kubernetes - parent_child_dashboard in modules/dashboards/parent - pivotal in modules/pivotal - rum_and_synthetics_dashboard in modules/dashboards/rum_and_synthetics - usage_dashboard in modules/dashboards/usage Initializing the backend... Initializing provider plugins... - Finding latest version of splunk-terraform/signalfx... - Installing splunk-terraform/signalfx v6.20.0... - Installed splunk-terraform/signalfx v6.20.0 (self-signed, key ID CE97B6074989F138) Partner and community providers are signed by their developers. If you'd like to know more about provider signing, you can read about it here: https://www.terraform.io/docs/cli/plugins/signing.html Terraform has created a lock file .terraform.lock.hcl to record the provider selections it made above. Include this file in your version control repository so that Terraform can guarantee to make the same selections by default when you run "terraform init" in the future. Terraform has been successfully initialized! You may now begin working with Terraform. Try running "terraform plan" to see any changes that are required for your infrastructure. All Terraform commands should now work. If you ever set or change modules or backend configuration for Terraform, rerun this command to reinitialize your working directory. If you forget, other commands will detect it and remind you to do so if necessary. 2. プランの作成 terraform plan コマンドで、実行計画を作成します。デフォルトでは、プランの作成は以下のように構成されています。
既に存在するリモートオブジェクトの現在の状態を読み込み、Terraform の状態が最新であることを確認します 現在の設定を以前の状態と比較し、相違点を抽出します 適用された場合にリモートオブジェクトと設定とを一致させるための、一連の変更アクションを提案します plan コマンドだけでは、提案された変更を実際に実行はされなません。変更を適用する前に、以下のコマンドを実行して、提案された変更が期待したものと一致するかどうかを確認しましょう。
​ Execution Plan Execution Plan Output terraform plan -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="o11y_prefix=[$(hostname)]" Plan: 146 to add, 0 to change, 0 to destroy. プランが正常に実行されれば、そのまま apply することができます。
3. プランの適用 terraform apply コマンドは、上記の Terraform プランで提案されたアクションを実行します。
この場合、新しい実行プランが自動的に作成され（terraform planを実行したときと同様です）、指示されたアクションを実行する前にAccess Token、Realm（プレフィックスのデフォルトはSplunk）の提供とプランの承認を求められます。
このワークショップでは、プレフィックスがユニークである必要があります。以下の terraform apply を実行してください。
​ Apply Plan Apply Plan Output terraform apply -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="o11y_prefix=[$(hostname)]" Apply complete! Resources: 146 added, 0 changed, 0 destroyed. 適用が完了したら、 Alerts → Detectors でディテクターが作成されたことを確認してください。ディテクターのプレフィックスには、インスタンスのホスト名が入ります。プレフィックスの値を確認するには以下を実行してください。
​ Echo Hostname echo $(hostname) 新しいディテクターのリストが表示され、上から出力されたプレフィックスを検索することができます。
4. 苦労して作ったもの全てを壊す terraform destroy コマンドは、Terraform の設定で管理されているすべてのリモートオブジェクトを破壊する便利な方法です。
通常、本番環境では長期保存可能なオブジェクトを破棄することはありませんが、Terraformでは開発目的で一時的なインフラを管理するために使用されることがあり、その場合は作業が終わった後に terraform destroy を実行して、一時的なオブジェクトをすべてクリーンアップすることができます。
それでは、ここまでで適用したダッシュボードとディテクターを全て破壊しましょう！
​ Destroy Destroy Output terraform destroy -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" Destroy complete! Resources: 146 destroyed. Alerts → Detectors に移動して、すべてのディテクターが削除されたことを確認してください。
Terraform は、インフラを安全かつ効率的に構築、変更、バージョン管理するためのツールです。Terraform は、既存の一般的なサービスプロバイダーだけでなく、様々なカスタムソリューションも管理できます。
Terraform の設定ファイルには、単一のアプリケーションまたはデータセンター全体を実行するために必要なコンポーネントをに記述します。Terraform はそれを受けて、望ましい状態に到達するために何をするかを記述した実行プランを生成し、記述されたインフラを構築するために実行します。設定が変更されても、Terraform は何が変更されたかを判断し、差分の実行プランを作成して適用することができます。
Terraform が管理できるインフラには、計算機インスタンス、ストレージ、ネットワークなどのローレベルのコンポーネントや、DNSエントリ、SaaS機能などのハイレベルのコンポーネントが含まれます。 ↩︎
プロバイダーは、APIのインタラクションを理解し、リソースを公開する責務があります。一般的にプロバイダーは、IaaS（Alibaba Cloud、AWS、GCP、Microsoft Azure、OpenStackなど）、PaaS（Herokuなど）、またはSaaSサービス（Splunk、Terraform Cloud、DNSimple、Cloudflareなど）があります。 ↩︎
`,description:"",tags:null,title:"Monitoring as Code",uri:"/ja/imt/monitoring-as-code/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > Pet Clinic Java ワークショップ",content:`このセクションでは、Spring PetClinicアプリケーションをファイルシステムのファイルにログを書き込むように設定し、 Splunk OpenTelemetry Collectorがそのログファイルを読み取り（tail）、Splunk Observability Platformに情報を報告するように設定していきます。
1. FluentDの設定 Splunk OpenTelemetry Collectorを、Spring PetClinicのログファイルをtailし Splunk Observability Cloudエンドポイントにデータを報告するように設定する必要があります。
Splunk OpenTelemetry Collectorは、FluentDを使用してログの取得/報告を行い、 Spring PetClinicのログを報告するための適切な設定を行うには、 デフォルトディレクトリ（/etc/otel/collector/fluentd/conf.d/）にFluentDの設定ファイルを追加するだけです。
以下は、サンプルのFluentD設定ファイル petclinic.conf を新たに作成し、
sudo nano /etc/otel/collector/fluentd/conf.d/petclinic.confファイル /tmp/spring-petclinic.logを読み取るよう設定を記述します。
<source> @type tail @label @SPLUNK tag petclinic.app path /tmp/spring-petclinic.log pos_file /tmp/spring-petclinic.pos_file read_from_head false <parse> @type none </parse> </source>このとき、ファイル petclinic.conf のアクセス権と所有権を変更する必要があります。
sudo chown td-agent:td-agent /etc/otel/collector/fluentd/conf.d/petclinic.conf sudo chmod 755 /etc/otel/collector/fluentd/conf.d/petclinic.confファイルが作成されたら、FluentDプロセスを再起動しましょう。
sudo systemctl restart td-agent3. Logbackの設定 Spring Pet Clinicアプリケーションは、いくつかのJavaログライブラリを使用することができます。 このシナリオでは、logbackを使ってみましょう。
リソースフォルダに logback.xml という名前のファイルを作成して…
nano src/main/resources/logback.xml以下の設定を保存しましょう:
<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE xml> <configuration scan="true" scanPeriod="30 seconds"> <contextListener class="ch.qos.logback.classic.jul.LevelChangePropagator"> <resetJUL>true</resetJUL> </contextListener> <logger name="org.springframework.samples.petclinic" level="debug"/> <appender name="file" class="ch.qos.logback.core.rolling.RollingFileAppender"> <file>/tmp/spring-petclinic.log</file> <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy"> <fileNamePattern>springLogFile.%d{yyyy-MM-dd}.log</fileNamePattern> <maxHistory>5</maxHistory> <totalSizeCap>1GB</totalSizeCap> </rollingPolicy> <encoder> <pattern> %d{yyyy-MM-dd HH:mm:ss} - %logger{36} - %msg trace_id=%X{trace_id} span_id=%X{span_id} trace_flags=%X{trace_flags} service.name=%property{otel.resource.service.name}, deployment.environment=%property{otel.resource.deployment.environment} %n </pattern> </encoder> </appender> <root level="debug"> <appender-ref ref="file" /> </root> </configuration>その後、アプリケーションを再構築して再度実行していきます。
./mvnw package -Dmaven.test.skip=truejava -javaagent:./splunk-otel-javaagent.jar \\ -Dserver.port=8083 \\ -Dotel.service.name=$(hostname).service \\ -Dotel.resource.attributes=deployment.environment=$(hostname),version=0.317 \\ -Dsplunk.profiler.enabled=true \\ -Dsplunk.profiler.memory.enabled=true \\ -Dsplunk.metrics.enabled=true \\ -jar target/spring-petclinic-*.jar --spring.profiles.active=mysqlこれまで通り、アプリケーション http://<VM_IP_ADDRESS>:8083 にアクセスしてトラフィックを生成すると、ログメッセージが報告されるようになります。
左側のLog Observerアイコンをクリックして、ホストとSpring PetClinicアプリケーションからのログメッセージのみを選択するためのフィルタを追加できます。
Add Filter → Field → host.name → <あなたのホスト名> Add Filter → Field → service.name → <あなたのホスト名>.service 4. まとめ これでワークショップは終了です。 これまでに、Splunk Observability Cloudにメトリクス、トレース、ログ、データベースクエリのパフォーマンス、コードプロファイリングが報告されるようになりました。 おめでとうございます！
`,description:"",tags:null,title:"Log Observer",uri:"/ja/other/pet-clinic/docs/logobserver/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する",content:`エクスポーターは、プッシュまたはプルベースであり、一つ以上のバックエンド/デスティネーションにデータを送信する方法です。エクスポーターは、一つまたは複数のデータソースをサポートすることがあります。
このワークショップでは、otlphttp エクスポーターを使用します。OpenTelemetry Protocol (OTLP) は、テレメトリーデータを伝送するためのベンダーニュートラルで標準化されたプロトコルです。OTLP エクスポーターは、OTLP プロトコルを実装するサーバーにデータを送信します。OTLP エクスポーターは、gRPC および HTTP/JSON プロトコルの両方をサポートします。
%%{ init:{ "theme":"base", "themeVariables": { "primaryColor": "#ffffff", "clusterBkg": "#eff2fb", "defaultLinkColor": "#333333" } } }%% flowchart LR; style Exporters fill:#e20082,stroke:#333,stroke-width:4px,color:#fff subgraph Collector A[OTLP] --> M(Receivers) B[JAEGER] --> M(Receivers) C[Prometheus] --> M(Receivers) end subgraph Processors M(Receivers) --> H(Filters, Attributes, etc) E(Extensions) end subgraph Exporters H(Filters, Attributes, etc) --> S(OTLP) H(Filters, Attributes, etc) --> T(JAEGER) H(Filters, Attributes, etc) --> U(Prometheus) end `,description:"",tags:null,title:"OpenTelemetry Collector エクスポーター",uri:"/ja/other/opentelemetry-collector/5-exporters/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk RUM",content:` ランディングページで利用できるUIとオプションに慣れる ページビュー/エラー、リクエスト/エラー、およびJavaScriptエラーを1つのビューで識別しする Web Vitalメトリクスと、ブラウザーアプリケーションに関連して発生したディテクターを確認する 1. Application Summary ダッシュボードの概要 1.1. ヘッダーバー 前のセクションで見たように、RUM Application Summary ダッシュボードは5つの主要セクションで構成されています。 最初のセクションは選択ヘッダーで、 ブラウザーアイコンまたはアプリケーション名の前の > を使用してペインを折りたたむことができます。また、アプリケーション名(下の例では jmcj-store )のリンクをクリックすると、Application Overview ページにアクセスできます。
また、右側のトリプルドット メニューから、 Application Overview や App Health ダッシュボード を開くことができます。
まず View Dashboard リンクをクリックし Browser App Health ダッシュボード を開きます（別タブで開かれます）。 次に元のRUMタブに戻り Open Application Overview リンクか、アプリの名前をクリックして、Application Overview ダッシュボードを開きます。
Application Overview と Browser App Health ダッシュボードを次のセクションで詳しく見ていきます。
2. Application Overview RUM Application Overview ダッシュボードでは 一目で アプリケーションの状態の概要を確認できます。
2.1. Page Views / Network Requests / Errors 最初セクションに表示されている Page Views / Errors と Network Requests and Errors チャートはアプリケーション内のリクエスト数と問題の傾向を示しています。 これは、Javascriptのエラーや、バックエンドサービスへのネットワーク呼び出しに失敗した可能性があります。
上の例では、Networkチャートではネットワーク呼び出しに失敗していないことがわかりますが、Page Viewsチャートでは多くのページで何らかのエラーが発生していることが確認できます。このようなエラーは一般ユーザーからは見えないことが多いのですが、Web サイトのパフォーマンスに重大な影響を与える可能性があります。
チャート上にカーソルをホバーすると Page Views / Network Requests / Errors の件数を確認できます。
2.2. JavaScript Errors 2番目のセクションでは、アプリケーションで発生したJavaScriptエラーの概要と、各エラーの件数が表示されます。 上の例では、3種類のJavaScriptエラーがあることがわかります。1つは選択した時間帯に29回発生し、他の2つはそれぞれ12回発生しています。
エラーの一つをクリックすると、ポップアウトが開き、時系列でエラーの概要（下図）が表示されます。また、JavaScript エラーのスタックトレースが表示され、問題が発生した場所を知ることができます（詳細については、次のセクションで説明します）。
2.3. Web Vitals 3番目のセクションでは、Googleがランキングシステムで使用する3つのメトリクスである重要な（Google）Web Vitalsを表示しており、エンドユーザーにとってのサイトの表示速度を非常によく表しています。
ご覧の通り、当サイトは3つのメトリクスすべてで Good スコアを獲得し、良好な動作をしています。これらのメトリクスは、アプリケーションの変更がもたらす影響を特定し、サイトのパフォーマンスを向上させるために使用することができます。
Web Vitalsペインに表示されているメトリクスをクリックすると、対応する Tag Spotlight ダッシュボードに移動します。例えば Largest Contentful Paint (LCP) をクリックすると、以下のスクリーンショットのようなダッシュボードが表示され、このメトリクスのパフォーマンスに関するタイムラインとテーブルビューを見ることができます。これにより、OS やブラウザーのバージョンなど、より一般的な問題の傾向を把握することができます。
2.4. Most Recent Detectors 4番目であり最後のセクションでは、アプリケーションでトリガーされたディテクターの概要を表示することにフォーカスしています。このスクリーンショット用にディテクターを作成しているため、皆さんのペインでは何も表示されていないはずです。次のセクションで実際にディテクターを追加し、トリガーされるようにします。
下のスクリーンショットでは、 RUM Aggregated View Detector のクリティカルアラートと、選択した時間ウィンドウでこのアラートが何回トリガーされたかを示す件数が表示されています。アラートが表示されている場合は、アラートの名前（青いリンクで表示されている）をクリックすると、アラートの詳細を表示するアラート概要ページに移動します（注意：この操作を行うと、現在のページから離れることになります。）
次のセクションに進む前に、RUM Application Summaryダッシュボードとその基礎となるチャートとダッシュボードを数分間試してみてください。
`,description:"",tags:null,title:"5. ブラウザーアプリケーションの健全性を一目で確認",uri:"/ja/rum/5-browser-app-summary/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector サービス",content:`OTLP HTTP エクスポーター ワークショップのエクスポーターセクションでは、otlphttp エクスポーターを設定して、メトリクスを Splunk Observability Cloud に送信するようにしました。これをメトリクスパイプライン下で有効にする必要があります。
metrics パイプラインの下の exporters セクションを更新して、otlphttp/splunk を追加します：
service: pipelines: traces: receivers: [otlp, opencensus, jaeger, zipkin] processors: [batch] exporters: [logging] metrics: receivers: [hostmetrics, otlp, opencensus, prometheus/internal] processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf] exporters: [logging, otlphttp/splunk] Ninja: コレクターの内部を観測する コレクターは、その動作に関する内部シグナルを捕捉しています。これには実行中のコンポーネントからの追加されるシグナルも含まれます。これは、データの流れに関する決定を行うコンポーネントが、その情報をメトリクスやトレースとして表面化する方法を必要とするためです。
なぜコレクターを監視するの？ これは「監視者を監視するのは誰か？」という種類の問題ですが、このような情報を表面化できることは重要です。コレクターの歴史の興味深い部分は、GoメトリクスのSDKが安定と考えられる前に存在していたことで、コレクターは当面の間、この機能を提供するために Prometheus エンドポイントを公開しています。
注意点 組織内で稼働している各コレクターの内部使用状況を監視することは、新しいメトリクス量（MTS）を大幅な増加させる可能性があります。Splunkディストリビューションはこれらのメトリクスをキュレーションしており、増加を予測するのに役立ちます。
Ninja ゾーン コレクターの内部オブザーバビリティを公開するためには、いくつかの設定を追加することがあります：
​ telemetry schema example-config.yml service: telemetry: logs: level: <info|warn|error> development: <true|false> encoding: <console|json> disable_caller: <true|false> disable_stacktrace: <true|false> output_paths: [<stdout|stderr>, paths...] error_output_paths: [<stdout|stderr>, paths...] initial_fields: key: value metrics: level: <none|basic|normal|detailed> # Address binds the promethues endpoint to scrape address: <hostname:port> service: telemetry: logs: level: info encoding: json disable_stacktrace: true initial_fields: instance.name: \${env:INSTANCE} metrics: address: localhost:8888 参照 https://opentelemetry.io/docs/collector/configuration/#service 完成した設定 Check-in完成した設定をレビューしてください ​ config.yaml 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 extensions: health_check: endpoint: 0.0.0.0:13133 pprof: endpoint: 0.0.0.0:1777 zpages: endpoint: 0.0.0.0:55679 receivers: hostmetrics: collection_interval: 10s scrapers: # CPU utilization metrics cpu: # Disk I/O metrics disk: # File System utilization metrics filesystem: # Memory utilization metrics memory: # Network interface I/O metrics & TCP connection metrics network: # CPU load metrics load: # Paging/Swap space utilization and I/O metrics paging: # Process count metrics processes: # Per process CPU, Memory and Disk I/O metrics. Disabled by default. # process: otlp: protocols: grpc: http: opencensus: # Collect own metrics prometheus/internal: config: scrape_configs: - job_name: 'otel-collector' scrape_interval: 10s static_configs: - targets: ['0.0.0.0:8888'] jaeger: protocols: grpc: thrift_binary: thrift_compact: thrift_http: zipkin: processors: batch: resourcedetection/system: detectors: [system] system: hostname_sources: [os] resourcedetection/ec2: detectors: [ec2] attributes/conf: actions: - key: participant.name action: insert value: "INSERT_YOUR_NAME_HERE" exporters: logging: verbosity: normal otlphttp/splunk: metrics_endpoint: https://ingest.\${env:REALM}.signalfx.com/v2/datapoint/otlp headers: X-SF-TOKEN: \${env:ACCESS_TOKEN} service: pipelines: traces: receivers: [otlp, opencensus, jaeger, zipkin] processors: [batch] exporters: [logging] metrics: receivers: [hostmetrics, otlp, opencensus, prometheus/internal] processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf] exporters: [logging, otlphttp/splunk] extensions: [health_check, pprof, zpages] ヒント コレクターを再起動する前に、設定ファイルを検証することをお勧めします。これは、組み込みの validate コマンドを使用して行うことができます：
​ Command Example error output otelcol-contrib validate --config=file:/etc/otelcol-contrib/config.yaml Error: failed to get config: cannot unmarshal the configuration: 1 error(s) decoding: * error decoding 'processors': error reading configuration for "attributes/conf": 1 error(s) decoding: * 'actions[0]' has invalid keys: actions 2023/06/29 09:41:28 collector server run finished with error: failed to get config: cannot unmarshal the configuration: 1 error(s) decoding: * error decoding 'processors': error reading configuration for "attributes/conf": 1 error(s) decoding: * 'actions[0]' has invalid keys: actions 動作する設定ができたので、コレクターを起動し、その後 zPages が報告している内容を確認しましょう。
​ Command otelcol-contrib --config=file:/etc/otelcol-contrib/config.yaml `,description:"",tags:null,title:"OpenTelemetry Collector サービス",uri:"/ja/other/opentelemetry-collector/6-service/5-otlphttp/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM > ダッシュボードを利用する",content:`1. メモの追加 ダッシュボードには、ダッシュボードの利用者を支援するための短い「説明」ペインを配置することがよくあります。
ここでは、 New Text Note ボタンをクリックして、ノートを追加してみましょう。
すると、ノートエディターが開きます。
ノートに単なるテキスト以外のものを追加できるように、Splunk ではこれらのノート/ペインで Markdown を使用できるようにしています。 Markdown は、ウェブページでよく使われるプレーンテキストを使ってフォーマットされたテキストを作成するための軽量なマークアップ言語です。
たとえば、以下のようなことができます (もちろん、それ以外にもいろいろあります)。
ヘッダー (様々なサイズで) 強調スタイル リストとテーブル リンク: 外部の Web ページ (ドキュメントなど) や他の Splunk IM ダッシュボードへの直接リンクできます 以下は、ノートで使用できる上記のMarkdownオプションの例です。
​ Sample Markdown text # h1 Big headings ###### h6 To small headings ##### Emphasis **This is bold text**, *This is italic text* , ~~Strikethrough~~ ##### Lists Unordered + Create a list by starting a line with \`+\`, \`-\`, or \`*\` - Sub-lists are made by indenting 2 spaces: - Marker character change forces new list start: * Ac tristique libero volutpat at + Facilisis in pretium nisl aliquet * Very easy! Ordered 1. Lorem ipsum dolor sit amet 2. Consectetur adipiscing elit 3. Integer molestie lorem at massa ##### Tables | Option | Description | | ------ | ----------- | | chart | path to data files to supply the data that will be passed into templates. | | engine | engine to be used for processing templates. Handlebars is the default. | | ext | extension to be used for dest files. | #### Links [link to webpage](https://www.splunk.com) [link to dashboard with title](https://app.eu0.signalfx.com/#/dashboard/EaJHrbPAEAA?groupId=EaJHgrsAIAA&configId=EaJHsHzAEAA "Link to the Sample chart Dashboard!") 上記をコピーボタンでコピーして、Edit ボックスにペーストしてみてください。 プレビューで、どのように表示されるか確認できます。
2. チャートの保存 ノートチャートに名前を付けます。この例では、Example text chart としました。そして、 Save And Close ボタンを押します。
これでダッシュボードに戻ると、メモが追加されました。
3. チャートの順序や大きさを変更 デフォルトのチャートの順番やサイズを変更したい場合は、ウィンドウをドラッグして、チャートを好きな場所に移動したり、サイズを変更したりすることができます。
チャートの 上側の枠 にマウスポインタを移動すると、マウスポインタがドラッグアイコンに変わります。これで、チャートを任意の場所にドラッグすることができます。
ここでは、 Latency vs Load チャートを Latency History と Example text chart の間に移動してください。
チャートのサイズを変更するには、側面または底面をドラッグします。
最後の練習として、ノートチャートの幅を他のチャートの3分の1程度にしてみましょう。チャートは自動的に、サポートしているサイズの1つにスナップします。他の3つのチャートの幅を、ダッシュボードの約3分の1にします。ノートを他のチャートの左側にドラッグして、他の23個のチャートに合わせてサイズを変更します。
最後に、時間を -1h に設定すると、以下のようなダッシュボードになります。
次は、ディテクターの登場です！
`,description:"",tags:null,title:"ノートの追加とダッシュボードのレイアウト",uri:"/ja/imt/dashboards/notes-and-layout/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk IM",content:` 10分 組織におけるObservability Cloudの利用状況を把握する Subscription Usage（サブスクリプション使用量）インターフェースを使って、使用量を追跡する チームを作成する チームへの通知ルールを管理する 使用量をコントロールする 1. 利用状況を把握する 組織内のObservability Cloudのエンゲージメントを完全に把握するには、左下 » を開き、Settings → Organization Overview を選択すると、Observability Cloud の組織がどのように使用されているかを示す以下のダッシュボードが表示されます。
左側のメニューには、メンバーのリストが表示され、右側には、ユーザー数、チーム数、チャート数、ダッシュボード数、ダッシュボードグループの作成数、様々な成長傾向を示すチャートが表示されます。
現在お使いのワークショップ組織では、ワークショップごとにデータが消去されるため、作業できるデータが少ないかもしれません。
このワークショップインスタンスの Organization Overview にある様々なチャートをじっくりとご覧ください。
2. Subscription Usage 契約に対する使用量を確認したい場合は、 Subscription Usage を選択します。
この画面では、使用量を計算して取り込むため、読み込みに数秒かかることがあります。
3. 使用量を理解する 下図のような画面が表示され、現在の使用量、平均使用量、およびホスト、コンテナ、カスタムメトリクス、高解像度メトリクスの各カテゴリごとの権利の概要が表示されます。
これらのカテゴリの詳細については、Monitor Splunk Infrastructure Monitoring subscription usage を参照してください。
4. 使用状況を詳しく調べる 一番上のチャートには、カテゴリーごとの現在のサブスクリプションレベルが表示されます（下のスクリーンショットでは、上部の赤い矢印で表示されています）。
また、4つのカテゴリーの現在の使用状況も表示されます（チャート下部の赤い線で示されています）。
この例では、「ホスト」が25個、「コンテナ」が0個、「カスタムメトリクス」が100個、「高解像度メトリクス」が0個であることがわかります。
下のグラフでは、現在の期間のカテゴリごとの使用量が表示されています（グラフの右上のドロップダウンボックスに表示されています）。
Average Usage と書かれた青い線は、Observability Cloudが現在のサブスクリプション期間の平均使用量を計算するために使用するものを示しています。
Info スクリーンショットからわかるように、Observability Cloudはコスト計算には最大値や95パーセンタイル値ではなく、実際の平均時間使用量を使用しています。これにより、超過料金のリスクなしに、パフォーマンステストやBlue/Greenスタイルのデプロイメントなどを行うことができます。
オプションを確認するには、左の Usage Metric ドロップダウンから異なるオプションを選択して表示するメトリックを変更するか、右のドロップダウンで Billing Period を変更します。
また、右側のドロップダウンでサブスクリプション期間を変更することもできます。
最後に、右側のペインには、お客様のサブスクリプションに関する情報が表示されます。
`,description:"",tags:null,title:"管理機能",uri:"/ja/imt/servicebureau/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk RUM",content:` RUM UIでRUMメトリクスとセッション情報を見る RUM & APM UIで相関するAPMトレースを見る 1. RUM Overview Pages RUM Application Summaryダッシュボードの右側のトリプルドット メニューから Open Application Overview を選択するか、アプリケーション名のリンク（以下の例では jmcj-store ）をクリックして Application Overviewページを開き、詳細情報を確認することができます。
以下のような RUM Application Overview ページが表示されます。
2. RUM Browserの概要 2.1. ヘッダー RUMのUIは、大きく6つのセクションで構成されています。一つ目は選択ヘッダーで、多くのオプションを設定/フィルタリングすることができます。
レビューする時間ウィンドウを選択するドロップダウン（この場合は過去15分）。 比較ウィンドウを選択するためのドロップダウン（現在のパフォーマンスをローリングウィンドウで比較します - この場合は1時間前と比較）。 Environmentを選択するドロップダウン (ワークショップ講師が提供するもの、またはこの例のように All を選択）。 様々なWebアプリのドロップダウン（ワークショップ講師が提供するものか、 All を使用）。 オプション ブラウザまたはモバイルメトリクスを選択するドロップダウン（ワークショップでは恐らく利用できません) 2.2. 概要ペイン ページの左側にある概要ペインでは、ロード時間が長くなったページの概要を確認することができます。
この例では checkout と cart ページに黄色の三角形でエラーを示しており、ロード時間が 2.38 秒から 5.50 秒に増加したことがわかります。
また、1分あたりのFrontend ErrorとBackend Errorsの件数の概要が表示され、このサイトでは3種類のJavaScriptエラーが発生していることが分かります。
最後の2つのペインでは、Top Page Views と Top Network Requests が表示されます。
2.3. Key Metricsペイン Key Metricsペインでは、毎分の JavaScript Errors と Network Errors の件数、また Backend/Resource Request Duration を確認できます。これらのメトリクスはサイトで問題が発生した場合に、発生個所を特定するのに非常に便利です。
2.4. Web Vitalsペイン Web Vitalsペインは、Web Vitalのメトリクスに基づいてエンドユーザーに提供しているエクスペリエンスに関する洞察を得たい場合に使用する場所です。 Web Vitalは、ウェブ上で優れたユーザーエクスペリエンスを提供するために不可欠な品質シグナルの統一ガイダンスを提供するGoogleのイニシアチブであり、3つの主要なパラメーターに焦点を当てています。
Largest Contentful Paint (LCP) （最大コンテンツの描画）：読み込みのパフォーマンスを測定するものです。良いユーザーエクスペリエンスを提供するために、LCPはページが読み込まれてから2.5秒以内に発生する必要があります。 First Input Delay (FID) （初回入力までの遅延時間）：インタラクティブ性を評価するものです。良いユーザーエクスペリエンスを提供するために、ページのFIDは100ミリ秒以下であるべきです。 Cumulative Layout Shift (CLS) （累積レイアウトシフト数）：視覚的な安定性を測定します。良いユーザーエクスペリエンスを提供するためには、CLSを 0.1 以下で維持する必要があります。 2.5. Other Metricsペイン Other Metricsペインでは、ページの初期ロード時間や完了までに時間がかかりすぎているタスクなどを中心に、その他のパフォーマンスメトリクスを確認することができます。
Time To First Byte (TTFB) ：クライアントのブラウザーがサーバーからレスポンスの最初のバイトを受信するまでの時間を測定します。サーバーがリクエストを処理し、レスポンスを送信するまでの時間が長いほど、訪問者のブラウザーがページを表示する際の速度が遅くなります。 Long Task Duration ：開発者がユーザーエクスペリエンス悪化を理解するために使用できるパフォーマンスメトリクスであり、問題の兆候である可能性もあります。 Long Task Count ：長いタスクの発生頻度を示すメトリクスで、これもユーザーエクスペリエンスの調査や問題の検出に使用されます。 2.6. Custom Eventペイン Custom Eventペインでは、監視しているウェブページに自分で追加したイベントのメトリクスが表示されます。
RUMを有効化したサイトで見れるように、以下の2行を追加しています。
const Provider = SplunkRum.provider; var tracer=Provider.getTracer('appModuleLoader');これらの行は、すべての新しいページに対して自動的にカスタムイベントを作成します。また、フレームワークや作成したイベントの一部ではないカスタムコードにこれらを追加することで、アプリケーションのフローをより良く理解することができます。 Custom Event Requests 、 Custom Event Error Rates 、 Custom Event Latency をサポートしています。
`,description:"",tags:null,title:"6. RUMメトリクスの分析",uri:"/ja/rum/6-analyzing-metrics/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する",content:`Service セクションでは、レシーバー、プロセッサー、エクスポーター、およびエクステンションにある設定に基づいて、コレクターで有効にするコンポーネントを設定していきます。
情報 コンポーネントが設定されていても、Service セクション内で定義されていない場合、そのコンポーネントは有効化されません。
サービスのセクションは、以下の3つのサブセクションで構成されています：
extensions（拡張機能） pipelines（パイプライン） telemetry（テレメトリー） デフォルトの設定では、拡張機能セクションが health_check、pprof、zpages を有効にするように設定されており、これらは以前のエクステンションのモジュールで設定しました。
service: extensions: [health_check, pprof, zpages]それでは、メトリックパイプラインを設定していきましょう！
`,description:"",tags:null,title:"OpenTelemetry Collector サービス",uri:"/ja/other/opentelemetry-collector/6-service/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk RUM",content:` より深く分析のために様々なエンドポイントのメトリクスビューを調査したりTag spotlightに送信されたTagを使用します。 1. CartエンドポイントのURLを探す RUMの概要ページから、Cart エンドポイントのURLを選択し、このエンドポイントで利用可能な情報をさらに深く掘り下げてみてください。
青色のURLをクリックすると、 Tag Spotlight の概要に遷移します。
ここでは、RUM トレースの一部として Splunk RUM に送信されたすべてのタグが表示されます。表示されるタグは、あなたが選択した概要に関連するものです。これらはトレースが送信されたときに自動的に作成された一般的なタグと、ウェブサイトの設定の一部でトレースに追加した追加タグです。
追加タグ 既に2つの追加タグを送信しています。それは皆さんのウェブサイトに追加された Beacon url に定義されている app: “[nodename]-store”, environment: “[nodename]-workshop” です（詳しくは後で確認します）。同様の方法で、タグを追加することができます。
この例では、以下のように Document Load Latency ビューを選択しています。
特定のメトリクスにフォーカスした以下のタグビューのいずれかを選択することができます。
2. Tag Spotlight内の情報を探索 Tag Spotlightは、チャートビューで異常値を確認したり、タグで問題を特定するのに役立つように設計されています。
Document Load Latency ビューで、Browser 、 Browser Version 、 OS Name タグビューを見ると、様々なブラウザーの種類とバージョン、そして基盤となるOSを確認することができます。 これにより、特定のブラウザやOSのバージョンに関連する問題が強調表示されるため、特定が容易になります。
上記の例では、Firefoxのレスポンスが最も遅く、様々なバージョンのブラウザ（Chrome）のレスポンスが異なること、Android端末のレスポンスが遅いことが分かります。
さらに、ISPや場所などに関連する問題を特定するために使用できる地域タグがあります。ここでは、Online Boutiqueにアクセスするために使用している場所を見つけることができます。以下のように、Online Boutiqueにアクセスしている都市や国をクリックしてドリルダウンしてください（City内のAmsterdam）。
以下のように選択した都市に関連するトレースのみが選択されます。
様々なタグを選択することでフィルターを構築することができ、現在の選択項目も確認できます。
フィルタを解除してすべてのトレースを表示するには、ページ右上の Clear All をクリックしてください。
概要ページが空であるか、 と表示されている場合、選択したタイムスロットでトレースが受信されていないことを示します。 左上のタイムウィンドウを広げる必要があります。例えば、Last 12 hours で調べることができます。
下の図のように表示したい時間帯を選択し、小さな虫眼鏡のアイコンをクリックして時間フィルタをセットにすることができます。
`,description:"",tags:null,title:"7. Tag Spotlightの使用",uri:"/ja/rum/7-tag-spotlight/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する",content:`Splunk Observability Cloud OpenTelemetry Collector を設定して Splunk Observability Cloud にメトリクスを送信するようにしたので、Splunk Observability Cloud でデータを見てみましょう。Splunk Observability Cloud　への招待を受け取っていない場合は、講師がログイン資格情報を提供します。
その前に、もう少し興味深くするために、インスタンスでストレステストを実行しましょう。これにより、ダッシュボードが活性化されます。
sudo apt install stress while true; do stress -c 2 -t 40; stress -d 5 -t 40; stress -m 20 -t 40; doneSplunk Observability Cloudにログインしたら、左側のナビゲーションを使用して Dashboards に移動します：
検索ボックスで OTel Contrib を検索します：
情報 ダッシュボードが存在しない場合は、講師が迅速に追加します。このワークショップの Splunk 主催版に参加していない場合、インポートするダッシュボードグループはこのページの下部にあります。
OTel Contrib Dashboard ダッシュボードをクリックして開きます：
ダッシュボードの上部にある Filter 欄に「participant」の途中まで入力し、候補に出る participant.name を選択します：
participant.name で、config.yaml 内で設定したあなたの名前を入力するか、リストから選択することができます：
これで、OpenTelemetry Collector を設定したホストの、ホストメトリクスを確認することができます。
ダッシュボードJSONのダウンロード方法 dashboard_OTel-Contrib-Dashboard.json (40 KB) `,description:"",tags:null,title:"データの可視化",uri:"/ja/other/opentelemetry-collector/7-visualisation/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する",content:`カスタムコンポーネントの開発 Open Telemetry Collectorのためのコンポーネントを構築するには、以下の3つの主要な部分が必要です：
Configuration - ユーザーが設定できる値は何か Factory - 提供された値を使ってコンポーネントを作成する Business Logic - コンポーネントが実行する必要があること これについて、プロジェクトの重要なDevOpsメトリクスを追跡するためにJenkinsと連携するコンポーネントを構築する例を考えていきます。
測定しようとしているメトリクスは次のとおりです：
変更に対するリードタイム - 「コミットが本番環境に入るまでにかかる時間」 変更失敗率 - 「本番環境での障害を引き起こすデプロイの割合」 デプロイ頻度 - 「[チーム]が本番環境に成功してリリースする頻度」 平均復旧時間 - 「[チーム]が本番環境の障害から復旧するのにかかる時間」 これらの指標は Google の DevOps Research and Assessment (DORA) チームによって特定されたもので、ソフトウェア開発チームのパフォーマンスを示すのに役立ちます。Jenkins CI を選択した理由は、私たちが同じオープンソースソフトウェアエコシステムに留まり、将来的にベンダー管理のCIツールが採用する例となることができるためです。
計装 🆚 コンポーネント 組織内でオブザーバビリティを向上させる際には、トレードオフが発生するため、考慮する点があります。
長所 短所 （自動）計装1 システムを観測するために外部APIが不要 計装を変更するにはプロジェクトの変更が必要 システム所有者/開発者は可観測性の変更が可能 ランタイムへの追加の依存が必要 システムの文脈を理解し、Exemplar とキャプチャされたデータを関連付けることが可能 システムのパフォーマンスに影響を与える可能性がある コンポーネント データ名や意味の変更をシステムのリリースサイクルから独立した展開が可能 APIの破壊的な変更の可能性があり、システムとコレクター間でリリースの調整が必要 その後の利用に合わせて収集されるデータの更新/拡張が容易 キャプチャされたデータの意味がシステムリリースと一致せず、予期せず壊れる可能性がある 計装（instrument, インストゥルメント）とは、アプリケーションなどのシステムコンポーネントに対して、トレースやメトリクス、ログなどのテレメトリーデータを出力させる実装。計装ライブラリを最低限セットアップするだけで一通りのトレースやメトリクスなどを出力できるような対応を「自動計装」と呼びます。 ↩︎
`,description:"",tags:null,title:"OpenTelemetry Collector を開発する",uri:"/ja/other/opentelemetry-collector/8-develop/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk RUM",content:` RUM UIでRUM Sessionの情報を調査する ユーザーインタラクションのSpanでJavascriptのエラーを特定する 1. cart URLを再び選択 タイムセレクタで時間帯を選択した後、以下のように Url Nameビューから cart URLを再選択する必要があります。
上の例では http://34.246.124.162:81/cart を選択しました。
2. Sessionsにドリルダウン Tag Spotlightで情報を分析し、トレースのサブセットをドリルダウンした後、エンドユーザーのブラウザーで実行された実際のセッションを表示することができます。
以下のように Example Sessions というリンクをクリックすることで行います。
これにより、時間フィルタとタグプロファイルで選択したサブセットの両方に一致するセッションのリストが表示されます。
セッションIDをクリックします。最も長い時間（700 ミリ秒以上が望ましい）のものを選択するとよいでしょう。
セッションを選択すると、セッションの詳細ページが表示されます。セッションの一部である特定のアクションを選択しているため、セッション内のどこかのインタラクションにたどり着く可能性が高いです。 先ほど選択したURL http://34.246.124.162:81/cart が、セッションストリームでフォーカスしている場所であることがわかります。
ページを少し下にスクロールすると、以下のように操作の終わりが表示されます。
エンドユーザーには検出されなかったか、または表示されなかった可能性のあるいくつかのJavaScript Consoleエラーが発生していることがわかります。これらのエラーを詳しく調べるには、真ん中のエラー Cannot read properties of undefined (reading ‘Prcie’) をクリックしてください。
これによってページが展開され、このインタラクションのSpanの詳細が表示されます。このページには、問題を解決するために開発者に渡すことができる詳細な error.stack が含まれます。Online Boutiqueで商品を購入した際、最終的な合計金額が常に0ドルであることにお気づきでしょうか。
`,description:"",tags:null,title:"8. RUM Sessionの分析",uri:"/ja/rum/8-rum-sessions/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector を開発する",content:`プロジェクトのセットアップ Ninja メモ このワークショップのセクションを完了する時間は経験によって異なる場合があります。
完成したものはこちらにあります。詰まった場合や講師と一緒に進めたい場合に利用してください。
新しい Jenkins CI レシーバーの開発を始めるため、まずは Go プロジェクトのセットアップから始めていきます。 新しい Go プロジェクトを作成する手順は以下の通りです：
\${HOME}/go/src/jenkinscireceiver という名前の新しいディレクトリを作成し、そのディレクトリに移動します。 実際のディレクトリ名や場所は厳密ではありません。自分の開発ディレクトリを自由に選ぶことができます。 go mod init splunk.conf/workshop/example/jenkinscireceiver を実行して、Go のモジュールを初期化します。 依存関係を追跡するために使用される go.mod というファイルが作成されます。 インポートされている依存関係のチェックサム値が go.sum として保存されます。 Check-ingo.modをレビューする \`\` text module splunk.conf/workshop/example/jenkinscireceiver
go 1.20
`,description:"",tags:null,title:"OpenTelemetry Collector を開発する",uri:"/ja/other/opentelemetry-collector/8-develop/1-project-setup/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk RUM",content:` RUM UIでRUM Sessionの情報を続けます APM & Log Observer UI で相関する APM トレースとログを確認します 1. バックエンドサービスの問題を発見 をクリックして、Spanビューを閉じます。 次に下にスクロールし、 POST /cart/checkout の行を見つけます。
青色の リンクをクリックすると、エンドユーザが行ったチェックアウト操作の一部であるバックエンドサービスに関する情報を示すダイアログがポップアップ表示されます。
このポップアップでは複数のセクションが用意されており、バックエンドサービスの挙動を素早く把握することができます。例えば、Performance Summaryセクションでは、バックエンドの呼び出し中にどこに時間が費やされたかを知ることができます。
上記の例では77.9%以上が外部サービスに費やされていることがわかります。
ダイアログの一番下までスクロールすると、下図のような「トレースとサービス」セクションが表示されます。
Checkout サービスと Payment サービスが、両方とも濃い赤色で表示されています。薄い赤はエラーを受け取ったことを意味し、濃い赤はそのサービスから発生したエラーを意味します。
つまり、すでにバックエンドのサービスに問題があることは明白なのです。
調査してみましょう！
2. Backendサービスまでのトレースをたどる Trace Idリンクをクリックすることができます。
これにより、バックエンドサービスへの呼び出しで何が起こったかを詳細に示すウォーターフォールAPMビューが表示されます。 右側には、Trace IDと、前に見たように、Performance Summuryが表示されています。 ウォーターフォールでは、フロントエンドからの呼び出しの一部である様々なバックエンドサービスを特定することができます。
ご覧のように、 Checkout サービスと Payment サービスの前に赤いエラーインジケータ が見えます。
paymentservice: grpc.hipstershop.PaymentService/Charge の行の後にある をクリックしてください。
Spanの詳細ページが表示され、このサービスコールの詳細情報が表示されます。 401 エラーコード、つまり Invalid Request が返されたことが確認できます。
3. 関連するログを確認 Splunk Observability Cloudは、トレースメトリクスとログを自動的に関連付けるため、ページ下部の関連コンテンツバーに、このトレースに対応するログが表示されます。
Logのリンクをクリックすると、ログが表示されます。
ログが表示されたら、ページの上部にあるフィルターにクリック元のTrace IDがセットされ、このトレースに関連するログが表示されていることに注意してください。 次にPaymentサービスのエラーを示す行の1つを選択すると右側にログメッセージが表示されます。
ここにPaymentサービスが失敗した理由が明確に示されています。サービスに対して無効なトークンを使用しているのです。
*Failed payment processing through ButtercupPayments: Invalid API Token (test-20e26e90-356b-432e-a2c6-956fc03f5609)
4. まとめ このワークショップではRUMをWebサイトに追加する方法を確認しました。 RUMメトリクスを使用してWebサイトのパフォーマンスを調査しました。 Tag Profileを使用して、自分のセッションを検索し、セッションウォーターフォールを使用して、2つの問題を特定しました。
JavaScriptのエラーにより、価格の計算が 0 になっていました。 支払いバックエンドサービスに問題があり支払いに失敗することがありました。 RUMのトレースとバックエンドAPMのトレースおよびログを関連付ける機能を使用して、支払い失敗の原因を発見しました。
`,description:"",tags:null,title:"9. Splunk RUM と APM バックエンドサービスの相関",uri:"/ja/rum/9-apm-correlation/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk RUM",content:` RUMメトリクスを使用して、問題が発生した場合に警告するAlertsを設定する RUMメトリクスに基づくカスタムチャートを作成する SplunkのRUMは完全忠実なソリューションとして設計されているため、お客様のトレースを100％取得することができ、Webサイトの動作の変化を検知して警告することができます。また、カスタムチャートとダッシュボードを作成することで、Webサイトの挙動を正確に把握することができます。 これにより、ウェブサイト、バックエンド・サービス、基盤となるインフラストラクチャからのデータを組み合わせることができます。これにより、お客様のアプリケーションやソリューションを構成する完全なスタックを観察することができます。
RUMメトリクスのチャートまたはアラートの作成は、インフラストラクチャのメトリクスと同じ方法で行います。このセクションでは、簡単なチャート、ディテクター、およびアラートを作成します。
Splunk IM ワークショップを受講したことがある方は、このセクションをよくご存知でしょう。Splunk IM ワークショップの経験がない場合は、RUM ワークショップの終了後に ダッシュボード と ディテクター モジュールを参照して、機能をよりよく理解することをお勧めします。
`,description:"",tags:null,title:"10. RUMメトリクスに基づくカスタムチャートとアラート",uri:"/ja/rum/10-alerting/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector を開発する",content:'Configuration の構築 コンポーネントの Configuration 部分は、ユーザーがコンポーネントに対する入力を行う方法であり、設定に使用される値は以下のようである必要があります：\nそのフィールドが何を制御するのか、ユーザーが直感的に理解できる 必須項目とオプション項目が明確である 共通の名前とフィールドを再利用する オプションをシンプルに保つ ​ 良い config 悪い config --- # Required Values endpoint: http://my-jenkins-server:8089 auth: authenticator: basicauth/jenkins # Optional Values collection_interval: 10m metrics: example.metric.1: enabled: true example.metric.2: enabled: true example.metric.3: enabled: true example.metric.4: enabled: true --- jenkins_server_addr: hostname jenkins_server_api_port: 8089 interval: 10m filter_builds_by: - name: my-awesome-build status: amber track: values: example.metric.1: yes example.metric.2: yes example.metric.3: no example.metric.4: no 悪い例では、Configuration のベストプラクティスに反するとコンポーネントが使いにくくなってしまうことが理解できるはずです。 フィールドの値が何であるべきかを明確ではなく、既存のプロセッサーに移譲できる機能を含み、コレクター内の他のコンポーネントと比較してフィールドの命名に一貫性がありません。\n良い例では、必要な値をシンプルに保ち、他のコンポーネントからのフィールド名を再利用し、コンポーネントが Jenkins とコレクター間の相互作用にのみ焦点を当てています。\n設定値の中には、このコンポーネントで独自に追加するものと、コレクター内部の共有ライブラリによって提供されているものがあります。これらはビジネスロジックに取り組む際にさらに詳しく説明します。Configuration は小さく始めるべきで、ビジネスロジックに追加の機能が必要になったら、設定も追加していきましょう。\nコードを書く Configuration に必要なコードを実装するために、config.go という名前の新しいファイルを以下の内容で作成します：\npackage jenkinscireceiver import ( "go.opentelemetry.io/collector/config/confighttp" "go.opentelemetry.io/collector/receiver/scraperhelper" "splunk.conf/workshop/example/jenkinscireceiver/internal/metadata" ) type Config struct { // HTTPClientSettings contains all the values // that are commonly shared across all HTTP interactions // performed by the collector. confighttp.HTTPClientSettings `mapstructure:",squash"` // ScraperControllerSettings will allow us to schedule // how often to check for updates to builds. scraperhelper.ScraperControllerSettings `mapstructure:",squash"` // MetricsBuilderConfig contains all the metrics // that can be configured. metadata.MetricsBuilderConfig `mapstructure:",squash"` }',description:"",tags:null,title:"OpenTelemetry Collector を開発する",uri:"/ja/other/opentelemetry-collector/8-develop/2-configuration/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops",content:`概要 OpenTelemetry を使い始める場合は、バックエンドに直接データを送ることから始めるかもしれません。最初のステップとしてはよいですが、OpenTelemetry Collector をオブザーバビリティのアーキテクチャとして使用するのは多くの利点があり、本番環境では Collector を使ったデプロイを推奨しています。
このワークショップでは、OpenTelemetry Collector を使用することに焦点を当て、Splunk Observability Cloud で使用するためのレシーバー、プロセッサー、エクスポーターを定義し、実際にテレメトリデータを送信するためのパイプラインを設定することで、環境に合わせて Collector を活用を学びます。また、分散プラットフォームのビジネスニーズに対応するための、カスタムコンポーネントを追加できるようになるまでの道のりを進むことになります。
Ninja セクション ワークショップの途中には、展開できる Ninja セクション があります。これらはより実践的で、ワークショップ中、もしくは自分の時間を使って、さらに技術的な詳細に取り組むことができます。
OpenTelemetry プロジェクトは頻繁に開発されているため、Ninjaセクションの内容が古くなる可能性があることに注意してください。コンテンツが古い場合には更新のリクエストを出すこともできますので、必要なものを見つけた場合はお知らせください。
Ninja: をテストして！ このワークショップを完了すると、正式に OpenTelemetry Collector ニンジャになります！
対象者 このワークショップは、OpenTelemetry Collector のアーキテクチャとデプロイメントについてさらに学びたいと考えている開発者やシステム管理者を対象としています。
前提条件 データ収集に関する基本的な理解 コマンドラインとvim/viの経験 Ubuntu 20.04 LTSまたは22.04 LTSが稼働するインスタンス/ホスト/VM 最小要件はAWS/EC2 t2.micro（1 CPU、1GB RAM、8GBストレージ） 学習目標 このセッションの終わりまでに、参加者は以下を行うことができるようになります：
OpenTelemetry のコンポーネントを理解する レシーバー、プロセッサー、エクスポーターを使用してデータを収集・分析する OpenTelemetry を使用する利点を特定する 自分たちのビジネスニーズに対応するカスタムコンポーネントを構築する OpenTelemetry のアーキテクチャー %%{ init:{ "theme":"base", "themeVariables": { "primaryColor": "#ffffff", "clusterBkg": "#eff2fb", "defaultLinkColor": "#333333" } } }%% flowchart LR; subgraph Collector A[OTLP] --> M(Receivers) B[JAEGER] --> M(Receivers) C[Prometheus] --> M(Receivers) end subgraph Processors M(Receivers) --> H(Filters, Attributes, etc) E(Extensions) end subgraph Exporters H(Filters, Attributes, etc) --> S(OTLP) H(Filters, Attributes, etc) --> T(JAEGER) H(Filters, Attributes, etc) --> U(Prometheus) end `,description:"OpenTelemetry Collectorのコンセプトを学び、Splunk Observability Cloudにデータを送信する方法を理解しましょう。",tags:null,title:"OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する",uri:"/ja/other/opentelemetry-collector/index.html"},{breadcrumb:"Splunk Observability Workshops > Splunk RUM",content:` Mobile RUMの簡単な紹介 Application Summary ダッシュボードで、モバイルアプリケーションの パフォーマンスの概要を確認できます 1. RUM Application Summary ダッシュボードにアクセス 左側のメニューバーから RUM を選択します。これで、RUM Application Summryページが表示されます。
このページの目的は、アプリケーションの健全性、パフォーマンス、潜在的なエラーを1つのペイン/ダッシュボードに表示し、Webサイトに対して実行されたユーザーセッションに関する情報を深く掘り下げることができるようにすることです。
アクティブな RUM アプリケーションごとにペインが表示されます。(以下のビューは、デフォルトの拡張ビューです。）
複数のアプリケーションを使用している場合、以下のようにペインが自動的に折りたたまれ、ペインビューが縮小されることがあります。
アプリケーション名の前にある左側の赤い矢印で強調されている または アイコン(アプリケーションの種類が モバイル か ブラウザー かによる）をクリックすると、RUM Application Summryビューをフルダッシュボードに展開することが可能です。
2. RUM Mobileの概要 Splunk RUM は Apple iPhone と Android Phone 向けの Native Mobile RUM をサポートしています。スマートフォンのネイティブアプリのエンドユーザーエクスペリエンスを確認するために使用することができます。
上の画面は、Splunk Mobile RUM が追跡できるさまざまなメトリクスやデータを表示するものです。例えば、以下のようなものです。
Custom events ：ブラウザーアプリケーションのものと同様です。 App Errors ：1分あたりの アプリエラー と クラッシュ 。 App Lifecycle Performance ：OSごとの コールドスタートアップ時間 、 ホットスタートアップ時間 。 Request/Response ：ブラウザーアプリケーションのものと同様です。 この時点では、スマートフォン上でネイティブアプリを実行するか、エミュレーションを実行する必要があるため、Mobile RUMについて深く掘り下げることはしません。必要に応じて、より詳細な情報をデモで提供することができます。
`,description:"",tags:null,title:"11. モバイルアプリケーション (紹介)",uri:"/ja/rum/11-mobile-app-summary/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector を開発する",content:`コンポーネントを検討する Jenkinsからメトリクスを取得するために必要なコンポーネントの種類をおさらいしましょう：
​ エクステンション レシーバー プロセッサー エクスポーター Ninja: コネクター エクステンションが解決するビジネスユースケースは以下の通りです：
実行時の設定が必要な共有機能を持つ コレクターの実行時間の観察に間接的に役立つ 詳細については、エクステンションの概要を参照してください。
レシーバーが解決するビジネスユースケースは以下の通りです：
リモートソースからのデータの取得 リモートソースからのデータの受信 これらは一般的に pull 対 push ベースのデータ収集と呼ばれ、詳細についてはレシーバーの概要で読むことができます。
プロセッサーが解決するビジネスユースケースは以下の通りです：
データ、フィールド、または値の追加または削除 データの観察と意思決定 バッファリング、キューイング、および並べ替え プロセッサーを通過するデータタイプは、下流のコンポーネントに同じデータタイプを転送する必要があることを覚えておいてください。 詳細については、プロセッサーの概要をご覧ください。
エクスポーターが解決するビジネスユースケースは以下の通りです：
データをツール、サービス、またはストレージに送信する OpenTelemetryコレクターは「バックエンド」、すべてを一元化した観測可能性スイートを目指すのではなく、OpenTelemetryの創設原則に忠実であり続けることを目指しています。つまり、ベンダーに依存しない全ての人のための観測可能性です。詳細については、エクスポーターの概要をお読みください。
コネクターは比較的新しいコンポーネントで、このワークショップではあまり触れていません。 コネクターは、異なるテレメトリタイプやパイプラインをまたいで使用できるプロセッサーのようなものだといえます。たとえば、コネクターはログとしてデータを受け取り、メトリクスとして出力したり、あるパイプラインからメトリクスを受け取り、テレメトリーデータに関するメトリクスを提供したりすることができます。
コネクターが解決するビジネスケースは以下の通りです：
異なるテレメトリタイプ間の変換 ログからメトリクスへ トレースからメトリクスへ メトリクスからログへ 受信したデータを観察し、自身のデータを生成する メトリクスを受け取り、データの分析メトリクスを生成する。 Ninjaセクションの一部としてプロセッサーの概要内で簡単に概要が説明されています。
これらのコンポーネントについて考えると、Jenkins に対応する場合はプルベースのレシーバーを開発する必要があることがわかります。
`,description:"",tags:null,title:"OpenTelemetry Collector を開発する",uri:"/ja/other/opentelemetry-collector/8-develop/3-component/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector を開発する",content:'メトリクスを設計する レシーバーによってキャプチャされるメトリクスを定義し、エクスポートするために、コレクターのために開発された mdatagen を使って、yaml で定義したメトリクスをコードに変換していきます。\n​ metadata.yaml gen.go --- # Type defines the name to reference the component # in the configuration file type: jenkins # Status defines the component type and the stability level status: class: receiver stability: development: [metrics] # Attributes are the expected fields reported # with the exported values. attributes: job.name: description: The name of the associated Jenkins job type: string job.status: description: Shows if the job had passed, or failed type: string enum: - failed - success - unknown # Metrics defines all the pontentially exported values from this receiver. metrics: jenkins.jobs.count: enabled: true description: Provides a count of the total number of configured jobs unit: "{Count}" gauge: value_type: int jenkins.job.duration: enabled: true description: Show the duration of the job unit: "s" gauge: value_type: int attributes: - job.name - job.status jenkins.job.commit_delta: enabled: true description: The calculation difference of the time job was finished minus commit timestamp unit: "s" gauge: value_type: int attributes: - job.name - job.status // To generate the additional code needed to capture metrics, // the following command to be run from the shell: // go generate -x ./... //go:generate go run github.com/open-telemetry/opentelemetry-collector-contrib/cmd/mdatagen@v0.80.0 metadata.yaml package jenkinscireceiver // There is no code defined within this file. 次のセクションに進む前に、これらのファイルをプロジェクトフォルダ内に作成してください。\nFactory の構築 Factory はソフトウェアデザインパターンの一種で、提供された Configuration を使って、動的にオブジェクト（この場合は jenkinscireceiver）を作成するものです。現実的な例では、携帯電話店に行って、あなたの正確な説明に合った携帯電話を求め、それを提供されるようなものです。\nコマンド go generate -x ./... を実行すると、定義されたメトリクスをエクスポートするために必要なすべてのコードを含む新しいフォルダ jenkinscireceiver/internal/metadata が作成されます。生成されるコードは以下の通りです：\n​ factory.go config.go scraper.go build-config.yaml project layout package jenkinscireceiver import ( "errors" "go.opentelemetry.io/collector/component" "go.opentelemetry.io/collector/config/confighttp" "go.opentelemetry.io/collector/receiver" "go.opentelemetry.io/collector/receiver/scraperhelper" "splunk.conf/workshop/example/jenkinscireceiver/internal/metadata" ) func NewFactory() receiver.Factory { return receiver.NewFactory( metadata.Type, newDefaultConfig, receiver.WithMetrics(newMetricsReceiver, metadata.MetricsStability), ) } func newMetricsReceiver(_ context.Context, set receiver.CreateSettings, cfg component.Config, consumer consumer.Metrics) (receiver.Metrics, error) { // Convert the configuration into the expected type conf, ok := cfg.(*Config) if !ok { return nil, errors.New("can not convert config") } sc, err := newScraper(conf, set) if err != nil { return nil, err } return scraperhelper.NewScraperControllerReceiver( &conf.ScraperControllerSettings, set, consumer, scraperhelper.AddScraper(sc), ) } package jenkinscireceiver import ( "go.opentelemetry.io/collector/config/confighttp" "go.opentelemetry.io/collector/receiver/scraperhelper" "splunk.conf/workshop/example/jenkinscireceiver/internal/metadata" ) type Config struct { // HTTPClientSettings contains all the values // that are commonly shared across all HTTP interactions // performed by the collector. confighttp.HTTPClientSettings `mapstructure:",squash"` // ScraperControllerSettings will allow us to schedule // how often to check for updates to builds. scraperhelper.ScraperControllerSettings `mapstructure:",squash"` // MetricsBuilderConfig contains all the metrics // that can be configured. metadata.MetricsBuilderConfig `mapstructure:",squash"` } func newDefaultConfig() component.Config { return &Config{ ScraperControllerSettings: scraperhelper.NewDefaultScraperControllerSettings(metadata.Type), HTTPClientSettings: confighttp.NewDefaultHTTPClientSettings(), MetricsBuilderConfig: metadata.DefaultMetricsBuilderConfig(), } } package jenkinscireceiver type scraper struct {} func newScraper(cfg *Config, set receiver.CreateSettings) (scraperhelper.Scraper, error) { // Create a our scraper with our values s := scraper{ // To be filled in later } return scraperhelper.NewScraper(metadata.Type, s.scrape) } func (scraper) scrape(ctx context.Context) (pmetric.Metrics, error) { // To be filled in return pmetrics.NewMetrics(), nil } --- dist: name: otelcol description: "Conf workshop collector" output_path: ./dist version: v0.0.0-experimental extensions: - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/basicauthextension v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/healthcheckextension v0.80.0 receivers: - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/jaegerreceiver v0.80.0 - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/prometheusreceiver v0.80.0 - gomod: splunk.conf/workshop/example/jenkinscireceiver v0.0.0 path: ./jenkinscireceiver processors: - gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.80.0 exporters: - gomod: go.opentelemetry.io/collector/exporter/loggingexporter v0.80.0 - gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.80.0 - gomod: go.opentelemetry.io/collector/exporter/otlphttpexporter v0.80.0 # This replace is a go directive that allows for redefine # where to fetch the code to use since the default would be from a remote project. replaces: - splunk.conf/workshop/example/jenkinscireceiver => ./jenkinscireceiver ├── build-config.yaml └── jenkinscireceiver ├── go.mod ├── config.go ├── factory.go ├── scraper.go └── internal └── metadata これらのファイルがプロジェクトに作成されたら、go mod tidy を実行します。すると、すべての依存ライブラリが取得され、go.mod が更新されます。\n',description:"",tags:null,title:"OpenTelemetry Collector を開発する",uri:"/ja/other/opentelemetry-collector/8-develop/4-design/index.html"},{breadcrumb:"Splunk Observability Workshops > Ninja Workshops > OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現する > OpenTelemetry Collector を開発する",content:`ビジネスロジックを作る この時点では、何も行っていないカスタムコンポーネントが作成されています。ここから、Jenkins からデータを取得するための必要なロジックを追加していきましょう。
ここからのステップは以下の通りです：
Jenkinsに接続するクライアントを作成する 設定されたすべてのジョブをキャプチャする 設定されたジョブの最後のビルドのステータスを報告する コミットタイムスタンプとジョブ完了の時間差を計算する 変更を scraper.go に加えていきます。
​ Jenkins クライアントを追加する ジョブをキャプチャする ジョブの状態を報告する 差分を報告する Jenkinsサーバーに接続するために、パッケージ “github.com/yosida95/golang-jenkins” を使用します。これには、Jenkinsサーバーからデータを読み取るために必要な機能が提供されています。
次に、“go.opentelemetry.io/collector/receiver/scraperhelper” ライブラリのいくつかのヘルパー関数を利用して、コンポーネントの起動が完了したらJenkinsサーバーに接続できるようにするスタート関数を作成します。
package jenkinscireceiver import ( "context" jenkins "github.com/yosida95/golang-jenkins" "go.opentelemetry.io/collector/component" "go.opentelemetry.io/collector/pdata/pmetric" "go.opentelemetry.io/collector/receiver" "go.opentelemetry.io/collector/receiver/scraperhelper" "splunk.conf/workshop/example/jenkinscireceiver/internal/metadata" ) type scraper struct { mb *metadata.MetricsBuilder client *jenkins.Jenkins } func newScraper(cfg *Config, set receiver.CreateSettings) (scraperhelper.Scraper, error) { s := &scraper{ mb : metadata.NewMetricsBuilder(cfg.MetricsBuilderConfig, set), } return scraperhelper.NewScraper( metadata.Type, s.scrape, scraperhelper.WithStart(func(ctx context.Context, h component.Host) error { client, err := cfg.ToClient(h, set.TelemetrySettings) if err != nil { return err } // The collector provides a means of injecting authentication // on our behalf, so this will ignore the libraries approach // and use the configured http client with authentication. s.client = jenkins.NewJenkins(nil, cfg.Endpoint) s.client.SetHTTPClient(client) return nil }), ) } func (s scraper) scrape(ctx context.Context) (pmetric.Metrics, error) { // To be filled in return pmetric.NewMetrics(), nil }これで、Jenkinsレシーバーを初期化するために必要なすべてのコードが完成しました。
ここから先は、実装が必要な scrape メソッドに焦点を当てます。このメソッドは、設定された間隔（デフォルトでは1分）ごとに実行されます。
Jenkins サーバーの負荷状況や、どの程度のプロジェクトが実行されているかを測定するために、Jenkins で設定されているジョブの数をキャプチャしたいと考えています。これを行うために、Jenkins クライアントを呼び出してすべてのジョブをリスト化し、エラーが報告された場合はメトリクスなしでそれを返し、そうでなければメトリクスビルダーからのデータを発行します。
func (s scraper) scrape(ctx context.Context) (pmetric.Metrics, error) { jobs, err := s.client.GetJobs() if err != nil { return pmetric.Metrics{}, err } // Recording the timestamp to ensure // all captured data points within this scrape have the same value. now := pcommon.NewTimestampFromTime(time.Now()) // Casting to an int64 to match the expected type s.mb.RecordJenkinsJobsCountDataPoint(now, int64(len(jobs))) // To be filled in return s.mb.Emit(), nil } 前のステップにより、すべてのジョブをキャプチャしてジョブの数をレポートできるようになりました。 このステップでは、それぞれのジョブを調査し、レポートされた値を使用してメトリクスをキャプチャしていきます。
func (s scraper) scrape(ctx context.Context) (pmetric.Metrics, error) { jobs, err := s.client.GetJobs() if err != nil { return pmetric.Metrics{}, err } // Recording the timestamp to ensure // all captured data points within this scrape have the same value. now := pcommon.NewTimestampFromTime(time.Now()) // Casting to an int64 to match the expected type s.mb.RecordJenkinsJobsCountDataPoint(now, int64(len(jobs))) for _, job := range jobs { // Ensure we have valid results to start off with var ( build = job.LastCompletedBuild status = metadata.AttributeJobStatusUnknown ) // This will check the result of the job, however, // since the only defined attributes are // \`success\`, \`failure\`, and \`unknown\`. // it is assume that anything did not finish // with a success or failure to be an unknown status. switch build.Result { case "aborted", "not_built", "unstable": status = metadata.AttributeJobStatusUnknown case "success": status = metadata.AttributeJobStatusSuccess case "failure": status = metadata.AttributeJobStatusFailed } s.mb.RecordJenkinsJobDurationDataPoint( now, int64(job.LastCompletedBuild.Duration), job.Name, status, ) } return s.mb.Emit(), nil } 最後のステップでは、コミットからジョブ完了までにかかった時間を計算して、DORA メトリクス を推測するのに役立てていきます。
func (s scraper) scrape(ctx context.Context) (pmetric.Metrics, error) { jobs, err := s.client.GetJobs() if err != nil { return pmetric.Metrics{}, err } // Recording the timestamp to ensure // all captured data points within this scrape have the same value. now := pcommon.NewTimestampFromTime(time.Now()) // Casting to an int64 to match the expected type s.mb.RecordJenkinsJobsCountDataPoint(now, int64(len(jobs))) for _, job := range jobs { // Ensure we have valid results to start off with var ( build = job.LastCompletedBuild status = metadata.AttributeJobStatusUnknown ) // Previous step here // Ensure that the \`ChangeSet\` has values // set so there is a valid value for us to reference if len(build.ChangeSet.Items) == 0 { continue } // Making the assumption that the first changeset // item is the most recent change. change := build.ChangeSet.Items[0] // Record the difference from the build time // compared against the change timestamp. s.mb.RecordJenkinsJobCommitDeltaDataPoint( now, int64(build.Timestamp-change.Timestamp), job.Name, status, ) } return s.mb.Emit(), nil } これらのステップがすべて完了すると、Jenkins CI レシーバーが完成します！
次は何をするの？ コンポーネントに必要な機能は、おそらく他にもたくさん思いつくでしょう。例えば：
ジョブで使用されたブランチ名を含めることはできますか？ ジョブのプロジェクト名を含めることはできますか？ プロジェクトのジョブの総持続時間をどのように計算しますか？ 変更が機能するかどうかをどのように検証しますか？ この時間を使って遊んでみたり、壊してみたり、変更してみたり、ビルドからのログをキャプチャしてみるなどしてください。
`,description:"",tags:null,title:"OpenTelemetry Collector を開発する",uri:"/ja/other/opentelemetry-collector/8-develop/5-business-logic/index.html"},{breadcrumb:"Splunk Observability Workshops",content:` Pet Clinic Java ワークショップJavaアプリケーションをつかったSplunk Oservabilityのワークショップです
OpenTelemetryでクラウドネイティブ環境のオブザーバビリティを実現するOpenTelemetry Collectorのコンセプトを学び、Splunk Observability Cloudにデータを送信する方法を理解しましょう。
`,description:"",tags:null,title:"Ninja Workshops",uri:"/ja/other/index.html"},{breadcrumb:"Splunk Observability Workshops",content:` よくある質問とその回答オブザーバビリティ、DevOps、インシデント対応、Splunk On-Callに関連する一般的な質問とその回答を集めました。
ディメンション、プロパティ、タグディメンションとプロパティの比較で、どちらかを使うべきかというのはよく議論されます。
OpenTelemetryとSplunkにおける、タグ付けのための命名規則大規模な組織で OpenTelemetry を展開する際には、タグ付けのための標準化された命名規則を定義し、規則が遵守されるようにガバナンスプロセスを確立することが重要です。
`,description:"",tags:null,title:"その他のリソース",uri:"/ja/resources/index.html"},{breadcrumb:"Splunk Observability Workshops",content:"",description:"",tags:null,title:"Categories",uri:"/ja/categories/index.html"},{breadcrumb:"Splunk Observability Workshops",content:"",description:"",tags:null,title:"Tags",uri:"/ja/tags/index.html"}]