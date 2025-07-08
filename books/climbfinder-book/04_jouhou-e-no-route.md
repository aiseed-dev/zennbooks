---
title: 第四章：情報へのルートを開く
---

ホーム画面のリストが美しくなったことで、美咲のモチベーションは最高潮に達していた。しかし、今のアプリはまだジムの名前と場所がわかるだけ。ユーザーが本当に知りたいのは、もっと詳しい情報のはずだ。

「よし、リストの項目をタップしたら、そのジムだけの詳しい情報が見れる画面を作ろう！」

彼女は早速、新しい画面（スクリーン）のファイルを作成し、`detail_screen.dart`と名付けた。しかし、すぐに新たな疑問が浮かぶ。

「ホーム画面でタップされたジムの情報を、どうやって詳細画面に渡せばいいんだろう？」

ただ画面を切り替えるだけでは、どのジムの詳細を表示すればいいのか分からない。この「画面間のデータ受け渡し」という新たな壁に、美咲はGeminiと共に挑むことにした。

---

**美咲:**
「Gemini、新しい画面を作ろうとしてるんだ。ホーム画面のリストで、例えば『NAC札幌クライミングジム』をタップしたら、そのジムの情報だけを表示する詳細画面に飛ばしたい。この『タップされたジムのデータ』を次の画面に渡すには、どうすればいいの？」

> **Gemini:**
> 美咲さん、それはアプリ開発における非常に重要なステップですね！画面遷移とデータ受け渡しはセットで考えます。Flutterでは、**コンストラクタ経由でデータを渡す**のが最もシンプルで安全な方法です。

**美咲:**
「コンストラクタ経由…？」

> **Gemini:**
> はい。まず、詳細画面のウィジェット（`DetailScreen`としましょう）に、表示したいデータ、つまり`Gym`オブジェクトを受け取るためのプロパティを定義します。そして、そのプロパティを必須の引数としてコンストラクタに設定します。
>
> ```dart
> // DetailScreenの定義（イメージ）
> class DetailScreen extends StatelessWidget {
>   final Gym gym; // この画面で表示するGymオブジェクト
>
>   // コンストラクタでGymオブジェクトを受け取る
>   const DetailScreen({super.key, required this.gym});
>
>   // ... buildメソッドで gym.name などを表示
> }
> ```
>
> こうすることで、`DetailScreen`を呼び出す側（ホーム画面）は、必ず`Gym`オブジェクトを渡さなければならなくなります。

**美咲:**
「なるほど！それで、ホーム画面からはどうやって呼び出すの？」

> **Gemini:**
> ホーム画面の`ListTile`には`onTap`というプロパティがあります。ユーザーがタイルをタップした時に実行されるコールバック関数です。ここで`Navigator.push`という命令を使い、新しい画面をスタックに積み上げるように表示します。その際に、先ほど設計した`DetailScreen`のコンストラクタに、タップされた`gym`オブジェクトを渡してあげるんです。
>
> ```dart
> // ListTileのonTapプロパティ（イメージ）
> onTap: () {
>   Navigator.push(
>     context,
>     MaterialPageRoute(
>       builder: (context) => DetailScreen(gym: gym), // ここでデータを渡す！
>     ),
>   );
> },
> ```

**美咲:**
「`Navigator.push`に`MaterialPageRoute`…！そういう風に繋がってるんだ！それならできそう。あと、詳細画面ではウェブサイトのURLをタップしたらブラウザで開けるようにしたいな。」

> **Gemini:**
> 素晴らしい機能ですね！そのためには`url_launcher`という非常に便利なパッケージがあります。これを`pubspec.yaml`に追加すれば、数行のコードでURLを外部ブラウザで開けるようになりますよ。
>
> それでは、これらの要素をすべて盛り込んだ`DetailScreen`のコードを生成しましょう。美咲さんのデザイナーセンスを活かして、情報をセクションごとに見やすく整理するレイアウトにしてみますね。

---

Geminiが生成したコードを参考に、美咲は`detail_screen.dart`を夢中で作り上げた。そして、`url_launcher`パッケージを`pubspec.yaml`に追加するのも忘れなかった。

```yaml
# pubspec.yaml
dependencies:
  flutter:
    sdk: flutter
  # URLを開くためのパッケージを追加
  url_launcher: ^6.1.14 # バージョンは適宜最新のものに
```

#### **`lib/screens/detail_screen.dart` (詳細画面)**

```dart
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/gym.dart';

class DetailScreen extends StatelessWidget {
  final Gym gym;

  const DetailScreen({super.key, required this.gym});

  // URLをブラウザで開くための非同期関数
  Future<void> _launchURL(String? urlString) async {
    if (urlString == null || urlString.isEmpty) return;

    final Uri url = Uri.parse(urlString);
    if (!await launchUrl(url, mode: LaunchMode.externalApplication)) {
      // 実際にはSnackBarなどでユーザーにエラーを通知するのが親切
      print('Could not launch $url');
    }
  }

  // 見出し用の共通ウィジェット
  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(top: 24.0, bottom: 8.0),
      child: Text(
        title,
        style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.brown),
      ),
    );
  }

  // 情報行用の共通ウィジェット
  Widget _buildInfoRow(IconData icon, String? text) {
    if (text == null || text.isEmpty) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: Colors.grey[600], size: 20),
          const SizedBox(width: 16),
          Expanded(child: Text(text, style: const TextStyle(fontSize: 16))),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(gym.name),
        backgroundColor: Colors.brown,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 基本情報セクション
            _buildSectionTitle('基本情報'),
            _buildInfoRow(Icons.location_on, gym.address),
            _buildInfoRow(Icons.directions_car, gym.access),
            _buildInfoRow(Icons.phone, gym.phoneNumber),

            // ウェブサイト（タップ可能）
            if (gym.website != null && gym.website!.isNotEmpty)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4.0),
                child: InkWell(
                  onTap: () => _launchURL(gym.website),
                  child: Row(
                    children: [
                      Icon(Icons.link, color: Colors.blue[700]),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Text(
                          '公式サイトを見る',
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.blue[700],
                            decoration: TextDecoration.underline,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),

            // 設備情報セクション
            _buildSectionTitle('設備'),
            _buildInfoRow(Icons.aspect_ratio, '壁の高さ: ${gym.wallHeight?.toString() ?? '情報なし'} m'),
            _buildInfoRow(Icons.fullscreen, '壁面積: ${gym.wallArea?.toString() ?? '情報なし'} ㎡'),
            _buildInfoRow(Icons.local_parking, '駐車場: ${gym.hasParking ?? '情報なし'}'),
            _buildInfoRow(Icons.shower, 'シャワー: ${gym.hasShower ?? '情報なし'}'),
            _buildInfoRow(Icons.store, 'ショップ: ${gym.hasShop ?? '情報なし'}'),
            
            // 備考セクション
            if (gym.notes != null && gym.notes!.isNotEmpty) ...[
              _buildSectionTitle('備考'),
              Text(gym.notes!, style: const TextStyle(fontSize: 16, height: 1.5)),
            ]
          ],
        ),
      ),
    );
  }
}
```

最後に、ホーム画面の`ListTile`に`onTap`処理を追加した。

```dart
// home_screen.dart の ListTile
// ...
child: ListTile(
  // ... (title, subtitle, trailing)
  onTap: () {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => DetailScreen(gym: gym),
      ),
    );
  },
),
//...
```

美咲は息を飲んでアプリを再起動した。美しく並んだジムのリストから、一番上の「NAC札幌クライミングジム」をタップする。すると、画面がスッと切り替わり、札幌のジムの詳細情報が整然と表示された。

「すごい…！」

住所、アクセス、電話番号。そして青い下線のついた「公式サイトを見る」というテキストをタップすると、見慣れたスマートフォンのブラウザが起動し、NACの公式サイトが表示された。

静的なJSONファイルから始まったデータが、今やインタラクティブな情報へと進化した。ユーザーはただ眺めるだけでなく、「タップする」というアクションで自ら情報へのルートを切り開くことができる。美咲は、自分のアプリがまた一つ、大きな成長を遂げたことを実感していた。