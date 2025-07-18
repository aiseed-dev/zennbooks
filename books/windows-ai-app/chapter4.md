---
title: 第4章　AIと作る！はじめての割り勘計算アプリ
---

この章では、AIメンターと対話しながら、シンプルだけど実用的な「割り勘計算アプリ」をFlutterで作成する流れを体験します。さっそく始めましょう！

#### ステップ1：アイデアをAIに相談して、固める

まずは、あなたの「ちょっとした不便」をAIに話してみることから始めます。

**【あなた（初心者）】**
友人との飲み会で、いつも割り勘の計算が面倒です。合計金額と人数を入れたら、パッと一人当たりの金額がわかる、ごくごく簡単なアプリが欲しいです。

---
**【AIメンター】**
「割り勘計算アプリ」、素晴らしいアイデアですね！日常で本当に役立ちますし、プログラミングの基本を学ぶのに最適なテーマです。

では、そのアプリの「設計図」を一緒に作りましょう。
まず、アプリに必要な部品（機能）を整理してみます。

1.  **入力する情報:**
    *   「合計金額」を入れるためのテキスト入力欄
    *   「参加した人数」を入れるためのテキスト入力欄

2.  **操作するもの:**
    *   「計算する！」と書かれたボタン

3.  **結果を表示する場所:**
    *   計算結果の「一人当たりの金額」を表示するテキスト

計算のロジックはシンプルに**「一人当たりの金額 = 合計金額 ÷ 人数」**ですね。
この設計図で、最初のバージョンを作ってみるのはいかがでしょうか？

---
**【あなた（初心者）】**
はい、そのシンプルな機能で大丈夫です！これをFlutterで作るには、どうすればいいですか？画面と、それを動かすためのコードを教えてください。

---

#### ステップ2：AIにFlutterコードを作ってもらう

設計図が決まったら、いよいよAIに具体的なコードの作成を依頼します。

**【AIメンター】**
承知いたしました！それでは、先ほどの設計図に基づいたFlutterのコードを作成します。

画面には、入力欄である`TextField`を２つ、`ElevatedButton`を１つ、そして結果を表示する`Text`を配置します。

以下のコードをコピーして、Flutterプロジェクトの `lib/main.dart` ファイルにそのまま貼り付けてみてください。すぐに動かすことができますよ。

---

### 【コピー＆ペーストで動く】割り勘計算アプリのFlutterコード

```dart
// Flutterの基本的なデザイン部品（ウィジェット）を使うためのおまじない
import 'package:flutter/material.dart';

// アプリを起動するメインの関数
void main() {
  runApp(const MyApp());
}

// アプリ全体の大枠を定義するクラス
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // アプリのタイトル
      title: '割り勘計算アプリ',
      // 見た目のテーマ設定
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      // 最初に表示する画面を指定
      home: const WariKanHomePage(),
    );
  }
}

// 割り勘アプリのホームページ画面を作るクラス
class WariKanHomePage extends StatefulWidget {
  const WariKanHomePage({super.key});

  @override
  State<WariKanHomePage> createState() => _WariKanHomePageState();
}

// 画面の状態を管理するクラス
class _WariKanHomePageState extends State<WariKanHomePage> {
  // 入力された文字を管理するためのコントローラー
  final TextEditingController _totalAmountController = TextEditingController();
  final TextEditingController _numberOfPeopleController = TextEditingController();

  // 計算結果を保存するための変数
  String _result = '';

  // 計算を実行する関数（メソッド）
  void _calculate() {
    // 入力された金額と人数を取得して、数値（double）に変換
    // もし入力が空なら0として扱う
    final double totalAmount = double.tryParse(_totalAmountController.text) ?? 0;
    final int numberOfPeople = int.tryParse(_numberOfPeopleController.text) ?? 0;

    // 状態を更新して画面を再描画する命令
    setState(() {
      if (totalAmount > 0 && numberOfPeople > 0) {
        // 割り勘計算を実行
        double resultPerPerson = totalAmount / numberOfPeople;
        // 計算結果を整数にして、文字列として保存
        _result = '一人当たり: ${resultPerPerson.ceil()} 円';
      } else {
        // 入力が正しくない場合
        _result = '金額と人数を正しく入力してください';
      }
    });
  }

  // 画面の見た目を組み立てるメインの部分
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // アプリ画面の上部のバー
      appBar: AppBar(
        title: const Text('かんたん割り勘計算'),
        backgroundColor: Colors.deepPurple[100],
      ),
      // 画面本体
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          // 子ウィジェットを縦に並べる
          children: <Widget>[
            // 合計金額の入力欄
            TextField(
              controller: _totalAmountController,
              decoration: const InputDecoration(
                labelText: '合計金額（円）',
                border: OutlineInputBorder(),
              ),
              // 数字キーボードを表示する設定
              keyboardType: TextInputType.number,
            ),
            // 少しスペースを空ける
            const SizedBox(height: 16),
            // 人数の入力欄
            TextField(
              controller: _numberOfPeopleController,
              decoration: const InputDecoration(
                labelText: '人数（人）',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.number,
            ),
            const SizedBox(height: 32),
            // 計算ボタン
            ElevatedButton(
              onPressed: _calculate, // ボタンが押されたら_calculate関数を実行
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
              ),
              child: const Text('計算する'),
            ),
            const SizedBox(height: 32),
            // 計算結果の表示
            Text(
              _result,
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }

  // 画面が閉じられる時にコントローラーを破棄するお掃除処理
  @override
  void dispose() {
    _totalAmountController.dispose();
    _numberOfPeopleController.dispose();
    super.dispose();
  }
}

```

#### 次のステップ（機能拡張のヒント）

このシンプルなアプリが動いたら、さらに便利な機能を追加してみましょう！

*   **機能案1：端数処理機能**
    *   「100円単位で切り上げ」のようなボタンを追加する。
*   **機能案2：立て替え払い機能**
    *   「Aさんが1万円先に払った」場合などを考慮できる入力欄を追加する。
*   **機能案3：デザインの改善**
    *   色や文字の大きさを変えて、自分好みの見た目にしてみる。

AIメンターに「端数処理機能を追加したいです。コードを教えてください」と相談すれば、きっと次のステップも助けてくれますよ。