---
title: Spring PetClinic アプリケーションのビルド
linkTitle: 2. PetClinic のビルド
weight: 2
---

APM をセットアップするためにまず必要なものは…そう、アプリケーションです。この演習では、Spring PetClinic アプリケーションを使用します。これは Spring framework（Spring Boot 経由）で構築された、非常によく使われる Java のサンプルアプリケーションです。

まず、Spring PetClinic の GitHub リポジトリをクローンします。後ほど、アプリケーションのコンパイル、ビルド、パッケージング、テストを行います。

```bash
git clone https://github.com/spring-projects/spring-petclinic
```

`spring-petclinic` ディレクトリに移動します。

<!--
```bash
cd spring-petclinic && git checkout 276880e
```
-->

```bash
cd spring-petclinic
git checkout b26f235250627a235a2974a22f2317dbef27338d
```

Docker を使用して、PetClinic が利用する MySQL データベースを起動します。

```bash
docker run -d -e MYSQL_USER=petclinic -e MYSQL_PASSWORD=petclinic -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=petclinic -p 3306:3306 docker.io/biarms/mysql:5.7
```

次に、Spring PetClinic アプリケーションに対してトラフィックを生成するため、Locust を実行する別のコンテナを起動します。Locust はシンプルな負荷テストツールです。

```bash
docker run --network="host" -d -p 8090:8090 -v ~/workshop/petclinic:/mnt/locust docker.io/locustio/locust -f /mnt/locust/locustfile.py --headless -u 1 -r 1 -H http://127.0.0.1:8083
```

続いて、`maven` を使用してアプリケーションをコンパイル、ビルド、パッケージングします。

```bash
./mvnw package -Dmaven.test.skip=true
```

> [!INFO]
> このコマンドは、初回実行時にはアプリケーションをコンパイルする前に多くの依存関係をダウンロードするため、完了するまでに数分かかります。2 回目以降のビルドはより高速になります。

ビルドが完了したら、実行中のインスタンスのパブリック IP アドレスを取得する必要があります。次のコマンドを実行することで取得できます。

```bash
curl http://ifconfig.me
```

このコマンドで返された IP アドレスは、アプリケーションが動作していることを確認するために必要となるため、メモしておいてください。
