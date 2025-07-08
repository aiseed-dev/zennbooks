---
title: 第三章：リストに命を吹き込む
---

`Gym`クラスという強力な武器を手に入れた美咲は、いよいよUI（ユーザーインターフェース）の構築に取り掛かった。目標はシンプル。JSONから読み込んだジムのリストを、アプリの画面に表示することだ。

しかし、ここでも新たな壁が立ちはだかった。JSONの読み込みは「非同期処理」――つまり、完了するまでに少し時間がかかる。その完了を待たずに画面を描画しようとすると、データがまだ空っぽなのでエラーになってしまう。

「うーん、データが読み込めたら画面を更新する、みたいなことがしたいんだけど…」

美咲は再びGeminiに問いかけた。

---

**美咲:**
「Gemini、また問題発生。`Gym`クラスのリストは作れるようになったんだけど、それを画面に表示しようとするとうまくいかないの。データの読み込みが終わるのを待ってからリストを表示するには、どういうウィジェットを使えばいい？」

> **Gemini:**
> 美咲さん、良いところに気づきましたね！それこそがFlutterの非同期UIプログラミングの核心部分です。そのための完璧なウィジェットがあります。その名も**`FutureBuilder`**です。

**美咲:**
「`FutureBuilder`…？未来を組み立てるって感じの名前だね。」

> **Gemini:**
> まさに！`FutureBuilder`は、「未来に完了する処理（`Future`）」を監視し、その状態に応じて表示する内容を切り替えてくれるウィジェットです。具体的には、
>
> 1.  **処理中（waiting）:** `CircularProgressIndicator`のようなローディング表示を見せる。
> 2.  **完了（done）:** 取得したデータを使って、本来表示したかったリストなどを見せる。
> 3.  **エラー発生（error）:** エラーメッセージを表示する。
>
> この3つの状態を自動で管理してくれるので、非同期処理を扱うUIがとてもシンプルに書けますよ。

**美咲:**
「すごい、それを使えば完璧にできそう！リスト表示には`ListView`を使えばいいんだよね？」

> **Gemini:**
> その通りです。特に、リストの項目が多い場合は**`ListView.builder`**を使うのがおすすめです。これは画面に表示されている部分だけを効率的に描画してくれるので、何百、何千というデータがあってもアプリがスムーズに動きます。
>
> `FutureBuilder`と`ListView.builder`を組み合わせた基本的なコードの骨格を生成してみましょうか？

**美咲:**
「お願い！まずはシンプルに、ジムの名前がずらっと並ぶだけでもいいから見てみたい！」

---

Geminiが生成したコードを元に、美咲は`main.dart`を書き換えていった。

```dart
// main.dart (UI構築の初期段階)

import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'dart:convert';
import 'models/gym.dart'; // 作成したGymクラスをインポート

void main() {
  runApp(const MyApp());
}

// Gymオブジェクトのリストを返す非同期関数
Future<List<Gym>> loadGyms() async {
  final String jsonString = await rootBundle.loadString('assets/gym_data_en.json');
  final List<dynamic> jsonList = json.decode(jsonString);
  // JSONのリストを、Gymオブジェクトのリストに変換する
  return jsonList.map((json) => Gym.fromJson(json)).toList();
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'ClimbFinder',
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ClimbFinder')),
      body: FutureBuilder<List<Gym>>(
        future: loadGyms(), // この非同期関数を監視
        builder: (context, snapshot) {
          // 状態1: 読み込み中
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          // 状態3: エラー発生、またはデータなし
          if (snapshot.hasError || !snapshot.hasData) {
            return const Center(child: Text('データの読み込みに失敗しました'));
          }
          
          // 状態2: 読み込み完了
          final gyms = snapshot.data!;

          // 「とりあえず名前だけでも…」と美咲が最初に作ったリスト
          return ListView.builder(
            itemCount: gyms.length,
            itemBuilder: (context, index) {
              final gym = gyms[index];
              return Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text(gym.name), // Gymオブジェクトから名前を取得
              );
            },
          );
        },
      ),
    );
  }
}
```

アプリを再起動すると、一瞬ローディングのくるくるが表示された後、画面にジムの名前が並んだだけの、そっけないリストが表示された。

だが、美咲にとっては魔法のように見えた。あのExcelの表が、自分の手で構造化され、型安全なオブジェクトとなり、そして今、アプリの画面に生まれ変わったのだ。

「すごい…できた！でも、これじゃあちょっと味気ないな。もっとクライミングアプリっぽく、おしゃれにしたい！」

彼女のデザイナー魂に火がついた。

---

**美咲:**
「Gemini、リストは表示できたよ！ありがとう！ここからもっと見栄えを良くしたいんだ。例えば、各項目をカードみたいにして、ジムの都道府県も一緒に表示したい。あと、クライミングジムだから、岩とか自然をイメージした色使いにしたいな。」

> **Gemini:**
> 素晴らしいアイデアです！UIデザインはアプリの魂ですからね。
>
> *   **カード化:** 各項目を`Card`ウィジェットで囲むと、影がついて立体感が出ます。
> *   **情報追加:** `Text`だけではなく、タイトルとサブタイトルを持つ`ListTile`ウィジェットを使うと、ジム名と都道府県を綺麗に配置できます。
> *   **配色:** テーマカラーとして、落ち着いた茶色（`Colors.brown`）や緑色（`Colors.green`）などのアースカラーを使うと、クライミングの雰囲気にマッチしますね。
>
> さらに、仲間たちが気にしていた「駐車場の有無」もアイコンで表現したら一目で分かって便利じゃないですか？

**美咲:**
「それ最高！『有』なら緑のチェック、『無』なら赤のバツ印とかで表示したい！」

> **Gemini:**
> いいですね！では、それらのアイデアを盛り込んだ、洗練されたリスト項目のコードを生成します。

---

Geminiの提案を元に、美咲は`ListView.builder`の中身を夢中で書き換えていった。

```dart
// ... (HomeScreenのbuildメソッド内)

// 洗練されたリスト表示
return ListView.builder(
  itemCount: gyms.length,
  itemBuilder: (context, index) {
    final gym = gyms[index];
    
    // 駐車場の有無に応じてアイコンと色を決定する
    Icon? parkingIcon;
    if (gym.hasParking == '有') {
      parkingIcon = const Icon(Icons.check_circle, color: Colors.green);
    } else if (gym.hasParking == '無') {
      parkingIcon = const Icon(Icons.cancel, color: Colors.red);
    }

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      elevation: 3, // カードの影
      child: ListTile(
        contentPadding: const EdgeInsets.all(16.0),
        title: Text(
          gym.name,
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        subtitle: Text(gym.prefecture ?? '情報なし'),
        trailing: parkingIcon, // 右端にアイコンを表示
      ),
    );
  },
);
```

アプリをリロードすると、画面は一変した。
ただの文字列の羅列だったリストが、一枚一枚独立したカードになり、ジム名と都道府県が美しくレイアウトされている。そして、右端には駐車場の有無を示す緑や赤のアイコンが輝いていた。

「わぁ…！これだよ、これ！私が作りたかったのは！」

静的なデータに、デザインという命が吹き込まれた瞬間だった。美咲は、完成に一歩近づいた自分のアプリを眺めながら、次の壁――詳細画面の作成へと想いを馳せるのだった。