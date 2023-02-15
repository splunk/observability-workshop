var relearn_search_index=[{content:` 5 分 各自に割り当てられたAWS/EC2インスタンスのIPアドレスを確認します SSH、Putty1、またはWebブラウザを使ってインスタンスに接続します クラウド上にある AWS/EC2 インスタンスへの接続を確認します 1. AWS/EC2 の IP アドレス ワークショップの準備として、Splunk は AWS/EC2 に Ubuntu Linux インスタンスを用意しています。
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
`,description:"",tags:null,title:"ワークショップ環境へのアクセス",uri:"/observability-workshop/v4.55/ja/imt/initial-setup/index.html"},{content:` 15分 Online BoutiqueアプリケーションをKubernetes(K3s)にデプロイします アプリケーションが動作していることを確認します Locustを使って人工的なトラフィックを生成します UI で APM のメトリクスを見ましょう 1. EC2サーバーを確認 これからの操作は、IMワークショップを実行した後で、まだEC2インスタンスにアクセスできる状態であることを想定しています。 もしアクセスできる場合は、 2. Online Boutiqueをデプロイする に進みます。 新しいインスタンスを受け取った場合は、 データを取り込む の最初の2つのセクションを実行して、システムをAPMワークショップのために準備し、次のセクションを続行してください。
2. Online Boutiqueをデプロイする Online BoutiqueアプリケーションをK3sにデプロイするには、以下のデプロイメントを適用します。
Deploy Online Boutique Deployment Output cd ~/workshop/apm ./apm-config.sh kubectl apply -f deployment.yaml APM Only Deployment deployment.apps/recommendationservice created service/recommendationservice created deployment.apps/productcatalogservice created service/productcatalogservice created deployment.apps/cartservice created service/cartservice created deployment.apps/adservice created service/adservice created deployment.apps/paymentservice created service/paymentservice created deployment.apps/loadgenerator created service/loadgenerator created deployment.apps/shippingservice created service/shippingservice created deployment.apps/currencyservice created service/currencyservice created deployment.apps/redis-cart created service/redis-cart created deployment.apps/checkoutservice created service/checkoutservice created deployment.apps/frontend created service/frontend created service/frontend-external created deployment.apps/emailservice created service/emailservice created deployment.apps/rum-loadgen-deployment created 変数未セットに関するメッセージが表示された場合 kubectl delete -f deployment.yaml コマンドを実行しAPM環境のデプロイ削除します。 次にガイド、メッセージに表示されていた変数をexportし上記のデプロイスクリプトを再実行します。
Online Boutique アプリケーションが起動していることを確認するには:
Get Pods Get Pods Output kubectl get pods NAME READY STATUS RESTARTS AGE splunk-otel-collector-k8s-cluster-receiver-56585564cc-xclzj 1/1 Running 0 84s splunk-otel-collector-agent-hkshj 1/1 Running 0 84s svclb-frontend-external-c74n6 1/1 Running 0 53s currencyservice-747b74467f-xxrl9 1/1 Running 0 52s redis-cart-74594bd569-2jb6c 1/1 Running 0 54s adservice-6fb948b8c6-2xlrc 0/1 Running 0 53s recommendationservice-b5df8776c-sbt4h 1/1 Running 0 53s shippingservice-6d6f7b8d87-5lg9g 1/1 Running 0 53s svclb-loadgenerator-jxwct 1/1 Running 0 53s emailservice-9dd74d87c-wjdqr 1/1 Running 0 53s checkoutservice-8bcd56b46-bfj7d 1/1 Running 0 54s productcatalogservice-796cdcc5f5-vhspz 1/1 Running 0 53s paymentservice-6c875bf647-dklzb 1/1 Running 0 53s frontend-b8f747b87-4tkxn 1/1 Running 0 53s cartservice-59d5979db7-bqf64 1/1 Running 1 53s loadgenerator-57c8b84966-7nr4f 1/1 Running 3 53s Info 通常、ポッドがRunning状態に移行するのに1分30秒程度かかります。
3. UIで検証する Splunk UIでInfrastructure をクリックします。Infrastructure Overviewダッシュボードに遷移しますので、 Kubernetes をクリックします。
Cluster のドロップダウンを使用してクラスタを選択すると、新しいポッドが開始され、コンテナがデプロイされていることが確認できます。
Splunk UI で Cluster をクリックすると、次のような画面が表示されているはずです。
もう一度 WORKLOADS タブを選択すると、いくつかのデプロイメントとレプリカセットがあることがわかるはずです。
4. Online Boutique を閲覧する Online Boutique は、EC2インスタンスのIPアドレスの81番ポートで閲覧できます。このIPアドレスは、ワークショップの冒頭でインスタンスにSSH接続したときに使用したものと同じIPアドレスです。
ウェブブラウザを開き、 http://\u003cEC2-IP\u003e:81/ にアクセスすると、Online Boutique が起動しているのが確認できます。
`,description:"Online BoutiqueアプリケーションをKubernetes（K3s）にデプロイし、Locustを使って人工的なトラフィックを発生させます。",tags:null,title:"1. Online Boutiqueのデプロイ",uri:"/observability-workshop/v4.55/ja/apm/online-boutique/index.html"},{content:`RUM ワークショップの概要 このSplunk Real User Monitoring (RUM) ワークショップの目的は以下の通りです。
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
`,description:"",tags:null,title:"1. 概要",uri:"/observability-workshop/v4.55/ja/rum/1-overview/index.html"},{content:`1. チャートの編集 Sample Data ダッシュボードにある Latency histogram チャートの3点 ... をクリックして、Open をクリックします（または、チャートの名前をクリックしてください、ここでは Latency histogram です）。
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
`,description:"",tags:null,title:"チャートを編集する",uri:"/observability-workshop/v4.55/ja/imt/dashboards/editing/index.html"},{content:` ミューティングルールを設定する 通知を再開する 1. ミューティングルールの設定 特定の通知をミュートする必要がある場合があります。例えば、サーバーやサーバー群のメンテナンスのためにダウンタイムを設定したい場合や、新しいコードや設定をテストしている場合などがあります。このような場合には、Splunk Observability Cloud でミューティングルールを使用できます。それでは作成してみましょう。
ナビバーにある ボタンをクリックし、Detectors を選択します。現在設定されているディテクターの一覧が表示されます。フィルタを使ってディテクターを探すこともできます。
Creating a Detector でディテクターを作成した場合は、右端の3つの点 ... をクリックすると、そのディテクターが表示されます。
ドロップダウンから Create Muting Rule… をクリックします。
Muting Rule ウィンドウで、 Mute Indefinitely をチェックし、理由を入力します。
Important この操作をすると、ここに戻ってきてこのボックスのチェックを外すか、このディテクターの通知を再開するまで、通知が永久的にミュートされます。
Next をクリックして、新しいモーダルウィンドウでミュートルールの設定を確認します。
Mute Indefinitely   をクリックして、設定を確定させます。
これで、通知を再開するまで、ディテクターからのEメール通知は受け取ることがなくなりました。では、再開する方法を見てみましょう。
2. 通知を再開する Muting Rules をクリックして、Detector の見出しの下に、通知をミュートしたディテクターの名前が表示されます。
右端にあるドット ... を開いて、Resume Notifications をクリックします。
Resume   をクリックして、このディテクターの通知を確認し、再開します。
おめでとうございます！ これでアラート通知が再開されました。
`,description:"",tags:null,title:"ミューティングルールを利用する",uri:"/observability-workshop/v4.55/ja/imt/detectors/muting/index.html"},{content:` チームの管理 チームの作成とメンバーの追加 1. チームの管理 Observability Cloudを使用する際に、ユーザーに関連するダッシュボードやアラートが表示されるようにするために、ほとんどの組織ではObservability Cloudのチーム機能を使用して、メンバーを1つまたは複数のチームに割り当てます。
これは、仕事に関連した役割と一致するのが理想的で、たとえば、DevOpsグループやプロダクトマネジメントグループのメンバーは、Observability Cloudの対応するチームに割り当てられます。
ユーザーがObservability Cloudにログインすると、どのチームダッシュボードをホームページにするかを選択することができ、通常は自分の主な役割に応じたページを選択します。
以下の例では、ユーザーは開発、運用、プロダクトマネジメントの各チームのメンバーであり、現在は運用チームのダッシュボードを表示しています。
このダッシュボードには、NGINX、Infra、K8s用の特定のダッシュボード・グループが割り当てられていますが、どのダッシュボード・グループもチーム・ダッシュボードにリンクすることができます。
左上のメニューを使って割り当てられたチーム間を素早く移動したり、右側の ALL TEAMS ドロップダウンを使って特定のチームのダッシュボードを選択したり、隣のリンクを使って ALL Dashboards に素早くアクセスしたりすることができます。
アラートを特定のチームにリンクすることで、チームは関心のあるアラートだけをモニターすることができます。上記の例では、現在1つのアクティブなクリティカルアラートがあります。
チームダッシュボードの説明文はカスタマイズ可能で、チーム固有のリソースへのリンクを含むことができます（Markdownを使用します）。
2. 新しいチームの作成 Splunk のチーム UI を使用するには、左下の » を開き、 Settings → Teams を選択します。
Team を選択すると、現在のチームのリストが表示されます。
新しいチームを追加するには、 Create New Team   ボタンをクリックします。これにより、Create New Team ダイアログが表示されます。
独自のチームを作ってみましょう。チーム名を [あなたのイニシャル]-Team のように入力し、あなた自身のユーザー選んで、Add リンクからチームに追加してみましょう。上手くいくと、次のような表示になるはずです。
選択したユーザーを削除するには、Remove または x を押します。
自分のイニシャルでグループを作成し、自分がメンバーとして追加されていることを確認して、 Done   をクリックします。
これでチームリストに戻り、自分のチームと他の人が作成したチームが表示されます。
Note 自分がメンバーになっているチームには、グレーの Member アイコンが前に表示されています。
自分のチームにメンバーが割り当てられていない場合は、メンバー数の代わりに青い Add Members のリンクが表示されます。このリンクをクリックすると、Edit Team ダイアログが表示され、自分を追加することができます。
自分のチームの行末にある3つのドット … を押しても、Edit Team と同じダイアログが表示されます。
… メニューでは、チームの編集、参加、離脱、削除を行うことができます（離脱と参加は、あなたが現在メンバーであるかどうかによって異なります）。
3. 通知ルールの追加 チームごとに特定の通知ルールを設定することができます。Notification Policy タブをクリックすると、通知編集メニューが表示されます。
デフォルトでは、システムはチームの一般的な通知ルールを設定する機能を提供します。
Note Email all team members オプションは、アラートの種類に関わらず、このチームのすべてのメンバーにアラート情報のメールが送信されることを意味します。
3.1 受信者の追加 Add Recipient   をクリックすると、他の受信者を追加することができます。これらの受信者は Observability Cloud のユーザーである必要はありません。
Configure separate notification tiers for different severity alerts をクリックすると、各アラートレベルを個別に設定できます。
上の画像のように、異なるアラートレベルに対して異なるアラートルールを設定することができます。
Critical と Major は Splunk On-Call インシデント管理ソリューションを使用しています。Minor のアラートはチームの Slack チャンネルに送信し、Warning と Info はメールで送信する、という管理もできるようになります。
3.2 通知機能の統合 Observability Cloud では、アラート通知をメールで送信するだけでなく、以下のようなサービスにアラート通知を送信するように設定することができます。
チームの事情に合わせて、通知ルールを作成してください。
`,description:"",tags:null,title:"チーム",uri:"/observability-workshop/v4.55/ja/imt/servicebureau/teams/index.html"},{content:`この テクニカル Splunk Observability Cloud ワークショップでは、 lightweight Kubernetes1 クラスタをベースにした環境を構築します。
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
`,description:"オンプレミス、ハイブリッド、マルチクラウドのいずれにおいても、Splunk はリアルタイムの監視とトラブルシューティングを提供し、完全な可視化によってインフラのパフォーマンスを最大化することを支援します。",tags:null,title:"Splunk IM",uri:"/observability-workshop/v4.55/ja/imt/index.html"},{content:`Splunk Observabilityワークショップへようこそ Splunk Observability Cloud の監視、分析、対応ツールを使用して、アプリケーションとインフラストラクチャをリアルタイムで把握することができます。
このワークショップでは、メトリクス、トレース、ログを取り込み、監視し、可視化し、分析するためのクラス最高のオブザーバビリティ（可観測性）プラットフォームについて説明します。
OpenTelemetry このワークショップでOpenTelemetryをアプリケーションやインフラの分析に役立つテレメトリデータ（メトリクス、トレース、ログ）の計装、生成、収集、エクスポートに使用します。
GitHub このドキュメントには、issue や pull request で 貢献 することができます。より良いワークショップにするために、是非ご協力ください。
Twitter SplunkのTwitterチャンネルでは、アップデート情報や興味深い読み物を紹介しています。
Splunk IMオンプレミス、ハイブリッド、マルチクラウドのいずれにおいても、Splunk はリアルタイムの監視とトラブルシューティングを提供し、完全な可視化によってインフラのパフォーマンスを最大化することを支援します。
Splunk APMSplunk APM は、クラウドネイティブ、マイクロサービスベースのアプリケーションのための NoSample™ Full-fidelity アプリケーションパフォーマンス監視およびトラブルシューティングソリューションです。
Splunk RUMエンド・ツー・エンドの可視化により、Webブラウザやネイティブモバイルアプリからバックエンドサービスに至るまで、顧客に影響を与える問題をピンポイントで特定することができます。
Splunk Syntheticsユーザーフロー、ビジネストランザクション、APIにおけるパフォーマンスの問題を積極的に発見、修正し、より良いデジタル体験を提供します。
`,description:"Splunk を使用したオブザーバビリティソリューションの構築方法をご紹介します。",tags:null,title:"Splunk Observability Workshops",uri:"/observability-workshop/v4.55/ja/index.html"},{content:`このラボでは Chrome Selenium IDE エクステンションを使用したSplunkデモインスタンスに対する合成トランザクションと、Splunk Synthetic Monitoring Real Browser Check (RBC)を作成します。
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
`,description:"",tags:null,title:"Real Browser Checks",uri:"/observability-workshop/v4.55/ja/synthetics/real-browser-checks/index.html"},{content:` 5分 1. トラフィックを発生させる Online Boutique のデプロイメントには、Locust が動作するコンテナが含まれており、これを使用してウェブサイトに対する負荷トラフィックを生成し、メトリクス、トレース、スパンを生成することができます。
Locust は、EC2インスタンスのIPアドレスの82番ポートで利用できます。ウェブブラウザで新しいタブを開き、 http://\u003cEC2-IP\u003e:82/ にアクセスすると、Locust が動作しているのが確認できます。
Spawn rate を 2 に設定し、Start Swarming をクリックすると、アプリケーションに緩やかな負荷がかかり続けます。
それでは、 Dashboards → All Dashboards → APM Services → Service を開きましょう。
そのためには、アプリケーションの Environment 名を知る必要があります。このワークショップでは、\u003chostname\u003e-apm-env のような Environment 名で定義されています。
ホスト名を調べるには、AWS/EC2インスタンス上で以下のコマンドを実行します:
Echo Hostname Output Example echo $(hostname)-apm-env bdzx-apm-env 前のステップで見つけた Environment を選択し、「frontend」サービスを選択し、時間を「Past 15 minutes」に設定します。
この自動生成されたダッシュボードでは、RED (Rate, Error \u0026 Duration) メトリクスを使用して、サービスの状態を監視することができます。このダッシュボードでは、パフォーマンスに関連したさまざまなチャートのほか、基盤となるホストやKubernetesポッド（該当する場合）の相関情報も提供されます。
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
Lynx Command lynx http://localhost:55679/debug/tracez `,description:"",tags:null,title:"1.1 Locustでトラフィックを発生させる",uri:"/observability-workshop/v4.55/ja/apm/online-boutique/locust/index.html"},{content:`API Checkは、APIエンドポイントの機能およびパフォーマンスをチェックする柔軟な方法を提供します。APIファーストの開発へのシフトにより、フロントエンドのコア機能を提供するバックエンドサービスを監視する必要性が高まっています。複数ステップのAPIインタラクションのテストに興味がある場合でも、エンドポイントのパフォーマンスを可視化したい場合でも、API Checkは目標の達成に役立ちます。
1. グローバル変数の作成 API Checkを行うために使用するグローバル変数を表示します。 Admin Tools の下にある Global Variables をクリックします。 spotifyのAPIトランザクションを行うために使用するグローバル変数を確認してください。
2. API Check の作成 新しい API Check を作成し、\u003cあなたのイニシャル\u003e の後に Splunk REST API Check をつけた名前にします （例: AP - Spotify API）
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
`,description:"",tags:null,title:"API Checks",uri:"/observability-workshop/v4.55/ja/synthetics/api-checks/index.html"},{content:` 15分 Splunk Helm chartを使用して、K3s に OpenTelemetry Collector をインストールします Kubernetes Navigatorでクラスタを探索します 1. Access Tokenの取得 Kubernetes が起動したら、Splunk の UI から Access Token1 を取得する必要があります。Access Token は、左下にある » を開き、 Settings → Access Tokens を選択すると表示されます。
主催者が指示したワークショップトークン（例： O11y-Workshop-ACCESS 等）を開き、 Show Token をクリックしてトークンを公開します。 Copy   ボタンをクリックし、クリップボードにコピーしてください。 Default のトークンは使用しないでください。
独自のトークンを新たに作成しないようにしてください このワークショップのために設定のトークンを作成し、IngestとAPIの両方の権限を割り当てています。実運用でのベストプラクティスは、1つのTokenにはIngestまたはAPIまたはRUMのような単一のパーミッションを割り当て、必要な場合は複数のトークンを使用することです。
また、Splunk アカウントの Realm2 の名前を取得する必要があります。サイドメニューの最上部の名前をクリックし、Account Settings ページに移動します。Organizations タブをクリックします。Realm はページの中央に表示されています。 この例では「us0」となっています。
2. Helmによるインストール 環境変数 ACCESS_TOKEN と REALM を作成して、進行中の Helm のインストールコマンドで使用します。例えば、Realm が us1 の場合は、export REALM=us1 と入力し、eu0 の場合は、export REALM=eu0 と入力します。
Export ACCESS TOKEN export ACCESS_TOKEN="\u003creplace_with_O11y-Workshop-ACCESS_TOKEN\u003e" Export REALM export REALM="\u003creplace_with_REALM\u003e" Splunk Helm チャートを使って OpenTelemetry Collector をインストールします。まず、Splunk Helm chart のリポジトリを Helm に追加してアップデートします。
Helm Repo Add Helm Repo Add Output helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart \u0026\u0026 helm repo update Using ACCESS_TOKEN={REDACTED} Using REALM=eu0 “splunk-otel-collector-chart” has been added to your repositories Using ACCESS_TOKEN={REDACTED} Using REALM=eu0 Hang tight while we grab the latest from your chart repositories… …Successfully got an update from the “splunk-otel-collector-chart” chart repository Update Complete. ⎈Happy Helming!⎈
以下のコマンドでOpenTelemetry Collector Helmチャートをインストールします。これは 変更しないでください。
Helm Install Helm Install Output Install Network Explorer helm install splunk-otel-collector \\ --set="splunkObservability.realm=$REALM" \\ --set="splunkObservability.accessToken=$ACCESS_TOKEN" \\ --set="clusterName=$(hostname)-k3s-cluster" \\ --set="splunkObservability.logsEnabled=true" \\ --set="splunkObservability.profilingEnabled=true" \\ --set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \\ --set="environment=$(hostname)-apm-env" \\ splunk-otel-collector-chart/splunk-otel-collector \\ -f ~/workshop/k3s/otel-collector.yaml Using ACCESS_TOKEN={REDACTED} Using REALM=eu0 NAME: splunk-otel-collector LAST DEPLOYED: Fri May 7 11:19:01 2021 NAMESPACE: default STATUS: deployed REVISION: 1 TEST SUITE: None
helm install splunk-otel-collector \\ --set="splunkObservability.realm=$REALM" \\ --set="splunkObservability.accessToken=$ACCESS_TOKEN" \\ --set="clusterName=$(hostname)-k3s-cluster" \\ --set="splunkObservability.logsEnabled=true" \\ --set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \\ --set="networkExplorer.enabled=true" \\ --set="networkExplorer.podSecurityPolicy.enabled=false" \\ --set="agent.enabled=true" \\ --set="gateway.replicaCount=1" \\ --set="gateway.resources.limits.cpu=500m" \\ --set="gateway.resources.limits.memory=1Gi" \\ --set="clusterReceiver.enabled=true" \\ --set="environment=$(hostname)-apm-env" \\ splunk-otel-collector-chart/splunk-otel-collector \\ -f ~/workshop/k3s/otel-collector.yaml 約30秒程度待ってから kubectl get pods を実行すると、新しいポッドが稼働していることが報告され、デプロイメントの進捗を監視することができます。
続行する前に、ステータスがRunningと報告されていることを確認してください。
Kubectl Get Pods Kubectl Get Pods Output kubectl get pods NAME READY STATUS RESTARTS AGE splunk-otel-collector-agent-2sk6k 0/1 Running 0 10s splunk-otel-collector-k8s-cluster-receiver-6956d4446f-gwnd7 0/1 Running 0 10s
OpenTelemetry Collector podのログを確認して、エラーがないことを確認します。出力は、以下の出力例にあるログに似ているはずです。
ログを確認するには、helm のインストールで設定したラベルを使用してください（終了するには ctrl+c を押します）。もしくは、インストールされている k9s ターミナル UI を使うとボーナスポイントがもらえます！
Kubectl Logs Kubectl Logs Output kubectl logs -l app=splunk-otel-collector -f --container otel-collector 2021-03-21T16:11:10.900Z INFO service/service.go:364 Starting receivers… 2021-03-21T16:11:10.900Z INFO builder/receivers_builder.go:70 Receiver is starting… {“component_kind”: “receiver”, “component_type”: “prometheus”, “component_name”: “prometheus”} 2021-03-21T16:11:11.009Z INFO builder/receivers_builder.go:75 Receiver started. {“component_kind”: “receiver”, “component_type”: “prometheus”, “component_name”: “prometheus”} 2021-03-21T16:11:11.009Z INFO builder/receivers_builder.go:70 Receiver is starting… {“component_kind”: “receiver”, “component_type”: “k8s_cluster”, “component_name”: “k8s_cluster”} 2021-03-21T16:11:11.009Z INFO k8sclusterreceiver@v0.21.0/watcher.go:195 Configured Kubernetes MetadataExporter {“component_kind”: “receiver”, “component_type”: “k8s_cluster”, “component_name”: “k8s_cluster”, “exporter_name”: “signalfx”} 2021-03-21T16:11:11.009Z INFO builder/receivers_builder.go:75 Receiver started. {“component_kind”: “receiver”, “component_type”: “k8s_cluster”, “component_name”: “k8s_cluster”} 2021-03-21T16:11:11.009Z INFO healthcheck/handler.go:128 Health Check state change {“component_kind”: “extension”, “component_type”: “health_check”, “component_name”: “health_check”, “status”: “ready”} 2021-03-21T16:11:11.009Z INFO service/service.go:267 Everything is ready. Begin running and processing data. 2021-03-21T16:11:11.009Z INFO k8sclusterreceiver@v0.21.0/receiver.go:59 Starting shared informers and wait for initial cache sync. {“component_kind”: “receiver”, “component_type”: “k8s_cluster”, “component_name”: “k8s_cluster”} 2021-03-21T16:11:11.281Z INFO k8sclusterreceiver@v0.21.0/receiver.go:75 Completed syncing shared informer caches. {“component_kind”: “receiver”, “component_type”: “k8s_cluster”, “component_name”: “k8s_cluster”}
インストールに失敗した場合に削除する OpenTelemetry Collectorのインストールに失敗した場合は、次のようにしてインストールを削除することで、最初からやり直すことができます。
helm delete splunk-otel-collector 3. UI でメトリクスを確認する Splunk の UI で左下の » を開いて Infrastructure をクリックします。
Containers の下にある Kubernetes をクリックして Kubernetes Navigator Cluster Map を開き、メトリクスが送信されていることを確認します。
クラスタが検出され、レポートされていることを確認するには、自分のクラスタを探します（ワークショップでは、他の多くのクラスタが表示されます）。クラスタ名を見つけるには、以下のコマンドを実行し、出力をクリップボードにコピーしてください。
Echo Cluster Name echo $(hostname)-k3s-cluster 次に、UIで、Splunkロゴのすぐ下にある「Cluster: - 」メニューをクリックし、先程コピーしたクラスタ名を検索ボックスに貼り付け、チェックボックスをクリックしてクラスタを選択し、最後にメニューのその他の部分をクリックしてフィルタを適用します。
ノードの状態を確認するには、クラスターの淡いブルーの背景にカーソルを置き、左上に表示される青い虫眼鏡をクリックしてください 。 これで、ノードレベルまでドリルダウンできます。 次に、サイドバーボタンをクリックしてサイドバーを開き、Metricsサイドバーを開きます。
サイドのスライダーを使って、CPU、メモリ、ネットワーク、イベントなど、クラスタ/ノードに関連する様々なチャートを見ることができます。
Access Tokens (Org Tokensと呼ばれることもあります)は、長期間利用を前提とした組織レベルのトークンです。デフォルトでは、これらのトークンは 5 年間保存されます。そのため、長期間にわたってデータポイントを送信するエミッターに組み込んだり、Splunk API を呼び出す長期的なスクリプトに使用したりするのに適しています。 ↩︎
Realm とは、Splunk内部の管理単位ので、その中で組織がホストされます。異なる Realm には異なる API エンドポイントがあります (たとえば、データを送信するためのエンドポイントは、us1 realm では ingest.us1.signalfx.com 、eu0 レルムでは ingest.eu0.signalfx.com となります)。このrealm名は、Splunk UI のプロファイルページに表示されます。エンドポイントを指定する際にレルム名を含めない場合、Splunk は us0 レルムを指していると解釈します。 ↩︎
`,description:"",tags:null,title:"OpenTelemetry Collector を Kubernetes に導入する",uri:"/observability-workshop/v4.55/ja/imt/gdi/index.html"},{content:` Online Boutiqueのアドレスを探します Online Boutiqueのウェブショップで買い物しトラフィックを生成させます 1. RUMが有効化されたOnline BoutiqueのURL 前のセクションで説明したように、RUMホスト上で動作するOnline Boutiqueを使用します。 RUMのみのワークショップに参加される方は、使用するシステムは既に準備されていますので、RUMインスタンスのURLを受け取った後、セクション4 Online Boutiqueを使ってシステムに負荷を与える まで進むことができます。
2. RUM Access Token の入手 APMワークショップでサービスをインストールしました。これから、RUM機能もデプロイメントに追加していきます。
まず、RUM Authorization スコープを持つ RUM_ACCESS_TOKEN を取得する必要があります。ワークショップのRUM Access Tokenは、 settings メニューボタンをクリックし、 Access Tokens を選択することで見つけることができます。
講師が使用するように指示したRUMワークショップトークン（例： O11y-Workshop-RUM-TOKEN ）を展開し、 Show Token をクリックしてトークンを表示します。 Copy   ボタンをクリックし、クリップボードにコピーしてください。 Default トークンは使用しないでください。トークンのAuthorization ScopeがRUMであることを確認してください。
自分のトークンを作らないでください このワークショップのために、皆さんが行う演習に適した設定をしたRUM Tokenを作成ししています。
進行中のシェルスクリプトで環境変数 RUM_TOKEN を作成し、デプロイメントをパーソナライズします。
Export Variables export RUM_TOKEN=\u003creplace_with_O11y-Workshop-RUM-TOKEN\u003e 3. RUMを組み込んだOnline Boutiqueのデプロイ EC2インスタンスのkubernetes（K3s）にOnline Boutiqueのアプリケーションをデプロイするには、元のデプロイメントを削除し、RUM用のapm configスクリプトを実行し、RUMのデプロイメントを適用します。
Deploy Online Boutique with RUM Partial Deployment Output cd ~/workshop/apm kubectl delete -f deployment.yaml ./apm-config.sh -r kubectl apply -f deployment.yaml …… Adding RUM_TOKEN to deployment deployment.apps/recommendationservice created service/recommendationservice created deployment.apps/productcatalogservice created service/productcatalogservice created deployment.apps/cartservice created service/cartservice created deployment.apps/adservice created service/adservice created deployment.apps/paymentservice created service/paymentservice created deployment.apps/loadgenerator created service/loadgenerator created deployment.apps/shippingservice created service/shippingservice created deployment.apps/currencyservice created service/currencyservice created deployment.apps/redis-cart created service/redis-cart created deployment.apps/checkoutservice created service/checkoutservice created deployment.apps/frontend created service/frontend created service/frontend-external created deployment.apps/emailservice created service/emailservice created deployment.apps/rum-loadgen-deployment created
変数未セットに関するメッセージが表示された場合 kubectl delete -f deployment.yaml コマンドを実行しAPM環境のデプロイ削除します。 次にガイド、メッセージに表示されていた変数をexportし上記のデプロイスクリプトを再実行します。
4. Online Boutiqueを使ってシステムに負荷を与える 皆さんと一緒にOnline Boutiqueに接続し買い物をシミュレートする合成ユーザーもいます。これにより、複数の場所からのトラフィックが発生し、よりリアルなデータが得られます。
ワークショップ講師からURLを受け取っているはずです。 新しいWebブラウザを立ち上げ http://{==RUM-HOST-EC2-IP==}:81/ にアクセスするとRUMが有効化されたOnline Boutiqueが表示されます。
5. トラフィックを発生させる この演習の目的は、RUMが有効化されたOnline Boutiqueを閲覧し、さまざまな商品と数量の組み合わせで購入することです。 さらに別のブラウザやスマートフォンからアクセスすることもできます。
これにより複数のセッションが作成され、調査することができます。じっくりと吟味して、いろいろな商品を購入しカートに入れてください。
Home Barista Kitかっこよくないですか？… ショッピングを楽しんでください！
`,description:"",tags:null,title:"2. Online BoutiqueでのRUMの利用例",uri:"/observability-workshop/v4.55/ja/rum/2-showcase/index.html"},{content:`サービスマップ サービスマップの paymentservice をクリックし、paymentservice の下にあるbreakdownのドロップダウンフィルタから version を選択します。これにより、カスタムスパンタグの version でサービスマップがフィルタリングされます。
これで、サービスマップが以下のスクリーンショットのように更新され、paymentservice の異なるバージョンが表示されていることがわかります。
`,description:"",tags:null,title:"2.1 サービスマップ",uri:"/observability-workshop/v4.55/ja/apm/using-splunk-apm/service_map/index.html"},{content:`1. チャートの保存 チャートの保存するために、名前と説明をつけましょう。チャートの名前 Copy of Latency Histogram をクリックして、名前を “現在のレイテンシー” に変更します。
説明を変更するには、 Spread of latency values across time. をクリックし、 リアルタイムでのレイテンシー値 に変更します。
Save As  ボタンをクリックします。チャートに名前が付いていることを確認します。前のステップで定義した 現在のレイテンシー という名前が使用されますが、必要に応じてここで編集することができます。
Ok  ボタンを押して続行します。
2. ダッシュボードの作成 Choose dashboard ダイアログでは、新しいダッシュボードを作成する必要があります。 New Dashboard   ボタンをクリックしてください。
これで、New Dashboard ダイアログが表示されます。ここでは、ダッシュボードの名前と説明を付け、Write Permissions で書き込み権限を設定します。
ダッシュボードの名前には、自分の名前を使って YOUR_NAME-Dashboard の形式で設定してください。
YOUR_NAME を自分の名前に置き換えてから、編集権限をEveryone can Read or Write からRestricted Read and Write access に変更してみてください。
ここには、自分のログイン情報が表示されます。つまり、このダッシュボードを編集できるのは自分だけということになります。もちろん、ダッシュボードやチャートを編集できる他のユーザーやチームを下のドロップボックスから追加することもできますが、今回は、Everyone can Read or Write に 再設定 して制限を解除し、 Save   ボタンを押して続行してください。
新しいダッシュボードが利用可能になり、選択されましたので、チャートを新しいダッシュボードに保存することができます。
ダッシュボードが選択されていることを確認して、 Ok  ボタンを押します。
すると、下図のようにダッシュボードが表示されます。左上に、YOUR_NAME-DASHBOARD がダッシュボードグループ YOUR_NAME-Dashboard の一部であることがわかります。このダッシュボードグループに他のダッシュボードを追加することができます。
3. チームページへの追加 チームに関連するダッシュボードは、チームページにリンクさせるのが一般的です。そこで、後で簡単にアクセスできるように、ダッシュボードをチームページに追加してみましょう。 ナビバーのアイコンを再びクリックします。 これでチームダッシュボードに遷移します。ここでは、チーム Example Team を例にしていますが、ワークショップのものは異なります。
+   を押し、 Add Dashboard Group ボタンを押して、チームページにダッシュボードを追加します。
すると、 Select a dashboard group to link to this team ダイアログが表示されます。 検索ボックスにご自身のお名前（上記で使用したお名前）を入力して、ダッシュボードを探します。ダッシュボードがハイライトされるように選択し、Ok ボタンをクリックしてダッシュボードを追加します。
ダッシュボードグループがチームページの一部として表示されます。ワークショップを進めていくと、さらに多くのダッシュボードがここに表示されていくはずです。
次のモジュールでは、ダッシュボードのリンクをクリックして、チャートをさらに追加していきます！
`,description:"",tags:null,title:"チャートを保存する",uri:"/observability-workshop/v4.55/ja/imt/dashboards/savingcharts/index.html"},{content:` 個別のアクセストークンを作成し、制限を設けることで利用を制限する方法を紹介します 1. アクセストークン ホスト、コンテナ、カスタムメトリクス、高解像度メトリクスの使用量をコントロールしたい場合は、複数のアクセストークンを作成し、組織内の異なる部分に割り当てることができます。
左下の » を開いて、General Settings 配下の Settings → Access Tokens を選択します。
Access Tokens インターフェースでは、生成されたアクセストークンのリストで概要が表示されます。すべての組織では、最初のセットアップ時に Default のトークンが生成され、その他のトークンを追加・削除できるようになっています。
各トークンは一意であり、消費できるホスト、コンテナ、カスタムメトリクス、高解像度メトリクスの量に制限を設けることができます。
Usage Status 欄は、トークンが割り当てられた制限値を上回っているか下回っているかを素早く表示します。
2. 新しいトークンの作成 New Token   ボタンをクリックして、新しいトークンを作成しましょう。Name Your Access Token ダイアログが表示されます。
ここでは、Ingest Token と API Token の両方のチェックボックスにチェックを入れてください。
OK   を押すと、Access Token のUIに戻ります。ここでは、既存のトークンの中に、あなたの新しいトークンが表示されているはずです。
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
受信者を指定するには、 Add Recipient   をクリックして、使用する受信者または通知方法を選択します（受信者の指定は任意ですが、強くお勧めします）。
トークンアラートの重要度は常に「Critical」です。
Update   をクリックすると、アクセストークンの制限とアラートの設定が保存されます。
Note: トークンの上限を超えると、何が起こるのか トークンが使用カテゴリの上限に達したとき、または上限を超えたとき、その使用カテゴリの新しいメトリクスはObservability Cloudに保存されず、処理されません。これにより、チームが無制限にデータを送信することによる予期せぬコストが発生しないようになります。
Note: 高度なアラート通知 90%に達する前にアラートを取得したい場合は、必要な値を使用して追加のディテクターを作成できます。これらのディテクターは、特定のアクセストークンを消費しているチームをターゲットにすることができ、管理者が関与する必要がある前に行動を起こすことができます。
これらの新しいアクセストークンを様々なチームに配布し、Observability Cloudに送信できる情報やデータの量をコントロールできるようになります。
これにより、Observability Cloudの使用量を調整することができ、過剰な使用を防ぐことができます。
おめでとうございます！ これで、管理機能のモジュールは終わりです！
`,description:"",tags:null,title:"使用量を管理する",uri:"/observability-workshop/v4.55/ja/imt/servicebureau/tokens/index.html"},{content:`Splunk APM は、クラウドネイティブなマイクロサービスベースのアプリケーション向けの NoSample™ で 完全忠実なアプリケーションパフォーマンスモニタリングおよびトラブルシューティングソリューションです。
サンプリングされた部分的な情報ではなく、すべてのトレースを収集することで、異常が検出されないことはありません。ユーザーがエラーを経験しても、通常より長いレイテンシーを経験しても、数秒以内にそれを知り、対処することができます。ときに、悪い動作がエラーとして扱われないこともあります。開発者が新しいアプリケーションを作成する際には、そのカナリアリリースが期待通りの結果をもたらすかどうかを知る必要があります。すべてのトレースデータを収集して、初めて、クラウドネイティブアプリケーションが想定通り動作していることを確信できるようになります。
インフラとアプリケーションのパフォーマンスは相互に依存しています。全体像を把握するために、Splunk APM はクラウドのインフラとその上で動作するマイクロサービスをシームレスに相関付けます。メモリリーク、ノイズの多い隣のコンテナ、その他のインフラ関連の問題が原因でアプリケーションが動作した場合、Splunk がすぐに知らせてくれます。さらに、Splunk のログやイベントにインコンテキストでアクセスすることで、より詳細なトラブルシューティングや根本原因の分析が可能になります。
1. Online BoutiqueのデプロイOnline BoutiqueアプリケーションをKubernetes（K3s）にデプロイし、Locustを使って人工的なトラフィックを発生させます。
2. トレースとスパンSplunk APMの概要と使用方法
`,description:"Splunk APM は、クラウドネイティブ、マイクロサービスベースのアプリケーションのための NoSample™ Full-fidelity アプリケーションパフォーマンス監視およびトラブルシューティングソリューションです。",tags:null,title:"Splunk APM",uri:"/observability-workshop/v4.55/ja/apm/index.html"},{content:` 15分 APM の概要 - RED メトリクス サービスマップを利用する タグスポットライトの紹介 トレースの例 インフラとのリンク トレースとスパンについて トレースは、同じトレースIDを共有するスパンの集合体であり、アプリケーションとその構成サービスが処理する固有のトランザクションを表します。
各スパンには、そのスパンでキャプチャされた操作を表す名前と、その操作がどのサービス内で行われたかを表すサービス名があります。
さらにスパンは、その親として別のスパンを参照することができ、そのトランザクションを処理するために実行されたトレースでキャプチャされた処理の関係を定義します。
各スパンには、キャプチャされたメソッド、オペレーション、コードブロックに関する以下のような多くの情報が含まれています。例えば:
処理名 処理の開始時間（マイクロ秒単位の精度） 処理の実行時間（マイクロ秒単位の精度） 処理が行われたサービスの論理名 処理が行われたサービスインスタンスのIPアドレス `,description:"Splunk APMの概要と使用方法",tags:null,title:"2. トレースとスパン",uri:"/observability-workshop/v4.55/ja/apm/using-splunk-apm/index.html"},{content:` NGINX ReplicaSet を K3s クラスタにデプロイし、NGINX デプロイメントのディスカバリーを確認します。 負荷テストを実行してメトリクスを作成し、Splunk Observability Cloudにストリーミングすることを確認します！ 1. NGINX の起動 Splunk UI で WORKLOADS タブを選択して、実行中の Pod の数を確認します。これにより、クラスタ上のワークロードの概要がわかるはずです。
デフォルトの Kubernetes Pod のうち、ノードごとに実行されている単一のエージェントコンテナに注目してください。この1つのコンテナが、このノードにデプロイされているすべての Pod とサービスを監視します！
次に、MAP タブを選択してデフォルトのクラスタノードビューに戻し、再度クラスタを選択します。
Multipass または AWS/EC2 のシェルセッションで、nginx ディレクトリに移動します。
Change Directory cd ~/workshop/k3s/nginx 2. NGINXのデプロイメント作成 NGINX の ConfigMap1 を nginx.conf ファイルを使って作成します。
Kubectl Configmap Create Kubectl Create Configmap Output kubectl create configmap nginxconfig --from-file=nginx.conf configmap/nginxconfig created
続いて、デプロイメントを作成します。
Kubectl Create Deployment Kubectl Create Deployment Output kubectl create -f nginx-deployment.yaml deployment.apps/nginx created service/nginx created
次に、NGINXに対する負荷テストを作成するため、 Locust2 をデプロイします。
Kubectl Create Deployment Kubectl Create Deployment Output kubectl create -f locust-deployment.yaml deployment.apps/nginx-loadgenerator created service/nginx-loadgenerator created デプロイメントが成功し、Locust と NGINX Pod が動作していることを確認しましょう。
Splunk UI を開いていれば、新しい Pod が起動し、コンテナがデプロイされているのがわかるはずです。
Pod が実行状態に移行するまでには 20 秒程度しかかかりません。Splunk UIでは、以下のようなクラスタが表示されます。
もう一度 WORKLOADS タブを選択すると、新しい ReplicaSet と NGINX 用のデプロイメントが追加されていることがわかります。
これをシェルでも検証してみましょう。
Kubectl Get Pods Kubectl Get Pods Output kubectl get pods NAME READY STATUS RESTARTS AGE splunk-otel-collector-k8s-cluster-receiver-77784c659c-ttmpk 1/1 Running 0 9m19s splunk-otel-collector-agent-249rd 1/1 Running 0 9m19s svclb-nginx-vtnzg 1/1 Running 0 5m57s nginx-7b95fb6b6b-7sb9x 1/1 Running 0 5m57s nginx-7b95fb6b6b-lnzsq 1/1 Running 0 5m57s nginx-7b95fb6b6b-hlx27 1/1 Running 0 5m57s nginx-7b95fb6b6b-zwns9 1/1 Running 0 5m57s svclb-nginx-loadgenerator-nscx4 1/1 Running 0 2m20s nginx-loadgenerator-755c8f7ff6-x957q 1/1 Running 0 2m20s
3. Locust の負荷テストの実行 Locust はオープンソースの負荷テストツールで、EC2 インスタンスの IP アドレスの8080番ポートで Locust が利用できるようになりました。Webブラウザで新しいタブを開き、http://{==EC2-IP==}:8080/にアクセスすると、Locust が動作しているのが確認できます。
Spawn rate を 2 に設定し、Start Swarming をクリックします。
これにより、アプリケーションに緩やかな連続した負荷がかかるようになります。
上記のスクリーンショットからわかるように、ほとんどのコールは失敗を報告しています。これはアプリケーションをまだデプロイしていないため予想されることですが、NGINXはアクセス試行を報告しており、これらのメトリックも見ることができます。
サイドメニューから Dashboards → Built-in Dashboard Groups → NGINX → NGINX Servers を選択して、UIにメトリクスが表示されていることを確認します。さらに Overrides フィルターを適用して、 k8s.cluster.name: に、ターミナルの echo $(hostname)-k3s-cluster で返されるクラスタの名前を見つけます。
ConfigMap とは、キーと値のペアで非機密データを保存するために使用される API オブジェクトです。Pod は、環境変数、コマンドライン引数、またはボリューム内の構成ファイルとして ConfigMap を利用することができます。ConfigMap を使用すると、環境固有の構成をコンテナイメージから切り離すことができるため、アプリケーションの移植が容易になります。 ↩︎
Locust とは？. ↩︎
`,description:"",tags:null,title:"K3s に NGINX をデプロイする",uri:"/observability-workshop/v4.55/ja/imt/gdi/nginx/index.html"},{content:`タグスポットライト 画面の右側にある Tag Spotlight をスクロールダウンし、ドロップダウンから Top Across All Indexed Tags を選択します。選択したら、下のスクリーンショットにあるように をクリックします。
タグスポットライトのページが表示されます。このページでは、アプリケーションの上位のタグと、それに対応するエラー率や秒間リクエスト数を確認できます。
version スパンタグでは、バージョン 350.10 のエラー率が100%であることがわかります。また、tenant.level スパンタグでは、3つのテナント（Gold、Silver、Bronze）すべてにエラーがあることがわかります。
タグスポットライトのページはインタラクティブに、目的のタグをクリックするだけでフィルタとしてタグを追加することができます。tenant.level の下の gold をクリックして、フィルターとして追加します。これを行うと、ページには tenant.level が gold のデータのみが表示されます。
タグスポットライトは、データを分析して傾向を見極めるのに非常に便利です。Gold Tenantでは、リクエストの総数のうち55件がエラーであることがわかります。（この数字はワークショップの実施時刻により異なります）
これをバージョンタグと関連付けると、バージョン 350.10 が55件、バージョン 350.9 が17件のリクエストに対応していることがわかります。つまり、バージョン 350.10 を経由したリクエストは、すべてエラー状態になったということになります。
paymentservice のバージョン 350.10 からのすべてのリクエストがエラーになるというこの理論をさらに検証するために、タグセレクタを使用して、フィルタを別のテナントに変更することができます。フィルターを gold テナントから silver テナントに変更します。
ここで、silver テナントのエラーのあるリクエスト数を見て、バージョン番号と相関させることで、同様の分析を行うことができます。silver テナントのエラー数は、バージョン 350.10 のリクエスト数と一致していることに注目してください。
タグスポットライトでは、秒間リクエスト数やエラー率だけでなく、サービスごとのレイテンシーも見ることができます。これを行うには、レイテンシーボタンを選択し、silver テナントタグを削除することで、すべての paymentservice のレイテンシーを確認することができます。
右端の Clear All の下にある X ボタンを押して、サービスマップに戻りましょう。
`,description:"",tags:null,title:"2.2 Tag Spotlight",uri:"/observability-workshop/v4.55/ja/apm/using-splunk-apm/tag_spotlight/index.html"},{content:` 20分 ダッシュボードとチャートの紹介 チャートの編集と作成 フィルタリングと分析関数 数式の使用 ダッシュボードでのチャートの保存 SignalFlowの紹介 1. ダッシュボード ダッシュボードとは、チャートをグループ化し、メトリクスを視覚化したものです。適切に設計されたダッシュボードは、システムに関する有益で実用的な洞察を一目で提供します。ダッシュボードは複雑なものもあれば、見たいデータだけを掘り下げたいくつかのチャートだけのものもあります。
このモジュールでは、次のようなチャートとダッシュボードを作成し、それをチームページに接続します。
2. あなたのチームのページ 左のナビゲーションから を開きます。あなたはすでにチームに割り当てられているので、チームダッシュボードが表示されます。
ここでは、チーム Example Team を例に挙げています。実際のワークショップでは、別のチーム名かも知れません。
このページには、チームメンバーの総数、チームのアクティブなアラートの数、チームに割り当てられているすべてのダッシュボードが表示されます。現在、ダッシュボードは割り当てられていませんが、この後で、あなたが作成する新しいダッシュボードをチームページに追加していきます。
3. サンプルチャート 続けて、画面右上の All Dashboards をクリックします。事前に作成されたもの（プレビルドダッシュボード）も含め、利用可能なすべてのダッシュボードが表示されます。
すでにSplunk Agentを介してCloud APIインテグレーションや他のサービスからメトリクスを受信している場合は、これらのサービスに関連するダッシュボードが表示されます。
4. サンプルデータの確認 ダッシュボードの中に、 Sample Data というダッシュボードグループがあります。Sample Data ダッシュボードグループをクリックして展開し、Sample Charts ダッシュボードをクリックします。
Sample Charts ダッシュボードでは、ダッシュボードでチャートに適用できる様々なスタイル、色、フォーマットのサンプルを示すチャートが表示されます。
このダッシュボードグループのすべてのダッシュボード（PART 1、PART 2、PART 3、INTRO TO SPLUNK OBSERVABILITY CLOUD）に目を通してみてください。
`,description:"",tags:null,title:"ダッシュボードを利用する",uri:"/observability-workshop/v4.55/ja/imt/dashboards/index.html"},{content:` ブラウザでOnline BoutiqueのウェブページのオリジナルのHEADセクション（またはここにある例を使用）をチェックします ワークショップ Online Boutique の Webアドレスを検索します Online Boutiqueに加えられた変更を確認します 1. RUMなしのOnline Boutiqueのオリジナルコードを確認する APMセッションの一部でEC2インスタンスにOnline Boutiqueをインストールしていれば、ポート番号81でサイトにアクセスできます。
Online BoutiqueがインストールされたEC2インスタンスにアクセスできない場合は、講師からRUMがインストールされていないOnline BoutiqueのURLを教えてもらい、次のステップに進んでください。
2. RUM Access Tokenの入手 これから行うデプロイメントは、RUM ワークショップセクションの一部としても使用されます。Splunk UIからRUM Access Tokenを取得する必要があります。ワークショップのアクセストークンは、左下の » をクリックし メニューをクリックして、 Settings → Access Tokens を選択すると見つけることができます。
講師が使用するように指示したRUMワークショップトークン（例： O11y-Workshop-RUM-TOKEN ）を展開し、 Show Token をクリックしてトークンを公開します。 Copy   ボタンをクリックし、クリップボードにコピーしてください。 Default のトークンは使用しないでください。トークンのAuthorization ScopeがRUMであることを確認してください。
新規にトークンを作らないでください このワークショップのために、皆さんが行う演習に適した設定をしたRUM Tokenを作成しています。
EC2にSSHアクセスしているシェルスクリプトで環境変数 RUM_TOKEN を作成し、デプロイメントをパーソナライズします。
Export Variables export RUM_TOKEN=\u003creplace_with_O11y-Workshop-RUM-TOKEN\u003e 2. Online Boutiqueのデプロイ Online BoutiqueアプリケーションをK3sにデプロイするには、apm configスクリプトを実行し、デプロイを適用してください。
Deploy Online Boutique Deployment Output cd ~/workshop/apm ./apm-config.sh -r kubectl apply -f deployment.yaml deployment.apps/checkoutservice created service/checkoutservice created deployment.apps/redis-cart created service/redis-cart created deployment.apps/productcatalogservice created service/productcatalogservice created deployment.apps/loadgenerator created service/loadgenerator created deployment.apps/frontend created service/frontend created service/frontend-external created deployment.apps/paymentservice created service/paymentservice created deployment.apps/emailservice created service/emailservice created deployment.apps/adservice created service/adservice created deployment.apps/cartservice created service/cartservice created deployment.apps/recommendationservice created service/recommendationservice created deployment.apps/shippingservice created service/shippingservice created deployment.apps/currencyservice created service/currencyservice created
変数未セットに関するメッセージが表示された場合 kubectl delete -f deployment.yaml コマンドを実行しAPM環境のデプロイ削除します。 次にガイド、メッセージに表示されていた変数をexportし上記のデプロイスクリプトを再実行します。
ウェブブラウザーを起動し、Online Boutiqueにアクセスします。 (以前使用したもの、または新しくワークショップ講師が提供したもの）。RUMなしのOnline Boutiqueが起動していることが確認できます。
下記のお使いのブラウザの説明に従ってください。
1.1 Chrome, FireFox \u0026 Microsoft Edge ユーザー - ページのソースを確認 Chrome、Firefox、Microsoft Edgeでは、Online Boutiqueのサイト上で右クリックすると、 「ページのソースを表示」 のオプションが表示されます。
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
\u003cscript src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" type="text/javascript"\u003e\u003c/script\u003e \u003cscript\u003ewindow.SplunkRum \u0026\u0026 window.SplunkRum.init({beaconUrl: "https://rum-ingest.eu0.signalfx.com/v1/rum", rumAuth: "1wCqZVUWIP5XSdNjPoQRFg", app: "ksnq-rum-app", environment: "ksnq-rum-env"});\u003c/script\u003e \u003cscript\u003e const Provider = SplunkRum.provider; var tracer=Provider.getTracer('appModuleLoader'); \u003c/script\u003e 最初の行は、Splunk Open Telemetry Javascript ファイルをダウンロードする場所を指定しています。https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js (必要であれば、ローカルに読み込むこともできます) 2行目は、Beacon URLでトレースの送信先を定義しています。 {beaconUrl: "https://rum-ingest.eu0.signalfx.com/v1/rum" また、Access Tokenを追加しています。 rumAuth: "1wCqZVUWIP5XSdNjPoQRFg" (もちろんこれは例です。全てのアプリケーションに対して、複数のRUM Access Tokenを作成することができます。) * また、SPLUNK RUM UIで使用するために、アプリケーション名や環境などの識別タグをRUMトレースに追加するために使用されます。 app: "ksnq-rum-app", environment: "ksnq-rum-env"} Info この例ではアプリ名は ksnq-rum-app ですが、これはワークショップでは異なるでしょう。RUMセッションで使用するアプリ名と環境は講師に確認し、メモしておいてください。
上記の2行だけであなたのWebサイトでRUMを有効にすることができます。
(青色の)オプションのセクションでは、 var tracer=Provider.getTracer('appModuleLoader'); を使用して、すべてのページ変更に対してカスタムイベントを追加し、ウェブサイトのコンバージョンと使用状況をよりよく追跡できるようにします。
`,description:"",tags:null,title:"3. 自分のWebサイトでRUMを有効化する場合の例",uri:"/observability-workshop/v4.55/ja/rum/3-setup/index.html"},{content:`1 新しいチャートの作成 それでは、新しいチャートを作成し、ダッシュボードに保存してみましょう。
UIの右上にある + アイコンを選択し、ドロップダウンから Chart を選択します。 または、 + New Chart   ボタンをクリックすると、新しいチャートが作成されます。
これで、以下のようなチャートのテンプレートが表示されます。
プロットするメトリックを入力してみましょう。ここでは、demo.trans.latency というメトリックを使用します。
Plot Editor タブの Signal に demo.trans.latency を入力します。
すると、折れ線グラフが表示されるはずです。時間を15分に切り替えてみてください。
2. フィルタリングと分析 次に、Paris データセンターを選択して分析を行ってみましょう。そのためにはフィルタを使用します。
Plot Editor タブに戻り、 Add Filter   をクリックして、入力補助として選択肢が出てくるので、そこから demo_datacenter を選択し、Paris を選択します。
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
Enter Formula   をクリックして、A-B （AからBを引いた値）を入力し、C を除くすべてのシグナルを隠します（目アイコンの選択を解除します）。
これで、 A と B のすべてのメトリック値の差だけがプロットされているのがわかります。B のメトリック値が、その時点での A のメトリック値よりも何倍か大きな値を持っているためです。
次のモジュールで、チャートとディテクターを動かすための SignalFlow を見てみましょう。
`,description:"",tags:null,title:"3.3 フィルタと数式の使い方",uri:"/observability-workshop/v4.55/ja/imt/dashboards/filtering/index.html"},{content:`Splunk RUM は、業界唯一のエンド・ツー・エンドで完全忠実なリアルユーザーモニタリングソリューションです。パフォーマンスを最適化し、トラブルシューティングを迅速に行い、エンドユーザーエクスペリエンスを完全に可視化するために構築されています。
Splunk RUM は、ユーザーエクスペリエンスに影響を与える Web およびモバイルアプリケーションのパフォーマンス問題を特定することができます。Core Web Vitalによるページパフォーマンスのベンチマークと計測をサポートします。W3C タイミング、長時間実行されるタスクの特定、ページロードに影響を与える可能性のあるあらゆるものが含まれますが、これらに限定されるものではありません。
Splunk のエンドツーエンドモニタリング機能を使用すると、アプリケーションを構成する、サービス自身を始めとしてデータベースコール数などのインフラメトリクスやその他関与するすべてに対して、サービス間の遅延を表示することができます。
私たちの完全忠実なエンドツーエンドモニタリングソリューションは、お客様のSpanデータを100％取得します。サンプリングは行わず、フレームワークにとらわれず、Open Telemetryに標準化されています。
フロントエンドとバックエンドのアプリケーションのパフォーマンスは相互に依存していることがよくあります。バックエンドサービスとユーザーエクスペリエンスとの関連性を十分に理解し、可視化できることがますます重要になっています。 全体像を把握するために、Splunk RUM は当社のフロントエンドとバックエンドのマイクロサービス間のシームレスな相関関係を提供します。マイクロサービスやインフラストラクチャに関連する問題によって、ユーザーが Web ベースのアプリケーションで最適とは言えない状態を経験している場合、Splunk はこの問題を検出して警告することができます。
また、Splunk は、より深いトラブルシューティングと根本原因の分析を可能にするために、インコンテキストログとイベントを表示することができます。
`,description:"エンド・ツー・エンドの可視化により、Webブラウザやネイティブモバイルアプリからバックエンドサービスに至るまで、顧客に影響を与える問題をピンポイントで特定することができます。",tags:null,title:"Splunk RUM",uri:"/observability-workshop/v4.55/ja/rum/index.html"},{content:`サンプルトレース 右上にある「Services by Error Rate」グラフのピンク色の線上をクリックします。選択すると、サンプルトレースのリストが表示されます。Initiating Operation ofが frontend: POST /cart/checkout であるサンプルトレースの1つをクリックしてください。
スパンとともに、選択したトレースの全体が表示されます。エラーが発生したスパンは、その横に赤い！マークが表示されます。グレーのボックスにx6などの数字が表示されている場合は、それをクリックするとpaymentservice スパンを展開することができます。
赤い！マークが表示されたpaymentservice スパンの一つをクリックすると展開され、関連するメタデータやエラーの詳細が表示されます。このエラーが401エラーによるものであることがわかります。また、「テナント」や「バージョン」などの有用な情報も表示されています。
エラーの原因が 無効なリクエスト であることがわかりましたが、正確なリクエストが何であるかはわかりません。ページの下部に、ログへのコンテキストリンクが表示されます。このリンクをクリックすると、このスパンに関連付けられているログが表示されます。
下の画像と同様の Log Observer ダッシュボードが表示されます。
フィルタを使用して、エラーログのみを表示できます。右上にあるERRORをクリックしてから、Add to filterをクリックします。
severityがERRORであるログエントリに絞り込まれます。
いずれかのエントリを選択して詳細を表示します。これで、開発者が誤って本番環境にプッシュした 無効なAPIトークン の使用によってエラーがどのように発生したかを確認できます。
おめでとうございます。これで、このAPMワークショップは完了です。
`,description:"",tags:null,title:"2.3 サンプルトレース",uri:"/observability-workshop/v4.55/ja/apm/using-splunk-apm/example_trace/index.html"},{content:`1. はじめに ここでは、Observability Cloud の分析言語であり、Monitoring as Codeを実現するために利用する SignalFlow について見てみましょう。
Splunk Infrastructure Monitoring の中心となるのは、Python ライクな、計算を実行する SignalFlow 分析エンジンです。SignalFlow のプログラムは、ストリーミング入力を受け取り、リアルタイムで出力します。SignalFlow には、時系列メトリック（MTS）を入力として受け取り、計算を実行し、結果の MTS を出力する分析関数が組み込まれています。
過去の基準との比較する（例：前週との比較） 分布したパーセンタイルチャートを使った母集団の概要を表示する 変化率（またはサービスレベル目標など、比率で表されるその他の指標）が重要な閾値を超えたかどうか検出する 相関関係にあるディメンジョンの発見する（例：どのサービスの挙動がディスク容量不足の警告と最も相関関係にあるかの判断する） Infrastructure Monitoring は、Chart Builder ユーザーインターフェイスでこれらの計算を行い、使用する入力 MTS とそれらに適用する分析関数を指定できます。また、SignalFlow API を使って、SignalFlow のプログラムを直接実行することもできます。
SignalFlow には、時系列メトリックを入力とし、そのデータポイントに対して計算を行い、計算結果である時系列メトリックを出力する、分析関数の大規模なライブラリが組み込まれています。
Info SignalFlow の詳細については、 Analyze incoming data using SignalFlow を参照してください。
2. SignalFlow の表示 チャートビルダーで View SignalFlow をクリックします。
作業していたチャートを構成する SignalFlow のコードが表示されます。UI内で直接 SignalFlow を編集できます。ドキュメントには、SignalFlow の関数やメソッドの 全てのリスト が掲載されています。
また、SignalFlow をコピーして、API や Terraform とやり取りする際に使用して、Monitoring as Code を実現することもできます。
SignalFlow A = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).publish(label='A', enable=False) B = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).timeshift('1w').publish(label='B', enable=False) C = (A-B).publish(label='C') View Builder をクリックすると、Chart Builder の UI に戻ります。
この新しいチャートをダッシュボードに保存してみましょう！
`,description:"",tags:null,title:"3.4 SignalFlow",uri:"/observability-workshop/v4.55/ja/imt/dashboards/signalflow/index.html"},{content:` 10 分 チャートからディテクターを作成する アラート条件を設定する プリフライトチェックを実行する ミューティングルールを設定する 1. はじめに Splunk Observability Cloud では、ディテクター（検出器）、イベント、アラート、通知を使用して、特定の条件が満たされたときに情報を提供することができます。たとえば、CPU使用率が95%に達したときや、同時ユーザー数が制限値に近づいてAWSインスタンスを追加で立ち上げなければならない可能性があるときに、Slack チャンネルや Ops チームのメールアドレスにメッセージを送信したいと考えるでしょう。
これらの条件は1つまたは複数のルールとして表現され、ルール内の条件が満たされたときにアラートが発生します。ディテクターに含まれる個々のルールは、重要度に応じてラベル付けされています。Info、Warning、Minor、Major、Criticalとなっています。
2. ディテクターの作成 Dashboards で、前のモジュールで作成した Custom Dashboard Group をクリックし、ダッシュボードの名前をクリックします。
このチャートから、新しいディテクターを作成していきます。Latency vs Load チャート上のベルのアイコンをクリックし、 New Detector From Chart をクリックします。
Detector Name の横にあるテキストフィールドで、提案されたディテクター名の最初に、あなたのイニシャル を追加してください。
ディテクターの名前を決める 提案されたディテクター名の前に自分のイニシャルを追加することをお忘れなく。
次のような名前にしてください: XY’s Latency Chart Detector
Create Alert Rule   をクリックします。
Detector ウィンドウの Alert signal の中で、アラートするシグナルは Alert on 欄に青のベルが表示されています。このベルは、どのシグナルがアラートの生成に使用されているかを示しています。
Proceed to Alert Condition   をクリックします。
3. アラート条件の設定 Alert condition で、Static Threshold をクリックし、 Proceed to Alert Settings   をクリックしてください。
Alert Settings で、 Threshold フィールドに値 290 を入力します。同じウィンドウで、右上の Time を過去1日（-1d）に変更します。
4. プリフライトチェックの警告 5秒後にプリフライトチェックが行われます。Estimated alert count に、アラート回数の目安が表示されます。現在のアラート設定では、1日に受信するアラート量は 3 となります。
プリフライトチェックについて アラート条件を設定すると、UIは現在の設定に基づいて、右上に設定された時間枠（ここでは過去1日）の中で、どのくらいのアラートが発生するかを予測します。
すぐに、プラットフォームは現在の設定でシグナルの分析を開始し、「プリフライトチェック」と呼ばれる作業を行います。これにより、プラットフォーム内の過去のデータを使用してアラート条件をテストし、設定が妥当であり、誤って大量のアラートを発生させないようにすることができます。Splunk Observability Cloud を使用してのみ利用できるシンプルかつ非常に強力な方法で、アラートの設定から推測作業を取り除くことができます。
ディテクターのプレビューについての詳細は、こちらのリンクをご覧ください。 Preview detector alerts
Proceed to Alert Message   をクリックし、次に進みます。
5. アラートメッセージ Alert message の Severity で Major を選択します。
Proceed to Alert Recipients   をクリックします。
Add Recipient（受信者の追加）をクリックし、最初の選択肢として表示されているメールアドレスをクリックします。
通知サービス これは、そのメールアドレスを入力したときと同じです。または、E-mail… をクリックして別のメールアドレスを入力することもできます。
これは、予め用意されている多くの Notification Services の一例です。全てを確認するには、トップメニューの Integrations タブに移動し、Notification Services を参照してください。
6. アラートの有効化 Proceed to Alert Activation   をクリックします。
Activivate… で Activate Alert Rule   をクリックします。
アラートをより早く取得したい場合は、Alert Settings をクリックして、値を 290 から 280 に下げてみてください。
Time を -1h に変更すると、過去1時間のメトリクスに基づいて、選択した閾値でどれだけのアラートを取得できるかを確認できます。
ナビバーにある ボタンをクリックして、その後 Detectors をクリックすると、ディテクターの一覧が表示されます。あなたのイニシャルでフィルタして、作成したディテクターを確認しましょう。表示されない場合は、ブラウザをリロードしてみてください。
おめでとうございます！ 最初のディテクターが作成され、有効化されました。
`,description:"",tags:null,title:"ディテクターを利用する",uri:"/observability-workshop/v4.55/ja/imt/detectors/index.html"},{content:` RUMランディングページにアクセスし、アプリケーションサマリーダッシュボード（モバイルおよびウェブベース）でRUM対応アプリケーションすべてのパフォーマンスの概要を確認します。 1. RUMランディングページにアクセス Splunk IM/APM/RUM ウェブサイトにログインします。左側のメニューバーから RUM を選択します。 RUMのランディングページが表示されます。
このページの目的は、アプリケーションの健全性、パフォーマンス、潜在的なエラーを1つのページで明確に示し、Webページ/アプリケーションから収集したユーザーセッションに関する情報をより深く掘り下げることができるようにすることです。アクティブなRUMアプリケーションごとにペインが表示されます。(以下のビューは、デフォルトの拡張ビューです。）
複数のアプリケーションがある場合（RUMワークショップの参加者全員が自分のec2インスタンスを使用する場合）、以下のようにペインを折りたたむことで自動的にペインビューが縮小される場合があります。
アプリケーション名の前にある左側の赤い矢印で強調されている または アイコン(アプリケーションの種類が モバイル か ブラウザー かによる）をクリックすると、RUM Application Summryビューをフルダッシュボードに展開することが可能です。
まず、ワークショップに使用する適切なアプリケーションを見つけます。
単独のRUMワークショップに参加する場合、ワークショップ講師が使用するアプリケーションの名前を教えてくれます。複合ワークショップの場合、IMとAPMで使用した命名規則に従い、上のスクリーンショットの一番最後に表示されているように、 jmcj-rum-app のようにユニークIDとしてEC2ノードの名前に従います。
2. RUM Application Summary ダッシュボード のヘッダーセクションを設定する RUM Application Summary ダッシュボードは5つの主要なセクションで構成されています。一つ目は選択ヘッダーで、多くのオプションを設定/フィルタリングすることができます。
表示対象時間のための タイム・ウィンドウ ドロップダウン（デフォルトでは過去15分間） Environment1 を選択するためのドロップダウン。これにより、その環境に属するアプリケーションのサブセットのみにフォーカスすることができます。 監視対象のさまざまな Apps を含むドロップダウンリスト。ワークショップ講師によって提供されたものを使用するか、あなた自身のものを選択することができます。これにより、1つのアプリケーションにフォーカスすることができます。 Source 、 Browser 、 Mobile アプリケーションを選択するためのドロップダウン。ワークショップの場合は、 All を選択したままにしてください。 ヘッダーの右側にあるハンバーガーメニューで、Splunk RUM アプリケーションのいくつかの設定を行うことができます(これについては、後のセクションで説明します)。 次のセクションでは「Application Summary」画面をより深く掘り下げて説明します。
デプロイメント環境（Environment）は、システムまたはアプリケーションの個別のデプロイメントであり、同じアプリケーションの他のデプロイメントの設定と重複しないように設定を行うことができます。開発、ステージング、本番など、開発プロセスの段階ごとに別々のデプロイメント環境を使用することがよくあります。 一般的なアプリケーションのデプロイメントパターンとして、互いに直接影響し合わない複数の異なるアプリケーション環境を持ち、それらをすべて Splunk APM または RUM で監視することがあります。たとえば、品質保証 (QA) 環境と本番環境、または異なるデータセンター、地域、クラウドプロバイダーでの複数の異なるデプロイメントが挙げられます。 ↩︎
`,description:"",tags:null,title:"4. RUMランディングページの確認",uri:"/observability-workshop/v4.55/ja/rum/4-rum-landing/index.html"},{content:`Splunk Synthetic Monitoring は、完全なオブザーバビリティスイートである Splunk Observability Cloud の一部として、アップタイムと Webパフォーマンスの最適化のための最も包括的で詳細な機能を提供します。
API、サービスエンドポイント、エンドユーザーエクスペリエンスの監視を簡単に設定できます。Splunk Synthetic Monitoringを使用すれば、基本的な稼働時間やパフォーマンスの監視にとどまらず、問題の発見と修正、Web パフォーマンスの最適化、顧客が最高のユーザーエクスペリエンスを得られるようにすることに注力することができます。
Splunk Synthetic Monitoringによって得られるもの:
重要なユーザーフロー、ビジネストランザクション、APIエンドポイントにおける問題を迅速に検出し解決 インテリジェンスなWeb最適化エンジンで、Webパフォーマンスの問題が顧客に影響を与えることを防止 すべてのページリソースとサードパーティの依存関係のパフォーマンスを向上 `,description:"ユーザーフロー、ビジネストランザクション、APIにおけるパフォーマンスの問題を積極的に発見、修正し、より良いデジタル体験を提供します。",tags:null,title:"Splunk Synthetics",uri:"/observability-workshop/v4.55/ja/synthetics/index.html"},{content:`1. 既存のダッシュボードに保存する 右上に YOUR_NAME-Dashboard と表示されていることを確認しましょう
これは、あなたのチャートがこのダッシュボードに保存されることを意味します。
チャートの名前を Latency History とし、必要に応じてチャートの説明を追加します。
Save And Close   をクリックします。これで、ダッシュボードに戻ると2つのチャートが表示されているはずです！
では、先ほどのチャートを元に、もう一つのチャートをさくっと追加してみましょう。
2. チャートのコピー＆ペースト ダッシュボードの Latency History チャート上の3つのドット ... をクリックし、 Copy をクリックします。
ページ左上の + の横に赤い円と白い1が表示されていれば、チャートがコピーされているということになります。
ページ上部の をクリックし、メニューの Paste Charts をクリックしてください (また、右側に 1 が見える赤い点があるはずです)。
これにより、先程のチャートのコピーがダッシュボードに配置されます。
3. 貼り付けたチャートを編集する ダッシュボードの Latency History チャートの3つの点 ... をクリックし、Open をクリックします（または、チャートの名前（ここでは Latency History）をクリックすることもできます）。
すると、再び編集できる環境になります。
まず、チャートの右上にあるタイムボックスで、チャートの時間を -1h（1時間前から現在まで） に設定します。そして、シグナル「A」の前にある目のアイコンをクリックして再び表示させ、「C」 を非表示にし、Latency history の名前を Latency vs Load に変更します。
Add Metric Or Event   ボタンをクリックします。これにより、新しいシグナルのボックスが表示されます。シグナル D に demo.trans.count と入力・選択します。
これにより、チャートに新しいシグナル D が追加され、アクティブなリクエストの数が表示されます。demo_datacenter:Paris のフィルタを追加してから、 Configure Plot ボタンをクリックしロールアップを Auto (Delta) から Rate/sec に変更します。名前を demo.trans.count から Latency vs Load に変更します。
最後に Save And Close   ボタンを押します。これでダッシュボードに戻り、3つの異なるチャートが表示されます。
次のモジュールでは、「説明」のメモを追加して、チャートを並べてみましょう！
`,description:"",tags:null,title:"ダッシュボードにチャートを追加する",uri:"/observability-workshop/v4.55/ja/imt/dashboards/adding-charts/index.html"},{content:` 10分 Terraform1 を使用して Observability Cloud のダッシュボードとディテクターを管理します。 Terraform のSplunk Provider2 を初期化します Terraformを実行して、Splunk Terraform Provider を使用してコードからディテクターとダッシュボードを作成します。 Terraformでディテクターやダッシュボードを削除する方法を確認します。 1. 初期設定 Monitoring as Codeは、infrastructure as Codeと同じアプローチを採用しています。アプリケーション、サーバー、その他のインフラコンポーネントと同じようにモニタリングを管理できます。
Monitoring as Codeでは、可視化したり、何を監視するか定義したり、いつアラートを出すかなどを管理します。つまり、監視設定、プロセス、ルールをバージョン管理、共有、再利用することができます。
Splunk Terraform Providerの完全なドキュメントはこちらにあります。
AWS/EC2 インスタンスにログインして、o11y-cloud-jumpstart ディレクトリに移動します
Change directory cd observability-content-contrib/integration-examples/terraform-jumpstart 必要な環境変数は、Helmによるインストール ですでに設定されているはずです。そうでない場合は、以下の Terraform のステップで使用するために、以下の環境変数を作成してください。
Export ACCESS TOKEN export ACCESS_TOKEN="\u003creplace_with_O11y-Workshop-ACCESS_TOKEN\u003e" Export REALM export REALM="\u003creplace_with_REALM\u003e" Terraform を初期化し、Splunk Terraform Provider を最新版にアップグレードします。
Note: SignalFx Terraform Provider のアップグレード Splunk Terraform Provider の新バージョンがリリースされるたびに、以下のコマンドを実行する必要があります。リリース情報は GitHub で確認できます。
Initialise Terraform Initialise Output terraform init -upgrade Upgrading modules... - aws in modules/aws - azure in modules/azure - docker in modules/docker - gcp in modules/gcp - host in modules/host - kafka in modules/kafka - kubernetes in modules/kubernetes - parent_child_dashboard in modules/dashboards/parent - pivotal in modules/pivotal - rum_and_synthetics_dashboard in modules/dashboards/rum_and_synthetics - usage_dashboard in modules/dashboards/usage Initializing the backend... Initializing provider plugins... - Finding latest version of splunk-terraform/signalfx... - Installing splunk-terraform/signalfx v6.20.0... - Installed splunk-terraform/signalfx v6.20.0 (self-signed, key ID CE97B6074989F138) Partner and community providers are signed by their developers. If you'd like to know more about provider signing, you can read about it here: https://www.terraform.io/docs/cli/plugins/signing.html Terraform has created a lock file .terraform.lock.hcl to record the provider selections it made above. Include this file in your version control repository so that Terraform can guarantee to make the same selections by default when you run "terraform init" in the future. Terraform has been successfully initialized! You may now begin working with Terraform. Try running "terraform plan" to see any changes that are required for your infrastructure. All Terraform commands should now work. If you ever set or change modules or backend configuration for Terraform, rerun this command to reinitialize your working directory. If you forget, other commands will detect it and remind you to do so if necessary. 2. プランの作成 terraform plan コマンドで、実行計画を作成します。デフォルトでは、プランの作成は以下のように構成されています。
既に存在するリモートオブジェクトの現在の状態を読み込み、Terraform の状態が最新であることを確認します 現在の設定を以前の状態と比較し、相違点を抽出します 適用された場合にリモートオブジェクトと設定とを一致させるための、一連の変更アクションを提案します plan コマンドだけでは、提案された変更を実際に実行はされなません。変更を適用する前に、以下のコマンドを実行して、提案された変更が期待したものと一致するかどうかを確認しましょう。
Execution Plan Execution Plan Output terraform plan -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="o11y_prefix=[$(hostname)]" Plan: 146 to add, 0 to change, 0 to destroy. プランが正常に実行されれば、そのまま apply することができます。
3. プランの適用 terraform apply コマンドは、上記の Terraform プランで提案されたアクションを実行します。
この場合、新しい実行プランが自動的に作成され（terraform planを実行したときと同様です）、指示されたアクションを実行する前にAccess Token、Realm（プレフィックスのデフォルトはSplunk）の提供とプランの承認を求められます。
このワークショップでは、プレフィックスがユニークである必要があります。以下の terraform apply を実行してください。
Apply Plan Apply Plan Output terraform apply -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" -var="o11y_prefix=[$(hostname)]" Apply complete! Resources: 146 added, 0 changed, 0 destroyed.
適用が完了したら、 Alerts → Detectors でディテクターが作成されたことを確認してください。ディテクターのプレフィックスには、インスタンスのホスト名が入ります。プレフィックスの値を確認するには以下を実行してください。
Echo Hostname echo $(hostname) 新しいディテクターのリストが表示され、上から出力されたプレフィックスを検索することができます。
4. 苦労して作ったもの全てを壊す terraform destroy コマンドは、Terraform の設定で管理されているすべてのリモートオブジェクトを破壊する便利な方法です。
通常、本番環境では長期保存可能なオブジェクトを破棄することはありませんが、Terraformでは開発目的で一時的なインフラを管理するために使用されることがあり、その場合は作業が終わった後に terraform destroy を実行して、一時的なオブジェクトをすべてクリーンアップすることができます。
それでは、ここまでで適用したダッシュボードとディテクターを全て破壊しましょう！
Destroy Destroy Output terraform destroy -var="access_token=$ACCESS_TOKEN" -var="realm=$REALM" Destroy complete! Resources: 146 destroyed.
Alerts → Detectors に移動して、すべてのディテクターが削除されたことを確認してください。
Terraform は、インフラを安全かつ効率的に構築、変更、バージョン管理するためのツールです。Terraform は、既存の一般的なサービスプロバイダーだけでなく、様々なカスタムソリューションも管理できます。
Terraform の設定ファイルには、単一のアプリケーションまたはデータセンター全体を実行するために必要なコンポーネントをに記述します。Terraform はそれを受けて、望ましい状態に到達するために何をするかを記述した実行プランを生成し、記述されたインフラを構築するために実行します。設定が変更されても、Terraform は何が変更されたかを判断し、差分の実行プランを作成して適用することができます。
Terraform が管理できるインフラには、計算機インスタンス、ストレージ、ネットワークなどのローレベルのコンポーネントや、DNSエントリ、SaaS機能などのハイレベルのコンポーネントが含まれます。 ↩︎
プロバイダーは、APIのインタラクションを理解し、リソースを公開する責務があります。一般的にプロバイダーは、IaaS（Alibaba Cloud、AWS、GCP、Microsoft Azure、OpenStackなど）、PaaS（Herokuなど）、またはSaaSサービス（Splunk、Terraform Cloud、DNSimple、Cloudflareなど）があります。 ↩︎
`,description:"",tags:null,title:"Monitoring as Code",uri:"/observability-workshop/v4.55/ja/imt/monitoring-as-code/index.html"},{content:` ランディングページで利用できるUIとオプションに慣れる ページビュー/エラー、リクエスト/エラー、およびJavaScriptエラーを1つのビューで識別しする Web Vitalメトリクスと、ブラウザーアプリケーションに関連して発生したディテクターを確認する 1. Application Summary ダッシュボードの概要 1.1. ヘッダーバー 前のセクションで見たように、RUM Application Summary ダッシュボードは5つの主要セクションで構成されています。 最初のセクションは選択ヘッダーで、 ブラウザーアイコンまたはアプリケーション名の前の \u003e を使用してペインを折りたたむことができます。また、アプリケーション名(下の例では jmcj-rum-app )のリンクをクリックすると、Application Overview ページにアクセスできます。
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
`,description:"",tags:null,title:"5. ブラウザーアプリケーションの健全性を一目で確認",uri:"/observability-workshop/v4.55/ja/rum/5-browser-app-summary/index.html"},{content:`1. メモの追加 ダッシュボードには、ダッシュボードの利用者を支援するための短い「説明」ペインを配置することがよくあります。
ここでは、 New Text Note   ボタンをクリックして、ノートを追加してみましょう。
すると、ノートエディターが開きます。
ノートに単なるテキスト以外のものを追加できるように、Splunk ではこれらのノート/ペインで Markdown を使用できるようにしています。 Markdown は、ウェブページでよく使われるプレーンテキストを使ってフォーマットされたテキストを作成するための軽量なマークアップ言語です。
たとえば、以下のようなことができます (もちろん、それ以外にもいろいろあります)。
ヘッダー (様々なサイズで) 強調スタイル リストとテーブル リンク: 外部の Web ページ (ドキュメントなど) や他の Splunk IM ダッシュボードへの直接リンクできます 以下は、ノートで使用できる上記のMarkdownオプションの例です。
Sample Markdown text # h1 Big headings ###### h6 To small headings ##### Emphasis **This is bold text**, *This is italic text* , ~~Strikethrough~~ ##### Lists Unordered + Create a list by starting a line with \`+\`, \`-\`, or \`*\` - Sub-lists are made by indenting 2 spaces: - Marker character change forces new list start: * Ac tristique libero volutpat at + Facilisis in pretium nisl aliquet * Very easy! Ordered 1. Lorem ipsum dolor sit amet 2. Consectetur adipiscing elit 3. Integer molestie lorem at massa ##### Tables | Option | Description | | ------ | ----------- | | chart | path to data files to supply the data that will be passed into templates. | | engine | engine to be used for processing templates. Handlebars is the default. | | ext | extension to be used for dest files. | #### Links [link to webpage](https://www.splunk.com) [link to dashboard with title](https://app.eu0.signalfx.com/#/dashboard/EaJHrbPAEAA?groupId=EaJHgrsAIAA\u0026configId=EaJHsHzAEAA "Link to the Sample chart Dashboard!") 上記をコピーボタンでコピーして、Edit ボックスにペーストしてみてください。 プレビューで、どのように表示されるか確認できます。
2. チャートの保存 ノートチャートに名前を付けます。この例では、Example text chart としました。そして、 Save And Close   ボタンを押します。
これでダッシュボードに戻ると、メモが追加されました。
3. チャートの順序や大きさを変更 デフォルトのチャートの順番やサイズを変更したい場合は、ウィンドウをドラッグして、チャートを好きな場所に移動したり、サイズを変更したりすることができます。
チャートの 上側の枠 にマウスポインタを移動すると、マウスポインタがドラッグアイコンに変わります。これで、チャートを任意の場所にドラッグすることができます。
ここでは、 Latency vs Load チャートを Latency History と Example text chart の間に移動してください。
チャートのサイズを変更するには、側面または底面をドラッグします。
最後の練習として、ノートチャートの幅を他のチャートの3分の1程度にしてみましょう。チャートは自動的に、サポートしているサイズの1つにスナップします。他の3つのチャートの幅を、ダッシュボードの約3分の1にします。ノートを他のチャートの左側にドラッグして、他の23個のチャートに合わせてサイズを変更します。
最後に、時間を -1h に設定すると、以下のようなダッシュボードになります。
次は、ディテクターの登場です！
`,description:"",tags:null,title:"ノートの追加とダッシュボードのレイアウト",uri:"/observability-workshop/v4.55/ja/imt/dashboards/notes-and-layout/index.html"},{content:` 10分 組織におけるObservability Cloudの利用状況を把握する Subscription Usage（サブスクリプション使用量）インターフェースを使って、使用量を追跡する チームを作成する チームへの通知ルールを管理する 使用量をコントロールする 1. 利用状況を把握する 組織内のObservability Cloudのエンゲージメントを完全に把握するには、左下 » を開き、Settings → Organization Overview を選択すると、Observability Cloud の組織がどのように使用されているかを示す以下のダッシュボードが表示されます。
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
`,description:"",tags:null,title:"管理機能",uri:"/observability-workshop/v4.55/ja/imt/servicebureau/index.html"},{content:` RUM UIでRUMメトリクスとセッション情報を見る RUM \u0026 APM UIで相関するAPMトレースを見る 1. RUM Overview Pages RUM Application Summaryダッシュボードの右側のトリプルドット メニューから Open Application Overview を選択するか、アプリケーション名のリンク（以下の例では jmcj-rum-app ）をクリックして Application Overviewページを開き、詳細情報を確認することができます。
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
const Provider = SplunkRum.provider; var tracer=Provider.getTracer('appModuleLoader'); これらの行は、すべての新しいページに対して自動的にカスタムイベントを作成します。また、フレームワークや作成したイベントの一部ではないカスタムコードにこれらを追加することで、アプリケーションのフローをより良く理解することができます。 Custom Event Requests 、 Custom Event Error Rates 、 Custom Event Latency をサポートしています。
`,description:"",tags:null,title:"6. RUMメトリクスの分析",uri:"/observability-workshop/v4.55/ja/rum/6-analyzing-metrics/index.html"},{content:` より深く分析のために様々なエンドポイントのメトリクスビューを調査したりTag spotlightに送信されたTagを使用します。 1. CartエンドポイントのURLを探す RUMの概要ページから、Cart エンドポイントのURLを選択し、このエンドポイントで利用可能な情報をさらに深く掘り下げてみてください。
青色のURLをクリックすると、 Tag Spotlight の概要に遷移します。
ここでは、RUM トレースの一部として Splunk RUM に送信されたすべてのタグが表示されます。表示されるタグは、あなたが選択した概要に関連するものです。これらはトレースが送信されたときに自動的に作成された一般的なタグと、ウェブサイトの設定の一部でトレースに追加した追加タグです。
追加タグ 既に2つの追加タグを送信しています。それは皆さんのウェブサイトに追加された Beacon url に定義されている app: “[nodename]-rum-app”, environment: “[nodename]-rum-env” です（詳しくは後で確認します）。同様の方法で、タグを追加することができます。
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
`,description:"",tags:null,title:"7. Tag Spotlightの使用",uri:"/observability-workshop/v4.55/ja/rum/7-tag-spotlight/index.html"},{content:` RUM UIでRUM Sessionの情報を調査する ユーザーインタラクションのSpanでJavascriptのエラーを特定する 1. cart URLを再び選択 タイムセレクタで時間帯を選択した後、以下のように Url Nameビューから cart URLを再選択する必要があります。
上の例では http://34.246.124.162:81/cart を選択しました。
2. Sessionsにドリルダウン Tag Spotlightで情報を分析し、トレースのサブセットをドリルダウンした後、エンドユーザーのブラウザーで実行された実際のセッションを表示することができます。
以下のように Example Sessions というリンクをクリックすることで行います。
これにより、時間フィルタとタグプロファイルで選択したサブセットの両方に一致するセッションのリストが表示されます。
セッションIDをクリックします。最も長い時間（700 ミリ秒以上が望ましい）のものを選択するとよいでしょう。
セッションを選択すると、セッションの詳細ページが表示されます。セッションの一部である特定のアクションを選択しているため、セッション内のどこかのインタラクションにたどり着く可能性が高いです。 先ほど選択したURL http://34.246.124.162:81/cart が、セッションストリームでフォーカスしている場所であることがわかります。
ページを少し下にスクロールすると、以下のように操作の終わりが表示されます。
エンドユーザーには検出されなかったか、または表示されなかった可能性のあるいくつかのJavaScript Consoleエラーが発生していることがわかります。これらのエラーを詳しく調べるには、真ん中のエラー Cannot read properties of undefined (reading ‘Prcie’) をクリックしてください。
これによってページが展開され、このインタラクションのSpanの詳細が表示されます。このページには、問題を解決するために開発者に渡すことができる詳細な error.stack が含まれます。Online Boutiqueで商品を購入した際、最終的な合計金額が常に0ドルであることにお気づきでしょうか。
`,description:"",tags:null,title:"8. RUM Sessionの分析",uri:"/observability-workshop/v4.55/ja/rum/8-rum-sessions/index.html"},{content:` RUM UIでRUM Sessionの情報を続けます APM \u0026 Log Observer UI で相関する APM トレースとログを確認します 1. バックエンドサービスの問題を発見 をクリックして、Spanビューを閉じます。 次に下にスクロールし、 POST /cart/checkout の行を見つけます。
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
`,description:"",tags:null,title:"9. Splunk RUM と APM バックエンドサービスの相関",uri:"/observability-workshop/v4.55/ja/rum/9-apm-correlation/index.html"},{content:` RUMメトリクスを使用して、問題が発生した場合に警告するAlertsを設定する RUMメトリクスに基づくカスタムチャートを作成する SplunkのRUMは完全忠実なソリューションとして設計されているため、お客様のトレースを100％取得することができ、Webサイトの動作の変化を検知して警告することができます。また、カスタムチャートとダッシュボードを作成することで、Webサイトの挙動を正確に把握することができます。 これにより、ウェブサイト、バックエンド・サービス、基盤となるインフラストラクチャからのデータを組み合わせることができます。これにより、お客様のアプリケーションやソリューションを構成する完全なスタックを観察することができます。
RUMメトリクスのチャートまたはアラートの作成は、インフラストラクチャのメトリクスと同じ方法で行います。このセクションでは、簡単なチャート、ディテクター、およびアラートを作成します。
Splunk IM ワークショップを受講したことがある方は、このセクションをよくご存知でしょう。Splunk IM ワークショップの経験がない場合は、RUM ワークショップの終了後に ダッシュボード と ディテクター モジュールを参照して、機能をよりよく理解することをお勧めします。
`,description:"",tags:null,title:"10. RUMメトリクスに基づくカスタムチャートとアラート",uri:"/observability-workshop/v4.55/ja/rum/10-alerting/index.html"},{content:` Mobile RUMの簡単な紹介 Application Summary ダッシュボードで、モバイルアプリケーションの パフォーマンスの概要を確認できます 1. RUM Application Summary ダッシュボードにアクセス 左側のメニューバーから RUM を選択します。これで、RUM Application Summryページが表示されます。
このページの目的は、アプリケーションの健全性、パフォーマンス、潜在的なエラーを1つのペイン/ダッシュボードに表示し、Webサイトに対して実行されたユーザーセッションに関する情報を深く掘り下げることができるようにすることです。
アクティブな RUM アプリケーションごとにペインが表示されます。(以下のビューは、デフォルトの拡張ビューです。）
複数のアプリケーションを使用している場合、以下のようにペインが自動的に折りたたまれ、ペインビューが縮小されることがあります。
アプリケーション名の前にある左側の赤い矢印で強調されている または アイコン(アプリケーションの種類が モバイル か ブラウザー かによる）をクリックすると、RUM Application Summryビューをフルダッシュボードに展開することが可能です。
2. RUM Mobileの概要 Splunk RUM は Apple iPhone と Android Phone 向けの Native Mobile RUM をサポートしています。スマートフォンのネイティブアプリのエンドユーザーエクスペリエンスを確認するために使用することができます。
上の画面は、Splunk Mobile RUM が追跡できるさまざまなメトリクスやデータを表示するものです。例えば、以下のようなものです。
Custom events ：ブラウザーアプリケーションのものと同様です。 App Errors ：1分あたりの アプリエラー と クラッシュ 。 App Lifecycle Performance ：OSごとの コールドスタートアップ時間 、 ホットスタートアップ時間 。 Request/Response ：ブラウザーアプリケーションのものと同様です。 この時点では、スマートフォン上でネイティブアプリを実行するか、エミュレーションを実行する必要があるため、Mobile RUMについて深く掘り下げることはしません。必要に応じて、より詳細な情報をデモで提供することができます。
`,description:"",tags:null,title:"11. モバイルアプリケーション (紹介)",uri:"/observability-workshop/v4.55/ja/rum/11-mobile-app-summary/index.html"},{content:"",description:"",tags:null,title:"Categories",uri:"/observability-workshop/v4.55/ja/categories/index.html"},{content:"",description:"",tags:null,title:"Tags",uri:"/observability-workshop/v4.55/ja/tags/index.html"}]