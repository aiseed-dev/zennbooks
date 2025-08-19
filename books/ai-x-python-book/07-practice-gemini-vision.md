---
title: 第7章 実践③ Geminiに画像を「説明」させてみよう (マルチモーダルAI)
---

これまでの章で、あなたは「予測AI」と「テキスト生成AI」を体験しました。最後の実践プロジェクトでは、AI開発の最先端領域である「**マルチモーダルAI**」の世界に足を踏み入れます。

マルチモーダルAIとは、テキスト、画像、音声など、複数の異なる種類の情報（モダリティ）を同時に理解し、処理できるAIのことです。

この章のゴールは、あなたのPCにある好きな**画像**をAIに見せ、その内容について**テキスト**で対話するプログラムを作成することです。例えば、旅行先で撮った風景写真を見せて「この写真について詩を書いて」とお願いしたり、料理の写真を見せて「この料理のレシピを推測して」と質問したりできるようになります。

## 0. 準備：プロジェクトの開始

黄金律に従い、最後のプロジェクトを始めましょう。

1.  **Windows Terminalを開きます。**
    `(gemini-env)`が有効な場合は`conda deactivate`で`base`環境に戻ります。

2.  `cd C:\dev`でアトリエに移動します。

3.  このプロジェクト用の新しいフォルダ `gemini-multimodal` を作成し、そこに移動します。
    ```powershell
    mkdir gemini-multimodal
    cd gemini-multimodal
    ```

4.  **画像の準備**
    AIに見せたい好きな画像ファイル（JPEGまたはPNG形式）を、エクスプローラーを使ってこの`gemini-multimodal`フォルダの中にコピーしてください。ファイル名は、半角英数字の簡単なもの（例: `dog.jpg`, `tokyo_tower.png`）にしておくと、後の作業が楽になります。

5.  **環境の準備**
    今回は、画像処理ライブラリも必要になります。`gemini-multimodal-env`という名前で新しい環境を作成しましょう。
    ```powershell
    conda create -n gemini-multimodal-env python=3.10 -y
    conda activate gemini-multimodal-env
    ```
    
6.  **必要なライブラリのインストール**
    Gemini APIライブラリと、画像を扱うための`Pillow`というライブラリを`pip`でインストールします。
    ```powershell
    pip install google-generativeai pillow
    ```

7.  `code .`で、このプロジェクトをVS Codeで開きます。

## 1. 実装：画像とテキストでAIと対話する

今回もPythonスクリプトファイルを作成して実装します。

1.  **Python環境の選択**
    VS Codeのインタープリターが `gemini-multimodal-env` になっていることを確認・設定します。

2.  **スクリプトファイルの作成**
    VS Codeのエクスプローラーで、`vision.py` という名前の新しいファイルを作成します。

3.  **コードの記述**
    `vision.py`に以下のコードを記述します。

---
```python
import os
from PIL import Image
import google.generativeai as genai

# APIキーの設定（第6章と同様）
API_KEY = "ここに、あなたのAPIキーを貼り付けます"
genai.configure(api_key=API_KEY)

# 1. 使用するモデルを選択
#    今回は、画像入力に対応した `gemini-pro-vision` を使用します。
model = genai.GenerativeModel('gemini-pro-vision')

# 2. 画像ファイルを読み込む
try:
    # ここで、あなたがフォルダに入れた画像ファイル名に書き換えてください
    image_file_name = "dog.jpg" 
    img = Image.open(image_file_name)
except FileNotFoundError:
    print(f"エラー: '{image_file_name}' が見つかりません。フォルダに画像ファイルを入れましたか？")
    exit()

# 3. AIへの質問（プロンプト）を準備
prompt = "この画像に写っているものについて、詳細に説明してください。"

# 4. 画像とプロンプトをAIに渡して、応答を生成させる
#    `model.generate_content` にリスト形式で画像とテキストを渡すのがポイントです。
response = model.generate_content([prompt, img])

# 5. AIの応答を表示
print("--- AIからの応答 ---")
print(response.text)
print("--------------------")

```
---
**コードの注意点:**
- `API_KEY = "..."` の部分に、あなたのAPIキーを忘れずに貼り付けてください。
- `image_file_name = "dog.jpg"` の部分を、あなたが`gemini-multimodal`フォルダに入れた実際の画像ファイル名に書き換えてください。

4.  **プログラムの実行**
    - VS Codeのターミナルで、`gemini-multimodal-env`環境で`C:\dev\gemini-multimodal`にいることを確認します。
    - ターミナルで以下のコマンドを実行します。
    ```powershell
    python vision.py
    ```

5.  **AIの応答を確認**
    プログラムを実行すると、AIが画像を分析し、その内容を説明する文章がターミナルに表示されます。犬の写真なら「茶色い毛並みの中型犬が、芝生の上で楽しそうにボールを追いかけています」のように、驚くほど的確な説明が返ってくるはずです。

### 色々な質問を試してみよう！
`prompt`の文字列を書き換えることで、AIとの対話の幅が無限に広がります。

*   `"この写真から、面白い物語を創作してください。"`
*   `"この風景写真に合う、感動的なキャッチコピーを3つ考えて。"`
*   `"この画像の状況を、ユーモアを交えて説明して。"`

`prompt`を書き換えてはプログラムを実行し、AIの創造性を引き出して遊んでみてください。これこそが、マルチモーダルAIの真の面白さです。

---

## 【AIに聞いてみよう③】エラー解決

プログラミングにおいて、エラーは避けて通れないものです。熟練の開発者でさえ、日常的にエラーに遭遇し、その解決に時間を費やします。重要なのは、エラーを恐れることではなく、**効率的に解決する方法**を知っていることです。

そして現代において、AIは最も優秀なデバッグ（エラー解決）アシスタントの一人です。

さっそく、意図的にエラーを発生させ、AIに解決を手伝ってもらう体験をしてみましょう。

1.  先ほど作成した `vision.py` ファイルを開き、一行をわざと間違えてみます。
    `model = genai.GenerativeModel('gemini-pro-vision')`
    この行の `GenerativeModel` を、例えば `Generative**Modell**` のように、スペルを一つ間違えてみてください。

2.  その状態で、ターミナルから再度 `python vision.py` を実行します。

3.  すると、プログラムは正常に動かず、赤文字でたくさんのエラーメッセージが表示されるはずです。最後の行あたりに、おそらくこのようなエラーが出ているでしょう。
    `AttributeError: module 'google.generativeai' has no attribute 'GenerativeModell'`

4.  初心者にとって、このメッセージは暗号のように見えるかもしれません。しかし、慌てる必要はありません。このエラーメッセージ全体を、マウスで選択してコピーします。

5.  Webブラウザで、Google Geminiなどの対話型AIサービスを開きます。

6.  AIへの質問（プロンプト）を入力するボックスに、以下のように質問します。

    **プロンプト例:**
    ```
    私はPython初心者です。以下のPythonスクリプトを実行したところ、エラーが発生しました。
    エラーメッセージの原因と、コードのどこをどのように修正すれば良いか教えてください。

    【エラーメッセージ】
    (ここに、先ほどコピーしたエラーメッセージを貼り付けます)

    【ソースコード】
    (ここに、エラーが出た vision.py のコード全体を貼り付けます)
    ```

7.  AIからの回答を見てみましょう。AIは瞬時にエラーメッセージとコードを分析し、以下のような的確なアドバイスを返してくれるはずです。
    *   **エラーの原因**: `AttributeError` は、指定したモジュール（今回は`google.generativeai`）に、呼び出そうとした名前（`GenerativeModell`）の属性（関数やクラス）が存在しないことを意味します。
    *   **具体的な指摘**: `GenerativeModell` というスペルは間違いで、正しくは `GenerativeModel` です。
    *   **修正案**: `vision.py` の該当行を `model = genai.GenerativeModel('gemini-pro-vision')` に修正してください。

このように、エラーメッセージを恐れずにAIに提示することで、問題の解決にかかる時間を劇的に短縮できます。エラーは「失敗」ではなく、AIとの対話を通じて学びを深めるための「きっかけ」なのです。
