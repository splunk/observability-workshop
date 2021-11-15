# チーム - ラボの概要

* チームの管理
* チームの作成とメンバーの追加

---

## 1. チームの管理

Observability Cloudを使用する際に、ユーザーに関連するダッシュボードやアラートが表示されるようにするために、ほとんどの組織ではObservability Cloudのチーム機能を使用して、メンバーを1つまたは複数のチームに割り当てます。

これは、仕事に関連した役割と一致するのが理想的で、たとえば、DevOpsグループやプロダクトマネジメントグループのメンバーは、Observability Cloudの対応するチームに割り当てられます。

ユーザーがObservability Cloudにログインすると、どのチームダッシュボードをホームページにするかを選択することができ、通常は自分の主な役割に応じたページを選択します。

以下の例では、ユーザーは開発、運用、プロダクトマネジメントの各チームのメンバーであり、現在は運用チームのダッシュボードを表示しています。

このダッシュボードには、NGINX、Infra、K8s用の特定のダッシュボード・グループが割り当てられていますが、どのダッシュボード・グループもチーム・ダッシュボードにリンクすることができます。

左上のメニューを使って割り当てられたチーム間を素早く移動したり、右側の **ALL TEAMS** ドロップダウンを使って特定のチームのダッシュボードを選択したり、隣のリンクを使って **ALL Dashboards** に素早くアクセスしたりすることができます。

![Teams](../images/servicebureau/teams-homepage.png)

アラートを特定のチームにリンクすることで、チームは関心のあるアラートだけをモニターすることができます。上記の例では、現在1つのアクティブなクリティカルアラートがあります。

チームダッシュボードの説明文はカスタマイズ可能で、チーム固有のリソースへのリンクを含むことができます（Markdownを使用します）。

---

## 2. 新しいチームの作成

Splunk のチーム UI を使用するには、左上のハンバーガーアイコンをクリックし、 **Organizations Settings → Teams** を選択します。

**Team** を選択すると、現在のチームのリストが表示されます。

新しいチームを追加するには、**Create New Team**{: .label-button .sfx-ui-button-blue} ボタンをクリックします。これにより、**Create New Team** ダイアログが表示されます。

![Add Team](../images/servicebureau/create-new-team.png){: .shadow}

自分の名前を検索して、名前の横にある **Add** リンクを選択して、自分自身を追加します。その結果、以下のようなダイアログが表示されるはずです。

![Add Team complete](../images/servicebureau/add-to-team.png){: .shadow}

選択したユーザーを削除するには、**Remove** または **x** を押します。

自分のイニシャルでグループを作成し、自分がメンバーとして追加されていることを確認して、**Done**{: .label-button .sfx-ui-button-blue} をクリックします。

これでチームリストに戻り、自分のチームと他の人が作成したチームが表示されます。

!!! note
    自分がメンバーになっているチームには、グレーの **Member** アイコンが前に表示されています。

自分のチームにメンバーが割り当てられていない場合は、メンバー数の代わりに青い **Add Members** のリンクが表示されます。このリンクをクリックすると、**Edit Team** ダイアログが表示され、自分を追加することができます。

自分のチームの行末にある3つのドット **...** を押しても、同じダイアログが表示されます。

**...** メニューでは、チームの編集、参加、離脱、削除を行うことができます（離脱と参加は、あなたが現在メンバーであるかどうかによって異なります）。

---

## 3. 通知ルールの追加

チームごとに特定の通知ルールを設定することができます。**Notification Policy** タブをクリックすると、通知編集メニューが表示されます。

![Base notification menu](../images/servicebureau/notification-policy.png)

デフォルトでは、システムはチームの一般的な通知ルールを設定する機能を提供します。

!!! note
    **Email all team members** オプションは、アラートの種類に関わらず、このチームのすべてのメンバーにアラート情報のメールが送信されることを意味します。

### 3.1 受信者の追加

**Add Recipient**{: .label-button .sfx-ui-button-blue} をクリックすると、他の受信者を追加することができます。これらの受信者は Observability Cloud のユーザーである必要はありません。

**Configure separate notification tiers for different severity alerts** をクリックすると、各アラートレベルを個別に設定できます。

![Multiple Notifications](../images/servicebureau/single-policy.png)

上の画像のように、異なるアラートレベルに対して異なるアラートルールを設定することができます。

Critical と Major は [Splunk On-Call](https://www.splunk.com/en_us/observability/on-call.html){: target=_blank} インシデント管理ソリューションを使用しています。Minor のアラートはチームの Slack チャンネルに送信し、Warning と Info はメールで送信しています。

## 3.2 通知機能の統合

Observability Cloud では、アラート通知をメールで送信するだけでなく、以下のようなサービスにアラート通知を送信するように設定することができます。

![Notifications options](../images/servicebureau/integrations.png)

チームの事情に合わせて、通知ルールを作成してください。
