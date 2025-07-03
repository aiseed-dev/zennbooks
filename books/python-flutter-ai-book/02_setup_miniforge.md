---
title: "第２章：開発環境の心臓部！MiniforgeでPython秘密基地を作ろう"
---

さあ、冒険の準備を始めましょう！Pythonを使うには、まずPCにそのための「秘密基地」を作る必要があります。私たちは**「Miniforge」**という、データサイエンスの世界で今一番人気の方法を選びます！🚀

**なぜMiniforgeなの？🤔**

*   **データ分析の達人**: データ分析に必要な便利な道具（ライブラリ）を、とても簡単に、しかも賢く管理してくれます。
*   **セットアップが超簡単**: 難しい設定は一切なし！インストーラに従うだけで、すぐに快適なPython環境が手に入ります。
*   **プロジェクトごとに部屋を分けられる**: プロジェクトごとに独立した「部屋」（仮想環境）を作ってくれるので、道具がごちゃ混ぜになりません。これでいつでも秘密基地はスッキリ整理！

### 1. Miniforgeをダウンロードしよう！ 🔽

*   [Miniforgeのダウンロードページ (GitHub)](https://github.com/conda-forge/miniforge/releases/latest) を開きます。
*   ページの中から、**「Miniforge3-Windows-x86_64.exe」**という名前のファイルを探してクリックし、ダウンロードします。

### 2. インストールしよう！ 魔法のセットアップ！ ✨

ダウンロードした `.exe` ファイルをダブルクリックして、インストールを開始します。

1.  `Welcome to Miniforge3` **Next**
2.  `License Agreement` **I Agree**
3.  `Installation Type` **Just Me** (推奨) を選んで **Next**
4.  `Choose Install Location` そのままでOK！ **Next**
5.  **`Advanced Installation Options` (ここが一番大事！)**
    *   ✅ **Add Miniforge3 to my PATH environment variable**
        *   **【重要！】** 「非推奨(Not recommended)」と書かれていますが、今回は学習を簡単にするため、**ここにチェックを入れてください！** これで、どこからでも`python`や`conda`という魔法の呪文が使えるようになります。
    *   ✅ **Register Miniforge3 as my default Python**
        *   こちらは最初からチェックが入っているはずです。そのままでOK！
    *   チェックを入れたら、**Install** をクリック！
6.  インストールが終わったら、**Next** **Finish** で完了です！

**本当にお疲れ様でした！**
これであなたのPCに、データサイエンスのための強力な秘密基地が完成しました！🎉 次は、この基地を最高の作業場にするための開発ツールを選びます。
