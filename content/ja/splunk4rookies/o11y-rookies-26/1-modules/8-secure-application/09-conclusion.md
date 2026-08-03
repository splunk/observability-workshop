---
title: まとめ
linkTitle: 09-Conclusion
weight: 9
---

## ワークショップの振り返り

チームが「本番環境で何が起きているのか、最初にどこを確認すべきか？」と尋ねるとき、Observability は信頼性に関する問いに答えます。**Splunk Secure Application** は、**別のエージェントを追加したり、別の製品を使用したりすることなく**、同じストーリーをアプリケーションセキュリティに拡張します。

このワークショップでは、断片化されたアプリケーションセキュリティツールから、チームが本番環境を理解する方法にセキュリティが組み込まれた運用モデルへの移行方法について説明しました。以下の方法を学びました:-
    - **実行中の**アプリケーションの脆弱性と攻撃を発見する
    - 受動的な緊急対応から**プロアクティブな防御**に移行する
    - **すでに実行している**計装を使用して、継続的な検出、ランタイム攻撃シグナル、およびサービス・環境・ライブラリに相関付けられた検出結果を活用する

> *「その成果：セキュリティがアプリケーションを理解する方法の一部になります。実際にデプロイされているものを防御し、より安全に素早くリリースし、ノイズの追跡に費やす時間を減らすことができます。」*

### ワークショップモジュールのまとめ

| モジュール | 実践した機能 |
|--------|---------------------|
| **Runtime Vulnerability Inventory** | CVE、CVSS、ステータス、リスクスコアを含む組織全体の露出ビュー |
| **Maintaining Visibility** | Overview、Service Map、およびサービスごとの Application Security ワークスペース |
| **Prioritizing Known Threats** | 運用トリアージのための CVSS と Threat Risk Score の活用 |
| **Investigating Vulnerabilities** | 修復ガイダンス、影響範囲、サービスライブラリのコンテキスト |
| **Investigating Attacks** | エクスプロイトのフォレンジックとコードレベルのスタックトレース |
| **Eliminating Risk & Tech Debt** | ステータスのライフサイクルと組織全体のライブラリ衛生管理 |
| **Integrated Defenses** | SIEM 通知と検出から適用へのロードマップ |

{{% notice title="CONGRATULATIONS" style="info" %}}
Splunk Application Security for Observability (O11y4Rookies) を完了いただき、ありがとうございます。
{{% /notice %}}
