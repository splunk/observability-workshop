---
title: Spring PetClinic アプリケーションのビルド
linkTitle: 2. PetClinic のビルド
weight: 2
---

APM をセットアップするために最初に必要なのは...そう、アプリケーションです。この演習では、Spring PetClinic アプリケーションを使用します。これは、Spring フレームワーク（Springboot）で構築された非常に人気のあるサンプル Java アプリケーションです。

まず、PetClinic の GitHub リポジトリをクローンし、その後アプリケーションのコンパイル、ビルド、パッケージ化、テストを行います：

```bash
git clone https://github.com/spring-projects/spring-petclinic
```

`spring-petclinic` ディレクトリに移動します：

<!--
```bash
cd spring-petclinic && git checkout 276880e
```
-->

```bash
cd spring-petclinic
git checkout b26f235250627a235a2974a22f2317dbef27338d
```

Docker を使用して、PetClinic が使用する MySQL データベースを起動します：

```bash
docker run -d -e MYSQL_USER=petclinic -e MYSQL_PASSWORD=petclinic -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=petclinic -p 3306:3306 docker.io/biarms/mysql:5.7
```

次に、PetClinic アプリケーションにシンプルなトラフィックを生成する Locust を実行する別のコンテナを起動します。Locust は、Web アプリケーションにトラフィックを生成するために使用できるシンプルな負荷テストツールです。

```bash
docker run --network="host" -d -p 8090:8090 -v ~/workshop/petclinic:/mnt/locust docker.io/locustio/locust -f /mnt/locust/locustfile.py --headless -u 1 -r 1 -H http://127.0.0.1:8083
```

次に、`maven` を使用して PetClinic をコンパイル、ビルド、パッケージ化します：

```bash
./mvnw package -Dmaven.test.skip=true
```

> [!INFO]
> 初回実行時は数分かかり、アプリケーションをコンパイルする前に多くの依存関係をダウンロードします。以降のビルドはより高速になります。

ビルドが完了したら、実行しているインスタンスのパブリック IP アドレスを取得する必要があります。以下のコマンドを実行して取得できます：

```bash
curl http://ifconfig.me
```

IP アドレスが返されます。アプリケーションが実行されていることを確認するために必要になるので、この IP アドレスをメモしておいてください。
