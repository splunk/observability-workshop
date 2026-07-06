---
title: 1. タグのキャプチャ - Java
weight: 1
time: 15 minutes
---

トレースにタグを追加して、一部の顧客がアプリケーションで不満な体験をしている理由を特定しましょう。

## 有用なタグの特定

まず、`creditcheckservice` の `creditCheck` 関数のコードを確認します（ファイルは `/home/splunk/workshop/tagging/creditcheckservice-java/src/main/java/com/example/creditcheckservice/CreditCheckController.java` にあります）

```java
@GetMapping("/check")
public ResponseEntity<String> creditCheck(@RequestParam("customernum") String customerNum) {
    // Get Credit Score
    int creditScore;
    try {
        String creditScoreUrl = "http://creditprocessorservice:8899/getScore?customernum=" + customerNum;
        creditScore = Integer.parseInt(restTemplate.getForObject(creditScoreUrl, String.class));
    } catch (HttpClientErrorException e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error getting credit score");
    }

    String creditScoreCategory = getCreditCategoryFromScore(creditScore);

    // Run Credit Check
    String creditCheckUrl = "http://creditprocessorservice:8899/runCreditCheck?customernum=" + customerNum + "&score=" + creditScore;
    String checkResult;
    try {
        checkResult = restTemplate.getForObject(creditCheckUrl, String.class);
    } catch (HttpClientErrorException e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error running credit check");
    }

    return ResponseEntity.ok(checkResult);
}
```

この関数は入力として**顧客番号**を受け取ることがわかります。これはトレースの一部としてキャプチャすると便利です。他に何が役立つでしょうか？

`creditprocessorservice` からこの顧客に対して返される**クレジットスコア**も興味深いかもしれません（ただし、PII データをキャプチャしないように注意する必要があります）。また、**クレジットスコアカテゴリ**や**クレジットチェック結果**もキャプチャすると便利です。

これで、調査に役立つ4つのタグをこのサービスからキャプチャすることを特定しました。では、これらをどのようにキャプチャすればよいでしょうか？

## タグのキャプチャ

まず、`CreditCheckController.java` ファイルの先頭にある以下の OpenTelemetry インポートのコメントを解除します

```java
...
import io.opentelemetry.api.trace.SpanKind;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.instrumentation.annotations.WithSpan;
import io.opentelemetry.instrumentation.annotations.SpanAttribute;
```

次に、`creditCheck` のスパンを生成するために `@WithSpan` アノテーションのコメントを解除します

```java
@GetMapping("/check")
@WithSpan(kind=SpanKind.SERVER)
public ResponseEntity<String> creditCheck(@RequestParam("customernum") String customerNum) {
    ...
```

これで現在のスパンへの参照を取得し、属性（タグ）を追加できます

```java
...
try {
    String creditScoreUrl = "http://creditprocessorservice:8899/getScore?customernum=" + customerNum;
    creditScore = Integer.parseInt(restTemplate.getForObject(creditScoreUrl, String.class));
} catch (HttpClientErrorException e) {
    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error getting credit score");
}
Span currentSpan = Span.current(); // ADDED
currentSpan.setAttribute("credit.score", creditScore); // ADDED
...
```

簡単でしたね？さらにキャプチャを追加しましょう。最終的な結果は以下のようになります

```java
@GetMapping("/check")
@WithSpan(kind=SpanKind.SERVER)
public ResponseEntity<String> creditCheck(@RequestParam("customernum")
                                          @SpanAttribute("customer.num")
                                          String customerNum) {
    // Get Credit Score
    int creditScore;
    try {
        String creditScoreUrl = "http://creditprocessorservice:8899/getScore?customernum=" + customerNum;
        creditScore = Integer.parseInt(restTemplate.getForObject(creditScoreUrl, String.class));
    } catch (HttpClientErrorException e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error getting credit score");
    }
    Span currentSpan = Span.current();
    currentSpan.setAttribute("credit.score", creditScore);

    String creditScoreCategory = getCreditCategoryFromScore(creditScore);
    currentSpan.setAttribute("credit.score.category", creditScoreCategory);

    // Run Credit Check
    String creditCheckUrl = "http://creditprocessorservice:8899/runCreditCheck?customernum=" + customerNum + "&score=" + creditScore;
    String checkResult;
    try {
        checkResult = restTemplate.getForObject(creditCheckUrl, String.class);
    } catch (HttpClientErrorException e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error running credit check");
    }
    currentSpan.setAttribute("credit.check.result", checkResult);

    return ResponseEntity.ok(checkResult);
}
```

## サービスの再デプロイ

これらの変更が完了したら、以下のスクリプトを実行して `creditcheckservice` で使用される Docker イメージを再ビルドし、Kubernetes クラスターに再デプロイします

``` bash
./5-redeploy-creditcheckservice.sh java
```

## タグが正常にキャプチャされたことを確認

数分後、**Splunk Observability Cloud** に戻り、最新のトレースの1つを読み込んで、タグが正常にキャプチャされたことを確認します（ヒント：タイムスタンプでソートして最新のトレースを見つけてください）

**![Trace with Attributes](../../images/trace_with_attributes_java.png)**

お疲れ様でした。OpenTelemetry のスキルがレベルアップし、タグを使用してトレースにコンテキストを追加できるようになりました。

次は、これらのタグを **Splunk Observability Cloud** でどのように活用できるかを見ていきましょう！
