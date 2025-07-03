### 第９章：【実践】ExcelをJSONに変換！AIとデータ加工の魔法

✨ **第９章：【実践】ExcelをJSONに変換！AIとデータ加工の魔法** 🧙‍♀️

これまでの章で、AIと協力してプログラムを動かす基本を学びました。この最終章では、より実践的なシナリオとして、ビジネス現場で多用されるExcelファイルを、Webサービスなどで広く利用されるJSON形式に変換するプログラムをAIに作ってもらいます。これで、あなたは「データの翻訳家」として、AIと協力して新たな価値を生み出す力を手に入れます！

### なぜExcelからJSONへ？

*   **Excel**: 人間が見やすい「表」。
*   **JSON**: プログラムが扱いやすい「メモ書き」。Webの世界の共通語です。

ExcelデータをJSONに変換することで、Webサイトのマップに表示したり、スマホアプリで検索したりと、データの活躍の場が大きく広がります。

### 1. AIへの指示（プロンプト）を考えよう 🗣️

手元に `gym_list.xlsx` というExcelファイル（ID, 店舗名, 住所, 緯度, 経度 の列がある）があると仮定し、AIに次のように「魔法の呪文」を唱えてみましょう！

**あなたからAIへの指示（プロンプト）例:**

```
Pythonで、gym_list.xlsx というExcelファイルを、gym_list.json というJSONファイルに変換するコードを教えてください。

お願い：
* Excelの1行が、JSONのデータ1つになるようにしてください。
* 日本語がきちんと表示されるようにしてください。
```

### 2. AIが生成したコードと実行準備 🛠️

AIは、あなたの指示に基づいて次のようなコードを生成してくれるでしょう。

**AIが生成したコード例:**

```python
import pandas as pd

# Excelファイルを読み込む
excel_file_path = 'gym_list.xlsx'
try:
    df = pd.read_excel(excel_file_path)

    # JSONファイルに出力する
    json_file_path = 'gym_list.json'
    df.to_json(json_file_path, orient='records', force_ascii=False, indent=4)

    print(f"✅ '{excel_file_path}' を '{json_file_path}' に変換しました。")

except FileNotFoundError:
    print(f"❌ エラー: '{excel_file_path}' が見つかりません。")
except Exception as e:
    print(f"❌ エラーが発生しました: {e}")
```

**実行前の準備:**
このコードを動かすには、`pandas` と `openpyxl` という便利な道具が必要です。PyCharmのターミナルで、以下のコマンドを実行してインストールしましょう。

```bash
pip install pandas openpyxl
```

### 3. 実行と結果の確認！ ✅

1.  **ファイル作成**: PyCharmで `excel_to_json.py` というファイル名で上記のコードを保存します。そして、同じ階層に、サンプルデータを入れた`gym_list.xlsx`を作成しておきましょう。
2.  **実行**: PyCharmのターミナルで `python excel_to_json.py` を実行します。
3.  **結果確認**: `gym_list.json` というファイルが新しく作成されているはずです！🎉 中身を見ると、ExcelデータがJSON形式に美しく変換されていることが確認できます。感動ですね！

---

🎉 **最初の冒険、完了です！** 🎉

**本当にお疲れ様でした！** あなたはここまで、一つ一つの章をクリアし、AIと協業しながら実践的なプログラムを動かすスキルを身につけました。

これであなたは、PythonとAIを使いこなし、データを自在に操るための、モダンでクリーンな開発環境と基本スキルを手に入れました。

ここからが、あなたの本当の開発者としての旅の始まりです！この素晴らしい環境で、たくさんのプログラムを作り、新しい世界を思いっきり楽しんでください！