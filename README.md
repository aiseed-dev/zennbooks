# zennbooks

[**zenn-cli で本（book）を管理する**](https://zenn.dev/zenn/articles/zenn-cli-guide#cli-%E3%81%A7%E6%9C%AC%EF%BC%88book%EF%BC%89%E3%82%92%E7%AE%A1%E7%90%86%E3%81%99%E3%82%8B)

カバー画像
cover.png
カバー画像の「幅 : 高さ」の比率は「1 : 1.4」(最終的に幅500px・高さ700pxにリサイズ)
カバー画像のサイズは1MB以内

### **ステップ1：ローカルのフォルダでGitを使い、GitHubに接続してプッシュする**

次に、あなたのPCのターミナル（またはコマンドプロンプトやGit Bash）で、本のフォルダ（`climbfinder-book`）に移動して、以下のコマンドを順番に実行します。

```bash
# 現在地が本のフォルダであることを確認してください
# cd path/to/zenn-climbfinder-book

# 1. このフォルダをGitの管理下に置く（初期化）
# これにより、フォルダ内に`.git`という隠しフォルダが作成されます。
git init

# 2. フォルダ内のすべてのファイルをGitの管理対象に追加する（ステージング）
# `.` は「すべてのファイル」を意味します。
git add .

# 3. 追加したファイルの状態を記録する（コミット）
# `-m` の後ろには、変更内容のメモを書きます。最初のコミットなのでこのようなメッセージが一般的です。
git commit -m "first commit: 本の初期バージョンを作成"

# 4. デフォルトのブランチ名を「main」に変更する
# GitHubの現在の標準に合わせています。
git branch -M main

# 5. ローカルのフォルダと、先ほどGitHubで作成したリポジトリを接続する
# 以下のURL部分は、GitHubのページに表示されているあなた自身のものに置き換えてください。
# 例: git remote add origin https://github.com/YourUsername/zenn-climbfinder-book.git
git remote add origin [GitHubリポジトリのURLをここに貼り付け]

# 6. ローカルのファイルをGitHubにアップロードする（プッシュ）
# これで初めて、あなたのPCからGitHubへデータが送信されます。
# 途中でGitHubのユーザー名やパスワード（またはアクセストークン）の入力を求められる場合があります。
git push -u origin main
```

これで、あなたの書いた物語のファイルがすべてGitHubにアップロードされました！

---

### **ステップ2：ZennとGitHubリポジトリを連携する**

最後に、Zennに「このGitHubリポジトリと連携して本を公開してね」と教える作業です。

1.  [Zennのダッシュボード](https://zenn.dev/dashboard)にアクセスします。
2.  左側のメニューから「GitHubからのデプロイ」を選択します。
3.  画面の指示に従い、先ほど作成したリポジトリ（`zenn-climbfinder-book`）を連携対象として登録します。

連携が完了すると、Zennが自動的にリポジトリの内容を読み取り、あなたのZennの管理画面に本が下書きとして表示されます。内容を確認し、`config.yaml`の`published: true`に変更してGitHubにプッシュすれば、本が公開されます。

---

### **今後の更新作業（物語を修正した場合）**

一度連携してしまえば、今後の更新はとても簡単です。

1.  ローカルでMarkdownファイルなどを修正します。
2.  ターミナルで以下の3つのコマンドを実行するだけです。

```bash
# 1. 変更したファイルをすべて追加
git add .

# 2. 変更内容をメモしてコミット
git commit -m "climbfinder-bookの追加"

# 3. GitHubに変更をアップロード
git push
```

`git push` を行うと、数分以内にZenn上の本のページも自動的に更新されます。
これで、美咲のように、あなたも自分の物語を世界に届ける準備が整いました。


