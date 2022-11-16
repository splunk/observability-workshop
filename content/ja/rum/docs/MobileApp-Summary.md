---
title:  モバイルアプリケーション (紹介)
linkTitle: モバイルアプリケーション (紹介)
weight: 25
isCJKLanguage: true
---

* Mobile RUMの簡単な紹介
* Application Summary ダッシュボードで、モバイルアプリケーションの<br>
  パフォーマンスの概要を確認できます

---

## 1. RUM Application Summary ダッシュボードにアクセス

左側のメニューバーから **RUM** ![RUM-ico](../../images/RUM_ico.png) を選択します。これで、RUM Application Summryページが表示されます。

このページの目的は、アプリケーションの健全性、パフォーマンス、潜在的なエラーを1つのペイン/ダッシュボードに表示し、Webサイトに対して実行されたユーザーセッションに関する情報を深く掘り下げることができるようにすることです。 

アクティブな RUM アプリケーションごとにペインが表示されます。(以下のビューは、デフォルトの拡張ビューです。）

![RUM-App-sum](../../images/Applicationsummarydashboard.png)

複数のアプリケーションを使用している場合、以下のようにペインが自動的に折りたたまれ、ペインビューが縮小されることがあります。

![RUM-App-sum-collapsed](../../images/multiple_apps_collapsed.png)

アプリケーション名の前にある左側の赤い矢印で強調されている ![RUM-browser](../../images/browser.png) または ![RUM-mobile](../../images/mobile.png) アイコン(アプリケーションの種類が *モバイル* か *ブラウザー* かによる）をクリックすると、RUM Application Summryビューをフルダッシュボードに展開することが可能です。

## 2. RUM Mobileの概要

Splunk RUM は Apple iPhone と Android Phone 向けの Native Mobile RUM をサポートしています。スマートフォンのネイティブアプリのエンドユーザーエクスペリエンスを確認するために使用することができます。

![RUM-Header](../../images/RUM-Mobile.png)

上の画面は、Splunk Mobile RUM が追跡できるさまざまなメトリクスやデータを表示するものです。例えば、以下のようなものです。

* **Custom events** ：ブラウザーアプリケーションのものと同様です。
* **App Errors** ：1分あたりの *アプリエラー* と *クラッシュ* 。
* **App Lifecycle Performance** ：OSごとの *コールドスタートアップ時間* 、 *ホットスタートアップ時間* 。
* **Request/Response** ：ブラウザーアプリケーションのものと同様です。

この時点では、スマートフォン上でネイティブアプリを実行するか、エミュレーションを実行する必要があるため、Mobile RUMについて深く掘り下げることはしません。必要に応じて、より詳細な情報をデモで提供することができます。
