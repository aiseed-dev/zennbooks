---
title: 付録　Gitの基本操作
---
アプリ開発では、Gitを使ったバージョン管理が欠かせません。この付録では、Gitの基本操作と、GitHubとの連携方法を解説します。

## A.1　Git の基本操作まとめ

### Git の基本用語

* **リポジトリ（Repository）** : プロジェクト全体の履歴を管理する領域
* **コミット（Commit）** : ファイルの変更履歴を記録する単位
* **ステージング（Staging）** : コミットする前に変更を一時保管する領域

### よく使うコマンド

```powershell
# 初期化
cd C:\dev\myproject
git init

# ファイルを作って追加
New-Item README.md
git add README.md

# コミット
git commit -m "最初のコミット"

# 状態確認
git status

# 履歴確認
git log
```

---

## A.2　.gitignore を設定しよう

Flutterプロジェクトでは、**ビルド成果物や一時ファイルをGitに含めない**ように`.gitignore`を使います。

### 例：Flutter用の基本 .gitignore

```gitignore
build/
.dart_tool/
.packages
.idea/
.vscode/
*.iml
```

`.gitignore` ファイルをプロジェクト直下に置くだけで機能します。

---

## A.3　GitHub と連携する（HTTPS + トークン認証）

2024年以降、GitHubでは**SSH鍵による接続が制限されつつあり**、代わりに **HTTPS + パーソナルアクセストークン（PAT）** が標準になっています。

### ステップ 1：GitHub アカウントの作成

[https://github.com](https://github.com) にアクセスして無料アカウントを作成しましょう。

---

### ステップ 2：GitHub で新しいリポジトリを作る

GitHub上で「New repository」→ 名前を入力 → 「Create repository」

---

### ステップ 3：ローカルリポジトリと接続

```powershell
git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git
git branch -M main
git push -u origin main
```

> ✅ 初回の push では、パスワードの代わりに「トークン」を入力する必要があります。

---

### ステップ 4：パーソナルアクセストークン（PAT）の発行方法

1. GitHub右上のアイコン → \[Settings]
2. 左メニューで \[Developer settings] → \[Personal access tokens]
3. \[Generate new token] をクリック
4. `repo` 権限などにチェックを入れて、トークンを発行

> 📌 トークンは一度しか表示されないので、メモ帳などに保存しておきましょう。

---

## A.4　補足：GitHub CLI（gh）を使う場合

以下のように GitHub CLI（gh）を使うことで、トークン入力の手間が省けます：

```powershell
winget install GitHub.cli

# 初回ログイン
gh auth login
```

---

## まとめ

| 項目         | 方法           | 説明          |
| ---------- | ------------ | ----------- |
| GitHub 接続  | HTTPS + トークン | 現在の標準、安全で確実 |
| SSH 鍵      | 非推奨          | 一部の環境では制限あり |
| GitHub CLI | 推奨           | トークン認証を簡略化  |

---

Gitは習得すると一生モノのスキルです。まずは最低限の操作から始め、少しずつ応用を覚えていきましょう。
