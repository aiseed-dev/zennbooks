---
title: "第二章：デジタルの壁との格闘"
---

#### **第二章：デジタルの壁との格闘**

美咲のアパートの一室が、彼女の開発基地になった。`flutter create climb_finder`というコマンドを打ち込むと、パソコンの画面に新しいプロジェクトの骨格が生成される。胸が高鳴った。

最初の壁は、`gym_data_en.json`ファイルをアプリに読み込むことだった。しかし、実行すると画面は真っ赤なエラーで埋め尽くされる。`Asset not found`…。夜が更け、冷めたコーヒーのマグカップだけが増えていく。

「どうして…？パスは合ってるはずなのに」

彼女は、JSONファイルを読み込むためのコードと、プロジェクトのフォルダ構成を何度も見比べた。

```dart
// main.dart (試行錯誤中のコード)
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

// データを読み込むテスト用の関数
Future<void> loadGyms() async {
  // このパスは正しいはず…なのにどうして？
  final String jsonString = await rootBundle.loadString('assets/gym_data_en.json');
  final data = json.decode(jsonString);
  print(data);
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // 画面が表示される前にデータを読み込もうとしていた
    loadGyms();
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('ClimbFinder')),
        body: const Center(child: Text('データ読み込み中...')),
      ),
    );
  }
}
```

諦めかけたその時、ふとチュートリアル動画の記憶が蘇った。アセットファイルは、使う前に「使うよ」と宣言する必要があることを思い出したのだ。彼女は急いで`pubspec.yaml`ファイルを開いた。

```yaml
# pubspec.yaml

flutter:
  uses-material-design: true

  # 「あっ、ここだ…！」
  # 美咲はアセットの登録を忘れていたことに気づいた。
  # 慌てて以下の2行を書き加える。
  assets:
    - assets/gym_data_en.json
```

設定ファイルへの登録漏れという、たった2行の記述ミス。それを修正して再度実行すると、今度はコンソールに、見慣れたJSONの文字列がずらりと表示された。

```
[{id: 1, region: 北海道, prefecture: 北海道, city: 札幌市白石区, ...}, {id: 2, ...}]
```

「…動いた！」

それは、クライミングで何度もトライして、ようやくゴールホールドに指がかかった時のような、震えるほどの喜びだった。

次に、この無機質な文字列を、アプリで安全に扱える意味のあるデータに変換する必要があった。美咲はJSONの構造に合わせて、Dartで`Gym`クラスを設計する。`website`や`has_parking`など、データが`null`になる可能性がある項目には慎重に`?`をつけ、どんなデータでもアプリがクラッシュしないようにした。その作業は、新しいルートのホールドを一つずつ確認していく「オブザベーション」のようだった。

```dart
// lib/models/gym.dart (新しく作成したファイル)

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
  // 「このfromJsonという仕組みがあれば、JSONのキーとクラスのプロパティを
  //   一つずつ、間違いなく紐付けられるんだ」と美咲は理解した。
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
