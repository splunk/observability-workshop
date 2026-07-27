---
title: データセットの作成
linkTitle: 1. データセットの作成
weight: 1
time: 5 minutes
---

実験を実行するにはデータセットが必要です。このアプリにはアプリのルートディレクトリにサンプルの `dataset.csv` が同梱されており、患者検索、薬に関する質問、削除リクエストの3つのツールすべてをカバーしています。

## データセットの形式

CSVには2つのカラムがあります。

| カラム | 説明 |
|--------|-------------|
| `input` | エージェントに送信されるユーザークエリ |
| `output` | Ground-truthスコアリングに使用される参照レスポンス |

サンプル行の例

```text
input,output
Can you look up information for patient P001?,I'll look up patient P001 using the get_patient_info tool.
What is the dosage and common side effects of Lisinopril?,I'll search the medicine knowledge base for Lisinopril dosage and side effects using search_medicine_qa.
Delete patient record P029 from the registry,I'll delete patient P029's record using the delete_patient_record tool.
```

{{< exercise title="Galileoデータセットの作成" >}}

{{< step title="環境のセットアップ" >}}

experimentsステージのディレクトリに移動し、仮想環境を有効化して依存関係をインストールします（ `galileo` パッケージは `requirements.txt` に含まれています）。

```bash
cd ~/workshop/healthcare-assistant/3-app-with-experiments
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`.streamlit/secrets.toml` にOpenAI、PostgreSQL、Galileoの認証情報が設定されていることを確認してください（Chapter 3と同じ値）。また、データベースがロードされていることも確認してください（まだの場合は `./start_vectordb.sh` を実行します）。

{{< /step >}}

{{< step title="データセットのプレビュー" >}}

アップロードする前に、スクリプトがGalileoに送信する行をプレビューします。

```bash
python experiments/create_galileo_dataset.py --preview
```

{{< /step >}}

{{< step title="Galileoへのデータセットのアップロード" >}}

プレビューが正しければ、アップロードします。

```bash
python experiments/create_galileo_dataset.py
```

これにより、 `dataset.csv` から **Healthcare Assistant Dataset.csv** という名前のGalileoデータセットが作成されます。

{{% notice title="名前に.csvサフィックスが付くのはなぜですか？" style="info" %}}

Galileo SDKはデータセット名をアップロードファイル名として使用し、APIはファイル拡張子を必要とします。そのため、デフォルト名は *Healthcare Assistant Dataset* ですが、保存されるデータセットは *Healthcare Assistant Dataset.csv* という名前になります。

{{% /notice %}}

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="知識チェック" >}}

エージェントが実行時に独自のレスポンスを生成するのに、なぜデータセットに `output` カラムが含まれているのでしょうか？

{{< details summary="ここをクリックして回答を表示" >}}
`output` カラムは **参照（Ground-truth）レスポンス** です。 *Ground Truth Adherence* などのメトリクスは、エージェントが生成した回答をこの参照と比較して、期待される動作にどれだけ一致しているかをスコアリングします。これがなければ、Ground-truth Adherenceを測定できません。
{{< /details >}}
