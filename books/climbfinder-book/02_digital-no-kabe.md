---
title: 第二章：デジタルの壁との格闘
---

美咲のアパートの一室が、彼女の開発基地になった。`flutter create climb_finder`というコマンドを打ち込むと、パソコンの画面に新しいプロジェクトの骨格が生成される。胸が高鳴った。

最初の壁は、第一章で作成した`gym_data_en.json`ファイルをアプリに読み込むことだった。早速コードを書き、実行してみる。しかし、期待とは裏腹に、画面は真っ赤なエラーメッセージで埋め尽くされた。`Asset not found`…。

夜が更け、冷めたコーヒーのマグカップだけが増えていく。

「どうして…？パスは合ってるはずなのに。`assets`フォルダも作ったし、その中に`gym_data_en.json`も入れた。完璧なはずなのに…」

途方に暮れた美咲は、すがるようにGeminiに助けを求めた。

---

**美咲:**
「Gemini、助けて！`rootBundle.loadString`でJSONを読み込もうとしてるんだけど、`Asset not found`っていうエラーがどうしても消えないんだ。これがその時のコードなんだけど…。」

```dart
// main.dart (試行錯誤中のコード)
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'dart:convert';

// ...

Future<void> loadGyms() async {
  // このパスは正しいはず…なのにどうして？
  final String jsonString = await rootBundle.loadString('assets/gym_data_en.json');
  final data = json.decode(jsonString);
  print(data);
}

// ...
```

> **Gemini:**
> こんにちは、美咲さん。そのエラーメッセージ、胸が痛みますね。でも安心してください、これはFlutter開発者が一度は必ず登る壁のようなものです。
>
> コードを見せてくれてありがとう。`loadString`の使い方は完璧ですよ。問題はコードの中ではなく、**プロジェクトの設定**にある可能性が非常に高いです。Flutterでは、画像やフォント、JSONファイルなどの「アセット」を使う場合、事前に『このファイルを使いますよ』とプロジェクトに宣言してあげる必要があります。

**美咲:**
「宣言…？そんなのが必要だったんだ。」

> **Gemini:**
> はい。その宣言を行うのが `pubspec.yaml` というファイルです。プロジェクトのルートディレクトリにあるはずです。そのファイルを開いて、`flutter:`というセクションの中を探してみてください。`# assets:` のようにコメントアウトされている箇所がありませんか？

美咲は言われた通りに`pubspec.yaml`ファイルを開いた。すると、Geminiの言う通りの箇所を見つけた。

```yaml
# pubspec.yaml

flutter:
  uses-material-design: true

  # To add assets to your application, add an assets section, like this:
  # assets:
  #   - images/a_dot_burr.jpeg
  #   - images/a_dot_ham.jpeg
```

**美咲:**
「あっ、これだ…！ずっとコメントアウトされたままだった！」

> **Gemini:**
> ビンゴです！そのコメントアウトを解除して、`gym_data_en.json`のパスを登録しましょう。インデント（字下げ）がとても重要なので、`uses-material-design: true` と同じレベルに `assets:` が来るように調整してください。

美咲は急いでファイルを修正した。

```yaml
# pubspec.yaml

flutter:
  uses-material-design: true

  # 美咲はGeminiに教えられた通り、慌てて以下の2行を書き加えた。
  assets:
    - assets/gym_data_en.json
```

たった2行の修正。祈るような気持ちで再度アプリを実行すると、今度はコンソールに、見慣れたJSONの文字列がずらりと表示された。

```
[{id: 1, region: 北海道, prefecture: 北海道, city: 札幌市白石区, ...}, {id: 2, ...}]
```

「…動いた！」

それは、クライミングで何度もトライして、ようやくゴールホールドに指がかかった時のような、震えるほどの喜びだった。

---

**美咲:**
「Gemini、ありがとう！本当に動いたよ！でも、このデータってまだただの文字列の集まりだよね。アプリの中で安全に、そして便利に扱うにはどうしたらいいんだろう？例えば`name`って打つつもりで`namae`ってタイプミスしても気づけなさそう…。」

> **Gemini:**
> 素晴らしい着眼点です！まさにその通りで、それが次のステップです。
> 生のJSON（技術的には`Map<String, dynamic>`）をそのまま使うと、今おっしゃったようなタイプミスによるバグが発見しにくくなります。そこで、このJSONの構造に合わせた**Dartのクラス（データモデル）**を作成します。
>
> そうすることで、例えば `gym.name` のようにプロパティにアクセスでき、もし `gym.namae` と間違えれば、プログラムを実行する前にエディタが「そんなプロパティはありません」と教えてくれます。これを**「型安全」**と言います。

**美咲:**
「型安全、なるほど！でも、JSONには値が入っていない`null`の項目もあるよね。`wall_area`とか。そういうのはどうすれば？」

> **Gemini:**
> そこがDartの**「Null安全」**機能の出番です。値が`null`になる可能性があるプロパティは、`String?`や`double?`のように、型の後ろにクエスチョンマーク `?` を付けて定義します。これは「この変数は`null`かもしれないから、扱う時は気をつけてね」というコンパイラへの合図になります。
>
> さらに、JSONデータからこのクラスのオブジェクトを生成するための、`fromJson`という名前の**ファクトリコンストラクタ**を定義するのが一般的です。
>
> この`Gym`クラス、一緒に設計してみましょうか？

**美咲:**
「ぜひお願い！`fromJson`ってすごく便利そう！」

> **Gemini:**
> 承知しました。美咲さんが作った`gym_data_en.json`の構造とNull安全を考慮して、以下のような`Gym`クラスを生成しました。

```dart
// lib/models/gym.dart (新しく作成するファイル)

// JSONの構造をDartのクラスとして定義する。
// これで型安全にデータにアクセスできるようになり、typoなどのミスを防げる。
class Gym {
  final int id;
  final String name;
  final String? region;
  final String? prefecture;
  final String? city;
  final String? address;
  final String? access;
  final String? website;
  final String? phoneNumber;
  final double? wallArea;
  final double? wallHeight;
  final String? hasParking;
  final String? hasShower;
  final String? hasShop;
  final String? notes;

  // コンストラクタ
  Gym({
    required this.id,
    required this.name,
    this.region,
    this.prefecture,
    this.city,
    this.address,
    this.access,
    this.website,
    this.phoneNumber,
    this.wallArea,
    this.wallHeight,
    this.hasParking,
    this.hasShower,
    this.hasShop,
    this.notes,
  });

  // JSONのMap<String, dynamic>からGymオブジェクトを生成するファクトリコンストラクタ。
  // Geminiが「これがあれば変換ロジックを綺麗にまとめられます」と教えてくれた仕組み。
  factory Gym.fromJson(Map<String, dynamic> json) {
    return Gym(
      id: json['id'],
      name: json['name'] ?? '名前不明', // nameは必須なので、万が一nullならデフォルト値を入れる
      region: json['region'],
      prefecture: json['prefecture'],
      city: json['city'],
      address: json['address'],
      access: json['access'],
      website: json['website'],
      phoneNumber: json['phone_number'],
      // JSONの数値はintかもしれないので、安全にdouble?型に変換
      wallArea: (json['wall_area'] as num?)?.toDouble(), 
      wallHeight: (json['wall_height'] as num?)?.toDouble(),
      hasParking: json['has_parking'],
      hasShower: json['has_shower'],
      hasShop: json['has_shop'],
      notes: json['notes'],
    );
  }
}
```

美咲は、生成されたコードを自分のプロジェクトに組み込んだ。それはまるで、新しいルートのホールドを一つずつ確認していく「オブザベーション」のようだった。無機質なデータが、意味のある「Gym」というオブジェクトになる。デジタルの壁を一つ乗り越え、彼女のアプリは確かな命を宿し始めていた。