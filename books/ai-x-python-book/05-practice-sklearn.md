---
title: 第5章 実践① 手書き文字を認識させてみよう！ (機械学習)
---

お待たせしました。ここからが、AI開発の冒険の始まりです。
最初のプロジェクトでは、コンピュータに「目」を持たせる、古典的かつ非常に面白いテーマである**画像認識**に挑戦します。具体的には、AIに手書きされた数字の画像を見せて、それが0から9までのどの数字なのかを当てさせるプログラムを作成します。

このタスクを通じて、あなたはAI開発の最も基本的なプロセスである「学習」「予測」「評価」の一連の流れを体験することになります。

## 0. 準備：プロジェクトの開始

まずは、AI開発の「黄金律」に従って、このプロジェクトのための新しい作業スペースを準備します。

1.  **Windows Terminalを開きます。**
    プロンプトの先頭に`(base)`が表示されていることを確認してください。

2.  `cd C:\dev` コマンドで、私たちのアトリエに移動します。
    ```powershell
    cd C:\dev
    ```

3.  このプロジェクト専用の新しいフォルダを作成します。フォルダ名は `handwriting-ai` としましょう。
    ```powershell
    mkdir handwriting-ai
    ```

4.  作成したプロジェクトフォルダに移動します。
    ```powershell
    cd handwriting-ai
    ```
    現在地が `C:\dev\handwriting-ai` になっていることを確認してください。

5.  **このプロジェクト専用のConda環境を作成・アクティベートします。**
    `base`環境を直接使うのではなく、プロジェクトごとに専用の環境を作るのが良い習慣です。これにより、将来他のプロジェクトとライブラリが衝突するのを防ぎます。
    
    環境名は `handwriting-env` とし、このプロジェクトで必要となるライブラリを同時にインストールします。
    :::message
    - `python=3.10`: 使用するPythonのバージョンを指定します。
    - `scikit-learn`: 今回の主役である、機械学習のための総合ライブラリです。
    - `matplotlib`: データをグラフや画像で表示するためのライブラリです。
    - `jupyterlab`: 対話的にコードを実行できるJupyter NotebookをVS Code上で動かすために必要です。
    :::
    ```powershell
    conda create -n handwriting-env python=3.10 scikit-learn matplotlib jupyterlab -y
    ```
    インストールには少し時間がかかります。完了したら、作成した環境を有効化（アクティベート）します。
    ```powershell
    conda activate handwriting-env
    ```
    プロンプトの先頭が `(base)` から `(handwriting-env)` に変わったことを確認してください。これが、専用の部屋に入った合図です。

6.  準備の総仕上げです。**`code .`** と打ち込み、このプロジェクトをVS Codeで開きます。
    ```powershell
    code .
    ```

## 1. 実装：Jupyter NotebookでAIを動かす

VS Codeが起動したら、いよいよAIを動かすコードを書いていきます。今回は、試行錯誤をしながら対話的に開発を進めるのに最適な**Jupyter Notebook**を使用します。

1.  **Python環境（インタープリター）の選択**
    VS Codeが、私たちが今アクティベートした `handwriting-env` 環境を正しく認識しているか確認・設定します。
    - 右下にPythonのバージョンが表示されている部分をクリックするか、`Ctrl+Shift+P`でコマンドパレットを開き、「Python: Select Interpreter」と入力して選択します。
    - 候補の中から、パスに `handwriting-env` を含むものを選択します。これで、このVS Codeウィンドウは `handwriting-env` の中のライブラリを使うようになります。

2.  **Jupyter Notebookファイルの作成**
    - VS Codeのエクスプローラー（左側のファイル一覧パネル）で、`handwriting-ai` フォルダが選択されていることを確認し、新しいファイル作成アイコンをクリックします。
    - ファイル名を `main.ipynb` とします。`.ipynb` がJupyter Notebookの拡張子です。

3.  **コードの記述と実行**
    `main.ipynb` を開くと、セルと呼ばれるコードの入力ブロックが表示されます。ここにコードを少しずつ記述し、実行しながら結果を確認していきます。

---

### ステップA: 必要なライブラリの読み込み
最初のセルに、今回使用する道具（ライブラリ）をインポートするコードを書きます。

```python
# scikit-learnから、データセット、機械学習モデル、評価指標をインポート
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# 画像を表示するためのmatplotlibをインポート
import matplotlib.pyplot as plt

# データを扱うためのnumpyをインポート (scikit-learnが内部で使っているので追加インストール不要)
import numpy as np
```
セルにコードを入力したら、セルの左側にある再生ボタン▶を押すか、`Shift + Enter`キーを押して実行します。エラーが出なければ、準備完了です。

### ステップB: データの準備と確認
次に、`scikit-learn`が練習用に用意してくれている手書き数字のデータセットを読み込みます。

```python
# 手書き数字データセットを読み込む
digits = load_digits()

# どんなデータが入っているか見てみよう
# 最初の10個の画像データを表示してみる
fig, axes = plt.subplots(2, 5, figsize=(10, 5))
for i, ax in enumerate(axes.flat):
    ax.imshow(digits.images[i], cmap='binary')
    ax.set_title(f"Label: {digits.target[i]}")
    ax.axis('off')
plt.show()
```
このセルを実行すると、8x8ピクセルの低解像度な手書き数字の画像が10個表示されます。`Label`が、その画像がどの数字であるかを示す「正解ラベル」です。AIの仕事は、この画像データだけを見て、この`Label`を当てることです。

### ステップC: AIの学習
データを「AIへの教材（学習データ）」と「AIの実力を測るテスト（テストデータ）」に分け、AIに教材を渡して学習させます。

```python
# 画像データと正解ラベルを取得
X = digits.data
y = digits.target

# データを学習用とテスト用に8:2の割合で分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# AIモデル（今回はサポートベクターマシンという手法）を作成
model = SVC(gamma=0.001)

# 学習用データを使ってAIに学習させる (fitメソッド)
model.fit(X_train, y_train)

print("学習が完了しました！")
```
このセルを実行すると、AIモデルが学習データ（`X_train`と`y_train`）から、数字の画像とその正解の組み合わせのパターンを学びます。

### ステップD: AIの予測と評価
学習が終わったAIに、一度も見せたことのないテストデータを渡し、どれくらい正しく予測できるか実力を試します。

```python
# テストデータを使って予測を行う (predictメソッド)
y_pred = model.predict(X_test)

# 正解率を計算して表示する
accuracy = accuracy_score(y_test, y_pred)
print(f"AIの正解率: {accuracy * 100:.2f}%")

# いくつか予測結果を実際に見てみよう
fig, axes = plt.subplots(4, 4, figsize=(8, 8))
for i, ax in enumerate(axes.flat):
    if i < len(X_test):
        ax.imshow(X_test[i].reshape(8, 8), cmap='binary')
        ax.set_title(f"Pred: {y_pred[i]} | True: {y_test[i]}")
        ax.axis('off')
plt.show()
```
このセルを実行すると、まずAIの正解率がパーセントで表示されます。おそらく98%を超える非常に高い精度が出るはずです。

そして、その下にテスト画像とAIの予測（`Pred`）、そして実際の正解（`True`）が並べて表示されます。AIがほとんどの数字を正しく認識していることに驚くでしょう。時々間違えているものがあれば、それは人間でも少し迷うような形の数字かもしれません。

---

## 【AIに聞いてみよう①】コード解説

さて、あなたはAIを動かすことに成功しました。しかし、コピー＆ペーストしたコードの中に、まだ意味がよく分からない部分があるかもしれません。

例えば、この一行は何をしているのでしょうか？
`X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)`

ここで、私たちの最強の家庭教師であるAIの出番です。この機会に、「AIに質問して理解を深める」という新しい学習スタイルを体験してみましょう。

1.  Webブラウザで、Google Geminiなどの対話型AIサービスを開きます。
    [https://gemini.google.com/](https://gemini.google.com/)

2.  AIへの質問（プロンプト）を入力するボックスに、以下のように質問を組み立てて入力します。

    **プロンプト例:**
    ```
    私はPythonの初心者です。以下のscikit-learnのコードが何をしているか、各部分の役割をステップバイステップで、専門用語をできるだけ使わずに分かりやすく説明してください。

    コード:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    ```

3.  AIからの回答を読んでみましょう。おそらく、以下のような内容を、より丁寧に解説してくれるはずです。
    *   `train_test_split`は、データを「学習用」と「テスト用」に分割するための関数であること。
    *   `X`（画像データ）と`y`（正解ラベル）をペアを崩さずに分割してくれること。
    *   `test_size=0.2`は、全体の20%をテスト用に、残りの80%を学習用にする、という割合の指定であること。
    *   `random_state=42`は、分割の仕方を固定するための「乱数の種」であり、この数字があるおかげで、誰が実行しても同じようにデータが分割され、結果を再現できること。

このように、ただコードを動かすだけでなく、分からない部分をAIに質問することで、あなたの知識は断片的なものではなく、体系的な理解へと深まっていきます。これからの学習で、この「AIに聞く」という習慣をぜひ活用してください。

