---
title: "第15章：Flutterの心臓部！「ウィジェット」でUIを組み立てよう"
---

前の章で、あなたは最初のFlutterアプリを動かし、ホットリロードの魔法を体験しました。素晴らしかったですね！この章では、FlutterのUIが**どのように作られているのか**、その秘密の核心に迫ります。

Flutterの世界では、画面に表示されるすべてのもの、例えばテキスト、ボタン、画像、さらにはレイアウトの配置方法まで、**すべてが「ウィジェット（Widget）」**という部品でできています。

ウィジェットは、まるで**レゴブロック**のようなもの。様々な形や色のブロックを自由に組み合わせることで、想像した通りの作品（＝アプリの画面）を作り上げることができるのです！この章では、基本的なブロックの使い方をマスターしましょう！🧩

### 1. すべてはウィジェットの「ツリー構造」

Flutterの画面は、ウィジェットが入れ子になった「ツリー（木）」のような構造をしています。

```
Scaffold (画面全体の骨格)
 └─ AppBar (画面上部のバー)
 │   └─ Text('アプリのタイトル')
 └─ Center (中央に配置するウィジェット)
     └─ Column (縦にウィジェットを並べる)
         ├─ Text('こんにちは！')
         └─ ElevatedButton(押せるボタン)
```

このように、大きなウィジェットの中に小さなウィジェットを配置していくことで、複雑なレイアウトもシンプルに表現できます。

### 2. 最も基本的なウィジェットたち（最初のレゴブロックセット）

まずは、どんなアプリでも使う、最も基本的で重要なウィジェットをいくつか紹介します。

| ウィジェット名 | 役割（どんなレゴブロック？） |
| :--- | :--- |
| `Text` | **文字ブロック**: 文字を表示するための基本ブロック。 |
| `Icon` | **絵柄ブロック**: アイコンを表示します。 |
| `Image` | **写真ブロック**: 画像ファイルやネット上の画像を表示します。 |
| `Container` | **万能ブロック**: 色を付けたり、サイズを指定したり、枠線を付けたりできる透明な箱。装飾の基本です。 |
| `Center` | **中央寄せブロック**: 中に入れたウィジェットを画面の中央に配置します。 |
| `Row` | **横並びブロック**: 中に入れたウィジェットたちを、水平方向（横）に並べます。 |
| `Column` | **縦並びブロック**: 中に入れたウィジェットたちを、垂直方向（縦）に並べます。 |
| `ElevatedButton` | **立体ボタンブロック**: ユーザーが押せる、影付きのボタンです。 |

### 3. 実践！ウィジェットを組み合わせてみよう！

それでは、`lib/main.dart` の中身を一度まっさらにして、これらのウィジェットを使って簡単な自己紹介画面を作ってみましょう！

**【準備】`lib/main.dart` を書き換える**

`main.dart` の中身をすべて削除し、以下のシンプルな骨格コードに貼り替えてください。`home:` の部分に、これからウィジェットを組み立てていきます。

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold( // ここからが画面の中身
        backgroundColor: Colors.teal, // 背景色
        body: SafeArea( // スマホの表示が崩れないようにするおまじない
          child: Center( // この中にウィジェットを組み立てる！
            // TODO: ここに自己紹介カードを作る
          ),
        ),
      ),
    );
  }
}
```

**【組み立て開始！】**

上記コードの `// TODO:` の部分を、以下の `Column` ウィジェットに置き換えてみてください。

```dart
// ... 前略
child: Center(
  child: Column(
    mainAxisAlignment: MainAxisAlignment.center, // Columnの中身を中央寄せ
    children: <Widget[
      CircleAvatar( // 丸いアバター画像
        radius: 50.0,
        backgroundImage: NetworkImage('https://via.placeholder.com/150'), // ダミー画像
      ),
      Text(
        'あなたの名前',
        style: TextStyle(
          fontFamily: 'Pacifico', // (注)別途フォント設定が必要
          fontSize: 40.0,
          color: Colors.white,
          fontWeight: FontWeight.bold,
        ),
      ),
      Text(
        'FLUTTER DEVELOPER',
        style: TextStyle(
          fontFamily: 'Source Sans Pro', // (注)別途フォント設定が必要
          color: Colors.teal.shade100,
          fontSize: 20.0,
          letterSpacing: 2.5,
          fontWeight: FontWeight.bold,
        ),
      ),
      Card( // カード型のウィジェット
        margin: EdgeInsets.symmetric(vertical: 10.0, horizontal: 25.0),
        child: ListTile(
          leading: Icon(
            Icons.phone,
            color: Colors.teal,
          ),
          title: Text(
            '+81 90 1234 5678',
            style: TextStyle(
              color: Colors.teal.shade900,
              fontSize: 20.0,
            ),
          ),
        ),
      ),
      Card(
        margin: EdgeInsets.symmetric(vertical: 10.0, horizontal: 25.0),
        child: ListTile(
          leading: Icon(
            Icons.email,
            color: Colors.teal,
          ),
          title: Text(
            'youremail@example.com',
            style: TextStyle(
              fontSize: 20.0,
              color: Colors.teal.shade900,
            ),
          ),
        ),
      )
    ],
  ),
),
// ... 後略
```

コードを貼り替えたら、ホットリロード（⚡）してみてください。どうですか？あっという間に、ちょっとおしゃれな自己紹介カードが表示されたのではないでしょうか？

---

**おめでとうございます！あなたはウィジェットを組み立てる基本をマスターしました！**

このように、Flutterでは小さなウィジェットを組み合わせて、大きな部品（`Card`の中に`ListTile`、その中に`Icon`と`Text`）を作り、さらにそれらを `Column` で縦に並べる…という風にUIを構築していきます。

最初はたくさんのウィジェットがあって戸惑うかもしれませんが、大丈夫。基本的なものをいくつか覚えれば、あとはAIに「〇〇みたいなUIを作りたい」と相談すれば、どんなウィジェットを使えばいいか教えてくれますよ！

次の章では、いよいよ最終目標である「ジム検索アプリ」の開発に着手します！Pythonで作ったデータを、Flutterで表示する、二つの世界が繋がる瞬間を体験しましょう！
