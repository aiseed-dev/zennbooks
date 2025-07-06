---
title: "第一章：始まりのデータ"
---
#### **第一章：始まりのデータ**

高田美咲は、平日はWebデザイナーとしてモニターに向かい、週末はクライミングジムの壁に向かう生活を送っていた。チョークの匂い、ホールドを掴んだ時の指先の感触、そして何より、自分の限界を少しだけ超えられた瞬間の達成感が、彼女を夢中にさせていた。

「次の出張、札幌なんだ。近くにいいジムないかな…」

出張先や旅先でジムを探すのは、彼女にとっていつも悩みの種だった。情報はネットに散らばり、更新が止まったままの古いサイトや、スマホではレイアウトが崩れて読めないページも少なくない。

「全国のジム情報が、見やすくまとまったアプリがあれば最高なのに…」

そんなことをクライミング仲間の健太にこぼした数日後、彼から一通のメールが届いた。
「美咲さんが言ってたやつ、昔Excelでまとめたデータがあったから送るよ！何かの役に立つかも」

添付されていたのは、全国のクライミングジムのリスト。美咲はファイルを開き、スクロールしながら考えた。「これを、あのカラフルな壁のように、もっと直感的で、わくわくするものに変えられないだろうか？」

その瞬間、最近独学で始めたプログラミング言語「Flutter」のことが頭をよぎった。Flutterなら、iOSでもAndroidでも動く美しいアプリが作れるという。

「…よし、作ってみよう。私のための、みんなのためのクライミングジム検索アプリを！」

決意した美咲の最初の仕事は、このExcelシートをアプリで扱える「JSON」形式に変換することだった。無機質なセルが、規則正しく並んだ括弧と引用符に囲まれたテキストデータに変わる。

### **美咲の変換プログラム：ExcelからJSONへ**

美咲は、健太からもらった`climbing_gym_list.xlsx`というファイルをデスクトップに保存しました。彼女は、これを手作業でJSONに書き換えるのは大変だと考え、Pythonスクリプトで自動化することにしました。

彼女の思考プロセスはこうです。
1.  **ライブラリの選定**: Excelファイルを扱うには`pandas`が、JSONを扱うには標準ライブラリの`json`が最適だと判断。
2.  **設計**:
    *   Excelファイルを読み込む。
    *   Excelの日本語の列名を、アプリで使う英語のキー名（スネークケース）に変換する対応表を作る。
    *   各行を辞書（キーと値のペア）に変換し、それらをリストにまとめる。
    *   最終的なリストを、見やすい形式でJSONファイルに出力する。
    *   空のセルは、JSONでは`null`として表現するのが一般的だと考え、そのように処理する。

以下が、美咲が書いたであろうPythonのプログラムです。

#### **準備**

まず、必要なライブラリをインストールします。ターミナル（またはコマンドプロンプト）で以下のコマンドを実行してください。

```bash
pip install pandas openpyxl
```

#### **Pythonスクリプト (`convert_to_json.py`)**

```python
import pandas as pd
import json
import os
import numpy as np

# --- 設定項目 ---

# 健太からもらったExcelファイル名
INPUT_EXCEL_FILE = 'climbing_gym_list.xlsx'

# アプリで使うJSONファイル名
OUTPUT_JSON_FILE = 'gym_data_en.json'

# Excelの列名 (日本語) と JSONのキー (英語) の対応表
# 「このキー名なら、後でコードを書くとき分かりやすいな」と考えながら美咲が定義した。
COLUMN_MAPPING = {
    'ID': 'id',
    '地方': 'region',
    '都道府県': 'prefecture',
    '市区町村': 'city',
    '住所': 'address',
    'アクセス': 'access',
    'ジム名': 'name',
    'ウェブサイト': 'website',
    '電話番号': 'phone_number',
    '壁面積(㎡)': 'wall_area',
    '壁の高さ(m)': 'wall_height',
    '駐車場': 'has_parking',
    'シャワー': 'has_shower',
    'ショップ': 'has_shop',
    '備考': 'notes'
}

def create_dummy_excel():
    """
    このスクリプトを単体で試せるように、見本のExcelファイルを作成する関数。
    美咲が健太からもらったファイルを想定しています。
    """
    if os.path.exists(INPUT_EXCEL_FILE):
        print(f"'{INPUT_EXCEL_FILE}' は既に存在します。作成をスキップします。")
        return

    print(f"見本ファイル '{INPUT_EXCEL_FILE}' を作成します...")
    # サンプルデータを作成
    sample_data = [
        {
            'ID': 1, '地方': '北海道', '都道府県': '北海道', '市区町村': '札幌市白石区',
            '住所': '北海道札幌市白石区東札幌3条2丁目1-7', 'アクセス': '地下鉄東西線「東札幌」駅より徒歩3分',
            'ジム名': 'NAC札幌クライミングジム', 'ウェブサイト': 'https://www.nacadventures.jp/nac-sapporo',
            '電話番号': '011-812-7979', '壁面積(㎡)': np.nan, '壁の高さ(m)': 10,
            '駐車場': '有', 'シャワー': '無', 'ショップ': '有', '備考': ''
        },
        {
            'ID': 2, '地方': '関東', '都道府県': '埼玉県', '市区町村': '入間市',
            '住所': '埼玉県入間市東町7-1-7', 'アクセス': '圏央道「入間IC」から約10分',
            'ジム名': 'Climb Park Base Camp', 'ウェブサイト': 'https://b-camp.jp/iruma/',
            '電話番号': '04-2936-8585', '壁面積(㎡)': 1200, '壁の高さ(m)': 15,
            '駐車場': '有', 'シャワー': '有', 'ショップ': '有', '備考': '日本最大級のクライミングジム'
        },
        {
            'ID': 3, '地方': '近畿', '都道府県': '大阪府', '市区町村': '大阪市北区',
            '住所': '大阪府大阪市北区長柄西1-5-21', 'アクセス': '天神橋筋六丁目駅から徒歩5分',
            'ジム名': 'Climbing JAM', 'ウェブサイト': 'http://climbing-jam.com/',
            '電話番号': '06-6467-4977', '壁面積(㎡)': np.nan, '壁の高さ(m)': np.nan,
            '駐車場': '無', 'シャワー': None, 'ショップ': '有', '備考': '2023年に閉店'
        },
    ]
    df = pd.DataFrame(sample_data)
    # Excelファイルとして保存（index=Falseで、行番号の列が追加されるのを防ぐ）
    df.to_excel(INPUT_EXCEL_FILE, index=False)
    print("見本ファイルの作成が完了しました。")


def convert_excel_to_json():
    """
    Excelファイルを読み込み、JSON形式に変換して出力するメインの関数。
    """
    try:
        # 1. Excelファイルを読み込む
        print(f"'{INPUT_EXCEL_FILE}' を読み込んでいます...")
        df = pd.read_excel(INPUT_EXCEL_FILE)
        
        # 2. 空のセル(NaN)をNoneに変換する。NoneはJSONのnullになる。
        #    こうしないと、json.dumpでエラーが出てしまう。
        df = df.astype(object).where(pd.notnull(df), None)

        # 3. 列名を日本語から英語に変換する
        df.rename(columns=COLUMN_MAPPING, inplace=True)
        
        # マッピングに存在する列のみを選択する（余計な列を無視するため）
        df = df[list(COLUMN_MAPPING.values())]

        # 4. DataFrameを辞書のリストに変換する
        #    `orient='records'` が、各行を辞書に変換してくれる重要なオプション。
        data_list = df.to_dict(orient='records')
        
        # 5. 辞書のリストをJSONファイルに書き出す
        print(f"'{OUTPUT_JSON_FILE}' を作成しています...")
        with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
            # `ensure_ascii=False` で日本語が文字化けしないようにする。
            # `indent=4` で、美咲が物語で作ったような綺麗なインデント付きのファイルになる。
            json.dump(data_list, f, ensure_ascii=False, indent=4)
            
        print("-" * 30)
        print(f"🎉 変換が成功しました！ '{OUTPUT_JSON_FILE}' を確認してください。")
        print("-" * 30)

    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{INPUT_EXCEL_FILE}' が見つかりませんでした。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


# --- メイン処理 ---
if __name__ == "__main__":
    # 最初に、見本となるExcelファイルを作成する（もし存在しなければ）
    create_dummy_excel()
    print("-" * 30)
    # 変換処理を実行する
    convert_excel_to_json()

```

#### **実行方法**

1.  上記のコードを `convert_to_json.py` という名前で保存します。
2.  ターミナルで、このファイルがあるディレクトリに移動します。
3.  以下のコマンドを実行します。

```bash
python convert_to_json.py
```

#### **実行結果**

実行すると、ターミナルに以下のようなメッセージが表示されます。

```
見本ファイル 'climbing_gym_list.xlsx' を作成します...
見本ファイルの作成が完了しました。
------------------------------
'climbing_gym_list.xlsx' を読み込んでいます...
'gym_data_en.json' を作成しています...
------------------------------
🎉 変換が成功しました！ 'gym_data_en.json' を確認してください。
------------------------------
```

これが、彼女のプロジェクトの記念すべき第一歩、`gym_data_en.json`が生まれた瞬間だった。

```json
// gym_data_en.json
[
    {
        "id": 1,
        "region": "北海道",
        "prefecture": "北海道",
        "city": "札幌市白石区",
        "address": "北海道札幌市白石区東札幌3条2丁目1-7",
        "access": "地下鉄東西線「東札幌」駅より徒歩3分",
        "name": "NAC札幌クライミングジム",
        "website": "https://www.nacadventures.jp/nac-sapporo",
        "phone_number": "011-812-7979",
        "wall_area": null,
        "wall_height": 10,
        "has_parking": "有",
        "has_shower": "無",
        "has_shop": "有",
        "notes": ""
    },
    {
        "id": 2,
        "region": "関東",
        "prefecture": "埼玉県",
        "city": "入間市",
        "address": "埼玉県入間市東町7-1-7",
        "access": "圏央道「入間IC」から約10分",
        "name": "Climb Park Base Camp",
        "website": "https://b-camp.jp/iruma/",
        "phone_number": "04-2936-8585",
        "wall_area": 1200,
        "wall_height": 15,
        "has_parking": "有",
        "has_shower": "有",
        "has_shop": "有",
        "notes": "日本最大級のクライミングジム"
    },
    {
        "id": 3,
        "region": "近畿",
        "prefecture": "大阪府",
        "city": "大阪市北区",
        "address": "大阪府大阪市北区長柄西1-5-21",
        "access": "天神橋筋六丁目駅から徒歩5分",
        "name": "Climbing JAM",
        "website": "http://climbing-jam.com/",
        "phone_number": "06-6467-4977",
        "wall_area": null,
        "wall_height": null,
        "has_parking": "無",
        "has_shower": null,
        "has_shop": "有",
        "notes": ""
    }
]
```
