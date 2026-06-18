---
title: 結果の理解
linkTitle: 1.2 結果の理解
weight: 2
---

1. Synthetics のランディングページからテストをクリックしてサマリービューを表示し、[Performance KPIs chart](https://docs.splunk.com/observability/en/synthetics/uptime-test/uptime-test-results.html#customize-the-performance-kpis-chart) のフィルターを操作して、データをさまざまな角度から分析する方法を確認します。ここはトレンドを理解し始めるのに最適な場所です。後ほど、カスタムチャートがどのように表示されるかを確認し、最も重要な KPI に合わせてダッシュボードをカスタマイズできるようにします。
![KPI chart filters](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-09/c040b5f6-a868-4977-8d3b-bc3e431ffcc8/user_cropped_screenshot.jpeg?tl_px=1160,0&br_px=2880,961&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=755,44)
{{% notice title="ワークショップの質問: Performance KPIs chart の使用" style="tip" icon="question" %}}
どのようなメトリクスが利用可能ですか？データは時間やロケーション間で一貫していますか？特定のロケーションが他より遅いですか？スパイクや障害はありますか？
{{% /notice %}}

1. チャートまたは下のテーブルから最近の実行結果をクリックします。
![run results chart](../../_img/run-results.png)

1. 障害がある場合は、レスポンスを確認して、レスポンスコードアサーション（302 が一般的です）を追加する必要があるか、認証が必要か、または異なるリクエストヘッダーを追加する必要があるかを確認します。ここでは、この特定のテスト実行に関する情報（成功したか失敗したか、ロケーション、タイムスタンプ、所要時間）が、他の Uptime テストメトリクスとともに表示されます。レスポンス、リクエスト、接続情報もクリックして確認できます。
![uptime test result](../../_img/uptime-test-result.png)
テストを正常に実行するために編集が必要な場合は、この実行結果ページの左上のパンくずリストでテスト名をクリックし、テスト概要ページの右上にある {{% button %}}Edit test{{% /button %}} をクリックします。テスト設定を編集した後は、下にスクロールして {{% button style="blue" %}}Submit{{% /button %}} をクリックして変更を保存することを忘れないでください。

1. テストが正常に実行されることに加えて、エンドポイントの健全性を測定するための他のメトリクスもあります。例えば、[Time to First Byte](https://web.dev/articles/ttfb)（TTFB）はパフォーマンスの優れた指標であり、[TTFB を最適化](https://web.dev/articles/optimize-ttfb)することでエンドユーザーエクスペリエンスを向上させることができます。

1. テスト概要ページに戻り、Performance KPIs chart を First Byte time の表示に変更します。テストが十分な期間実行されると、時間枠を拡大するとデータポイントがラインとして描画され、以下の例のようにトレンドや異常をより確認しやすくなります。
![Performance KPIs for Uptime Tests](../../_img/ttfb.png)

上記の例では、TTFB がロケーション間で一貫して異なることがわかります。これを踏まえて、メトリクスをレポートする際にロケーションを考慮することができます。また、例えばそれらのロケーションのユーザーに対して、より近くにホストされたエンドポイントを提供することでエクスペリエンスを改善でき、ネットワークレイテンシーを削減できるはずです。時間の経過とともに結果に若干のばらつきが見られますが、全体として、このエンドポイントの KPI のベースラインを十分に把握できています。ベースラインがあれば、メトリクスの悪化に対してアラートを設定したり、改善を可視化したりすることができます。
{{% notice title="ヒント" style="primary"  icon="lightbulb" %}}
テストが一貫して正常に実行されていることを確認するため、まだこのテストにディテクターを設定していません。非常に重要なエンドポイントをテストしていて、できるだけ早くアラートを受け取りたい場合（潜在的なアラートノイズを許容できる場合）は、**[Single Test Detectors](../../5-detectors/1-test-detector.md)** に進んでください。
{{% /notice %}}

Uptime テストが正常に実行されるようになったら、次のテストタイプに進みましょう。
