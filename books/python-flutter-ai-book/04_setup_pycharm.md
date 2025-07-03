---
title: "第４章：PyCharmをセットアップ！魔法の作業台を組み立てよう"
---

おめでとうございます！最高の仕事道具としてPyCharmを選びましたね。この章では、PyCharmをインストールし、第２章で作った秘密基地（Miniforge）と接続します。これであなたの開発環境が完成します！

### 1. PyCharmをインストールしよう！ 💻

私たちが使うのは、無料で非常に強力な**「PyCharm Community Edition」**です。

*   公式サイト: [https://www.jetbrains.com/pycharm/download/](https://www.jetbrains.com/pycharm/download/)
*   ページが開いたら、**「Community」**と書かれた方の**「ダウンロード」**ボタンをクリックしてください。
*   ダウンロードしたインストーラを実行し、画面の指示に従って「Next」をクリックしていけばインストールは完了です。途中のチェックボックスは、特に何も変更しなくて大丈夫ですよ。

### 2. 最初のプロジェクトを作ろう！ 🚀

PyCharmを初めて起動すると、プロジェクトを作成する画面になります。ここが、Miniforgeと接続するための重要なポイントです！

1.  **「New Project」**をクリックします。
2.  **Location**: プロジェクトを保存する場所です。右側のフォルダアイコンをクリックし、デスクトップなどに `my-python-project` という名前のフォルダを新しく作って指定しましょう。
3.  **Python Interpreter**: ここが最重要ポイントです！
    *   「New environment using」ではなく、**「Previously configured interpreter」**（以前に設定されたインタプリタ）を選択してください。
    *   右側の「...」ボタンをクリックします。
    *   左のメニューから**「Conda Environment」**を選択します。
    *   「Interpreter」の欄に、MiniforgeのPythonが自動で表示されているはずです。（例: `C:\Users\YourUser\miniforge3\python.exe`）もし表示されていなければ、右のフォルダアイコンからこのパスを指定します。
    *   **「OK」**をクリックします。
4.  最後に、右下の**「Create」**ボタンをクリックします。

### 3. 連携の確認！🤝

PyCharmのメイン画面が開きます。右下隅に**`Python 3.x (conda)`** のように表示されていれば、連携は大成功です！✨

**本当にお疲れ様でした！**
これで、PyCharmという最高の作業台から、Miniforgeという強力な秘密基地を自由に操作できるようになりました。次の章では、データサイエンスの必須ツール「Jupyter」について学びます！

