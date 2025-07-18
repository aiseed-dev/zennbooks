---
title: 第5章　AIと作る！はじめての京都観光アプリ
---

この章では、AIメンターとの対話を通じて、あなたの次の旅行で役立つかもしれない「京都観光アプリ」の第一歩を作成します。自分の興味を形にする楽しさを体験しましょう！

#### ステップ1：AIに旅の相談をして、アプリの「素材」を手に入れる

まずは、あなたが興味のあることをAIに尋ねてみましょう。今回は「京都旅行」がテーマです。

**【あなた（初心者）】**
来月、京都に遊びに行きます。有名どころを巡りたいのですが、おすすめの観光地をいくつか教えてください。

---
**【AIメンター】**
京都旅行、素敵ですね！それでは、初心者の方でも楽しめる、京都の魅力が詰まった王道の観光地をいくつかピックアップしますね。

*   **金閣寺（鹿苑寺）:** 鏡湖池に映る金色の舎利殿があまりにも有名なお寺です。
*   **清水寺:** 「清水の舞台」で知られ、京都市内を一望できる絶景が楽しめます。
*   **伏見稲荷大社:** 朱色の鳥居がトンネルのように続く「千本鳥居」は圧巻の光景です。
*   **嵐山 竹林の道:** 天高く伸びる竹林の中を歩くと、まるで別世界にいるような気分になります。

このあたりの情報を、いつでもスマホで見返せたら便利だと思いませんか？

---
**【あなた（初心者）】**
はい、すごく便利だと思います！この情報を元に、自分だけの簡単な観光アプリを作ってみたいです。どうすればFlutterで形にできますか？

---

#### ステップ2：AIにFlutterコードを作ってもらう

旅のプランという「素材」が集まったら、それを表示するアプリのコードをAIに作ってもらいましょう。

**【AIメンター】**
素晴らしいアイデアです！では、先ほどの観光地リストを表示するためのFlutterアプリのコードを作成します。

このアプリは2つの画面で構成されます。
1.  **一覧画面:** おすすめの観光地名がリストで表示されます。
2.  **詳細画面:** リストの項目をタップすると、その場所の詳しい説明と写真が表示されます。

以下のコードをコピーして、Flutterプロジェクトの `lib/main.dart` ファイルにそのまま貼り付けてみてください。あなただけの京都観光アプリが動き出しますよ。

---

### 【コピー＆ペーストで動く】京都観光アプリのFlutterコード

```dart
// Flutterの基本的なデザイン部品（ウィジェット）を使うためのおまじない
import 'package:flutter/material.dart';

// --- アプリのデータ部分 ---
// 観光地一つの情報をまとめるための設計図（クラス）
class Spot {
  final String name; // 名前
  final String description; // 説明文
  final String imageUrl; // 写真のURL

  const Spot({
    required this.name,
    required this.description,
    required this.imageUrl,
  });
}

// アプリで表示する観光地のリストデータ
// （AIに教えてもらった情報をここにまとめる）
const List<Spot> kyotoSpots = [
  Spot(
    name: '金閣寺（鹿苑寺）',
    description: '鏡湖池に映る金色の舎利殿があまりにも有名。室町幕府の三代将軍、足利義満によって建てられました。雪化粧の季節は特に息をのむ美しさです。',
    imageUrl: 'https://images.unsplash.com/photo-1503640538573-148065ba4904',
  ),
  Spot(
    name: '清水寺',
    description: '「清水の舞台から飛び降りる」の語源となった本堂の舞台で知られる寺院。音羽の滝や三重塔など見どころが多く、桜や紅葉の名所としても人気です。',
    imageUrl: 'https://images.unsplash.com/photo-1578469645742-46cae010e5d4',
  ),
  Spot(
    name: '伏見稲荷大社',
    description: '全国に約3万社ある稲荷神社の総本宮。朱色に染まった「千本鳥居」がトンネルのように続く光景は圧巻で、多くの観光客を魅了しています。',
    imageUrl: 'https://images.unsplash.com/photo-1558862107-d49ef2a04d72',
  ),
  Spot(
    name: '嵐山 竹林の道',
    description: '天龍寺から野宮神社にかけて続く、数万本の竹が生い茂る小道。風が竹林を揺らす音は「日本の音風景100選」にも選ばれています。',
    imageUrl: 'https://images.unsplash.com/photo-1607619662634-3ac55ec0e216',
  ),
];
// --- ここまでデータ部分 ---


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
      title: '京都観光アプリ',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      // 最初に表示するのは一覧画面
      home: const SpotListPage(),
    );
  }
}

// --- 画面1：観光地の一覧画面 ---
class SpotListPage extends StatelessWidget {
  const SpotListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('京都 おすすめ観光地'),
        backgroundColor: Colors.green[100],
      ),
      // リスト形式で表示するためのウィジェット
      body: ListView.builder(
        // リストの項目数をデータの数に合わせる
        itemCount: kyotoSpots.length,
        // 各項目をどのように表示するかを決める
        itemBuilder: (context, index) {
          final spot = kyotoSpots[index];
          return ListTile(
            title: Text(spot.name),
            // 項目がタップされた時の処理
            onTap: () {
              // 詳細画面に移動する命令
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => SpotDetailPage(spot: spot),
                ),
              );
            },
          );
        },
      ),
    );
  }
}

// --- 画面2：観光地の詳細画面 ---
class SpotDetailPage extends StatelessWidget {
  // 表示するべき観光地データを受け取るための変数
  final Spot spot;

  const SpotDetailPage({super.key, required this.spot});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(spot.name), // 受け取ったデータの名前をタイトルに表示
        backgroundColor: Colors.green[100],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // ネットワーク経由で写真を表示
              Image.network(spot.imageUrl),
              const SizedBox(height: 16),
              // 観光地名
              Text(
                spot.name,
                style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              // 説明文
              Text(
                spot.description,
                style: const TextStyle(fontSize: 16),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```
(注: 画像のURLは、雰囲気に合うものをUnsplashから引用しました)

#### 次のステップ（機能拡張のヒント）

この基本のアプリが動いたら、さらに自分好みに育てていきましょう！

*   **機能案1：地図表示機能**
    *   各観光地の住所データを追加し、詳細画面に地図を表示してみる。
*   **機能案2：「行きたいリスト」機能**
    *   各スポットにハートマークのボタンをつけ、お気に入りの場所を保存できるようにする。
*   **機能案3：データ追加機能**
    *   あなたが実際に見つけた「隠れ家カフェ」などを、自分でアプリに追加できる機能を作る。

AIメンターに「詳細画面に地図を追加したいです。どうすればいいですか？」と聞けば、きっと素晴らしいヒントをくれるはずです。楽しみながら、あなただけのアプリを完成させていきましょう！

はい、承知いたしました。
アプリ開発において著作権は非常に重要ですが、難しく感じさせてはいけません。初心者が「これは自分のことだ」と理解し、簡単で安全な方法をすぐに実践できるようなマニュアルを作成します。

---

### アプリ開発の落とし穴：写真の「著作権」を理解しよう

アプリに写真が入ると、ぐっと魅力的になります。しかし、ここで多くの初心者が陥ってしまう、**非常に危険な落とし穴**があります。それが、写真の「**著作権**」です。

「Google画像検索で良さそうな写真を見つけたから、自分のアプリに使おう！」

**…ちょっと待ってください！その行為は、法律で禁止されているかもしれません。**

#### 【最重要】絶対にやってはいけないこと

インターネット上で見つけた写真には、作った人（撮影者）の権利である「著作権」があります。他人の自転車を無断で乗り去ってはいけないのと同じように、**Google画像検索や個人のブログなどで見つけた写真を、許可なく自分のアプリに使うことは「著作権の侵害」にあたり、絶対にしてはいけません。**

もし公開するアプリで無断使用が発覚すると、アプリの公開停止や、損害賠償を請求されるなどの大きなトラブルに発展する可能性があります。

#### では、どうすれば？安全な写真を手に入れる3つの方法

幸いなことに、私たちは安全かつ無料で、アプリに使える美しい写真をたくさん手に入れることができます。主に以下の3つの方法を覚えておけば万全です。

##### 方法1：【推奨】ロイヤリティフリーの写真サイトを活用する

世界には、親切なクリエイターたちが「私の写真は、商用利用も含めて自由に使っていいですよ」と公開してくれている、素晴らしい写真サイトがたくさんあります。これらを「ロイヤリティフリー」や「CC0」ライセンスの写真と呼びます。

以下のサイトは特に有名で、品質も高く、ブックマークしておくと一生役立ちます。

*   **Unsplash:** おしゃれでアーティスティックな写真が豊富。
*   **Pexels:** センスの良い写真や動画素材が見つかる。
*   **Pixabay:** 写真だけでなく、イラスト素材なども充実。



##### 方法2：【一番かんたん】AIメンターに探してもらう

これらのサイトで探すのも良いですが、最も手軽なのは、あなたのAIメンターに安全な写真を探してもらうことです。

AIは、著作権フリーの写真サイトを横断的に探し、あなたのアプリのイメージに合った写真を提案してくれます。

**プロンプト（依頼文）の例：**
「奈良の東大寺の写真を、アプリで商用利用できるロイヤリティフリーのもので探してください。Unsplashなどのサイトから、直接表示できる画像URLを教えてください。」

この一言で、あなたは著作権のリスクを心配することなく、安全な写真のURLを手に入れることができます。

##### 方法3：【究極のオリジナル】自分で撮影する

もしあなたがその場所を訪れる機会があるなら、あなた自身がスマートフォンやカメラで撮影した写真は、**最高のオリジナル素材**です。もちろん著作権はあなたにあるので、100%安全で、何よりあなたのアプリにユニークな魂を吹き込みます。

---
> **まとめ：写真を使うときの鉄則**
>
> *   **Google画像検索の写真は使わない！**
> *   **Unsplashなどのフリー素材サイト**を積極的に利用する。
> *   面倒な時や不安な時は、**AIに「著作-権フリーの写真を探して」と頼む。**
> *   **自分で撮った写真**が、最強で最高の素材。
---

美しい写真で、あなたのアプリを安全に、そして魅力的に彩りましょう！