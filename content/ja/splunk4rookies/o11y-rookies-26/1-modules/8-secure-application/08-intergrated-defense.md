---
title: Integrated Defense
linkTitle: 08-Intergrated-Defense
weight: 8
---

## 統合がエンタープライズ防御のストーリーを完成させる理由

Observability 内で脆弱性や攻撃を検出することは、セキュリティジャーニーの一部にすぎません。SecOps チームもこの方程式の一部であり、エンタープライズレベルの防御規模から見ると、通常は SIEM ワークフローで作業しています。脆弱性や攻撃のイベントおよび検出結果がこれらのツールに届かない場合、セキュリティ管理にギャップが生じ、チケットの重複や古いエクスポートに戻ってしまうことがよくあります。

Splunk Secure Application は、Splunk Enterprise Security のような SIEM ソリューションに検出結果をストリーミングする**通知ルール**でこのループを閉じます。

---

## 7.4 SIEM 統合による SecOps への接続

通知統合は、脆弱性および攻撃イベントを選択した SIEM ソリューションに送信するように構成されており、SecOps チームにランタイムリスクをリアルタイムで可視化します。

1. **APM → Application Security → Notifications** に移動します。
2. 既存の通知ルールを確認します（デモテナントには事前にプロビジョニングされた Splunk ES 統合がある場合があります）。
3. **Create Notification Rule** をクリックして、構成フローを確認します

| ステップ | アクション |
|------|--------|
| **Trigger** | 脆弱性またはエクスプロイトイベントタイプを選択 |
| **Destination** | サポートされている統合を選択（例：Splunk ES HTTP Event Collector） |
| **Credentials** | Vault で管理されたシークレットを参照 |

![apm](./images/06-notification.png)

> *「ランタイムの検出結果から SOC の可視化までの単一パイプライン — SecOps はこれらのイベントを完全なコンテキスト付きで受信します。重複するワークフローはありません。」*

---

## 学んだこと

- 通知ルールが Observability ネイティブの検出結果を Splunk ES やその他の SOC ツールにどのようにフィードするか。
- 現在の利用可能状況を誇張せずに、攻撃ブロックのロードマップについて議論する方法。
- 最新の防御がランタイム検出と既存の SecOps ワークフローをどのように組み合わせるか。

---
