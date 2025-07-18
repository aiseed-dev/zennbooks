---
title: 第2章　開発環境の基本（Windowsユーザー向け）
---

――「動かす準備」で迷わないために

アプリ開発を始めるには、まず「動かせる状態」を整えることが大切です。
この章では、開発の舞台となる「フォルダ」「パス」「ターミナル」などの基本から、実際にアプリを動かすためのソフトウェアの導入まで、順を追って説明します。

---

## 2.1　開発の土台を知ろう ―― フォルダ・パス・ターミナル

### フォルダ（ディレクトリ）構成の考え方

Flutterでは、プロジェクトの自動生成で多くのファイルが一気に作られるため、**専用の作業構成を先に用意しておくことが大切**です。

おすすめの構成は以下のような「3段階構成」です：

```text
C:\dev\myproject\myapp
```

* `C:\dev\` : すべての開発作業をまとめるためのトップフォルダ（自由に名前をつけてOK）
* `myproject` : プロジェクト単位のフォルダ（例：アルバムアプリ、旅行アプリなど）
* `myapp` : Flutterで作るアプリ本体（`flutter create myapp` で作成）

この構成にすることで：

* 将来的に複数のアプリや関連ファイルをプロジェクト単位で管理できる
* Gitで管理する際にもフォルダ全体をバージョン管理できる
* `flutter create` で生成されるファイルが整理された場所に収まる

> ✅ 初心者ほど、「**とりあえず `C:\dev\myproject\myapp` にする**」と決め打ちして始めた方が、あとあと困りません。

### ターミナルの基本 ― PowerShell を使う理由

開発では、**PowerShell** を使って作業するのが基本です。
今後、Flutterコマンド、Git、ライブラリ管理など、すべてPowerShellから行います。

```powershell
cd C:\dev\myproject
flutter create myapp
```

のように、すべての操作をPowerShellで完結させましょう。

---

## 2.2　PowerShell を WinGet でアップグレードしよう

はい、ご提示いただいた内容について確認しました。全体として正しい情報ですが、より正確で、初心者の方にとって親切な記述にするために、いくつか補足と修正案を提案します。

### 指摘事項と修正案

ご提示のコマンドには、現在（2025年7月時点）ではより推奨される書き方があります。また、初心者の方が混乱しないための補足情報を加えることをお勧めします。

#### **1. コマンドについて**

提示されたコマンド`winget install --id Microsoft.PowerShell --source winget`でもインストールは可能ですが、現在では `--id` のエイリアス（別名）である `install` の後に直接IDを書く、よりシンプルな構文が一般的です。

*   **修正案:**
    ```powershell
    winget install Microsoft.PowerShell
    ```
    または、最新版であることを明示したい場合はプレビュー版を含まない安定版の最新を指すために以下のように記述することもできます。
    ```powershell
    winget install --id Microsoft.PowerShell --source winget
    ```
    ただ、一般的には `winget install Microsoft.PowerShell` で安定版の最新がインストールされるため、こちらの方がシンプルで分かりやすいでしょう。

#### **2. PowerShell 7の起動コマンドについて**

インストール後に `pwsh` と入力して起動する、という点はその通りです。しかし、なぜ `powershell` ではなく `pwsh` なのか、という点を補足すると、より丁寧な説明になります。

*   **補足情報の提案:**
    Windowsに標準でインストールされている「Windows PowerShell 5.1」の実行ファイル名は `powershell.exe` です。一方で、新しくインストールする「PowerShell 7」の実行ファイル名は `pwsh.exe` となっています。これにより、古いバージョンと新しいバージョンが共存できるようになっています。

#### **3. Windows Terminalへの統合について**

「`Windows Terminal` に新しいPowerShell7を統合することもおすすめです」という記述は非常に良い提案です。この手順をもう少し具体的に示すと、初心者の方が迷わず設定できます。

*   **具体的な手順の提案:**
    通常、PowerShell 7をインストールすると、次回のWindows Terminal起動時に自動的にプロファイルが追加されます。もし自動で追加されない場合でも、Windows Terminalの「設定」画面から簡単に追加できます。
    1.  Windows Terminalを開き、タブの隣にある「▼」をクリックし、「設定」を選択します。
    2.  左側のメニューで「プロファイルを追加する」を選択します。
    3.  既存のプロファイル一覧に「PowerShell」という名前（アイコンが黒色）があれば、それがPowerShell 7です。もしなければ、「新しいプロファイルを追加」から手動で設定できます。コマンドラインには `pwsh.exe` を指定します。

### 修正後の記述例

以上の点を踏まえて、修正後の記述例を以下に示します。

---

## 2.2 PowerShell を WinGet でアップグレードしよう

古いPowerShellのままでは、Flutter開発などで予期せぬ問題が発生することがあります。Windows Package Manager (winget) を使って、最新の **PowerShell 7** をインストールしましょう。

以下のコマンドを現在のPowerShell（またはコマンドプロンプト）で実行してください。

```powershell
winget install Microsoft.PowerShell
```

インストールが完了したら、ターミナルを再起動し、`pwsh` と入力してEnterキーを押してください。以下のようにバージョン情報が表示されれば、新しいPowerShell 7が正常に起動しています。

```
PowerShell 7.x.x
...
```

> **補足：なぜ `pwsh` なの？**  
> Windowsに標準搭載されている古いPowerShell (バージョン5.1) の実行ファイル名は `powershell.exe` です。新しくインストールしたPowerShell 7は `pwsh.exe` という別の名前になっており、これにより2つのバージョンが共存できます。

> 📌 **おすすめ: Windows Terminal起動時にPowerShell7を立ち上げる設定**  
具体的な手順:
1. Windows Terminalの上のバーの「+」の隣にある「ｖ」をクリックし、「設定」を選択します。
2. 既定のプロファイルを変更する:  
設定画面の左側メニューから「スタートアップ」（または「全般」）を選択します。
「既定のプロファイル」という項目があります。ここが現在、Windows Terminalを起動したときに最初に開くシェルになっています。
このドロップダウンメニューをクリックし、一覧から「PowerShell」（黒いアイコンの方）を選択します。
3. もし、「PowerShell」（黒いアイコンの方）がなければ、左側のメニューで「プロファイルを追加する」を選択します。「新しいプロファイルを追加」から手動で設定できます。コマンドラインには pwsh.exe を指定します。その後、既定のプロフィルを変更します。
---

## 2.3　開発用フォルダーを作ろう

PowerShell を使って、開発用のディレクトリ構造を作ってみましょう。

```powershell
cd C:\
mkdir dev
cd dev
mkdir myproject
```

フォルダーができているかどうかエクスプローラで確認してみてください。
この作業で、`C:\dev\myproject` という開発プロジェクトがが完成します。

---

## 2.4　Git のインストールと基本（WinGet + CLI）

### Gitのインストール（WinGet）

以下のコマンドでGitをインストールします：

```powershell
winget install --id Git.Git -e
```

### Gitが使えるか確認

```powershell
git --version
```

バージョン情報が表示されればOKです。

### 最初の設定

```powershell
git config --global user.name "あなたの名前"
git config --global user.email "あなたのメールアドレス"
```

### Gitの基本的な使い方

```powershell
cd C:\dev\myproject

git init       # Gitリポジトリを初期化

echo "# My App" > README.md
git add .       # すべてのファイルを追加
git commit -m "最初のコミット"
```

このように、コマンドで操作することで、Gitの動作がよく理解できるようになります。

---

## 2.5　Flutterアプリを動かす準備（Android Studio は必要）

Flutterでスマホアプリを動かすには、\*\*Androidの仮想スマホ（エミュレータ）\*\*が必要です。
そのために、**Android Studio をインストールする必要があります**。

### なぜ Android Studio が必要？
* Android SDK が含まれているため
* エミュレータ（仮想デバイス）を作成・起動するため

> ⚠ Android Studio は非常に重いソフトです。  
> エミュレータ用の仮想端末は一つだけ作成します。
> インストールは、最小限にします。

---

## 2.6　Windowsデスクトップアプリには Visual Studio が必要

Flutterでは、**Windows用のアプリも作れます**。
ただし、**Windowsアプリをビルド・実行するには Visual Studio が必要**です。

### 必要なもの：

* Visual Studio（**Visual Studio Codeではない**）
* C++によるデスクトップ開発 ワークロード

> ⚠ Visual Studio も Android Studioと同様に重たいソフトです。
> 最初からインストールするのではなく、必要になったときに導入しましょう。


---

## まとめ

| ソフト名            | 役割           | 今すぐ必要？ | 重さ |
| --------------- | ------------ | ------ | -- |
| PowerShell (最新) | ターミナル        | ✅ 必須   | 軽い |
| Git             | バージョン管理      | ✅ 必須   | 軽い |
| Android Studio  | スマホエミュレータ    | ⏳ 後で必要 | 重い |
| Visual Studio   | Windowsアプリ開発 | ⏳ 後で必要 | 重い |

次章では、実際にこれらのツールを使って、最初の開発環境を整えていきます。
