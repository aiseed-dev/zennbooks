---
title: 第九章：声をかたちに
---

九州のジムからの心温まる返信を皮切りに、美咲の元にはいくつかのジムから公式情報が届き始めた。それはGoogleフォームに整然と並んだデータであり、メールに添えられた情熱的な文章であり、そして、ジムの魅力が詰まった数枚の写真だった。

「この貴重な情報を、ただのテキストとして表示するだけじゃもったいない…！」

美咲のデザイナー魂が再び燃え上がった。AIが拡充してくれた`gym_data_v2.json`と、運営者から直接もらった公式情報を組み合わせ、詳細画面を劇的にリニューアルする時が来たのだ。

彼女の頭の中には、すでに新しいデザインの構想があった。
1.  **ヒーローイメージ:** ジムから提供された一番魅力的な写真を、画面のトップに大きく表示する。
2.  **タグ形式の設備情報:** 「リード壁」「オートビレイ」などの情報は、単なるテキストではなく、アイコン付きのタグで視覚的に分かりやすく見せる。
3.  **運営者からのメッセージ:** ジムの「こだわり」や「アピールポイント」は、特別なセクションを設けて、運営者の温かい声が直接伝わるようにデザインする。

この構想を実現するため、彼女は再びGeminiに相談を持ちかけた。

---

**美咲:**
「Gemini、ジムの運営者さんから写真やアピールポイントをもらえたんだ！これをアプリの詳細画面で、もっと魅力的に見せたい。画面の最初に写真を大きく表示して、設備情報はアイコン付きのタグみたいにして…って考えてるんだけど、どうかな？」

> **Gemini:**
> 美咲さん、素晴らしい進展ですね！運営者の方の想いをUIに反映させる、最高のアイデアだと思います。
>
> *   **ヒーローイメージ**はユーザーの心を掴むのに非常に効果的です。`Stack`ウィジェットを使えば、画像の上にジムの名前を重ねて表示するような、雑誌の表紙のようなデザインも可能ですよ。
> *   **タグ形式**の情報表示は、`Chip`ウィジェットや、`Icon`と`Text`を`Row`で組み合わせたカスタムウィジェットで作ると見栄えが良くなります。情報がある設備だけを動的に表示するようにしましょう。
> *   **運営者からのメッセージ**は、引用符のアイコンを付けたり、背景色を少し変えたりして、他の情報とは区別された特別なブロックとして見せると、その価値がユーザーに伝わりやすくなります。

**美咲:**
「`Stack`に`Chip`…！なるほど、ウィジェットを組み合わせれば表現の幅が広がるんだね。もらった写真は、どうやってアプリに組み込むのがベストかな？アセットに入れる？」

> **Gemini:**
> アセットに入れるのも一つの手ですが、ジムの数が増えるとアプリのサイズがどんどん大きくなってしまいます。ここで、第五章でセットアップした**Firebase**が再び活躍します。
>
> **Firebase Storage**というサービスを使えば、画像のような大きなファイルをクラウド上に保存できます。そして、アプリからはその画像のURLを取得して表示するだけ。こうすれば、アプリ本体のサイズを小さく保ったまま、たくさんの画像を表示できます。

**美咲:**
「Firebase Storage！なるほど、データベースだけじゃなくてファイル置き場もあるんだ。じゃあ、まずはもらった写真をStorageにアップロードして、そのURLをJSONファイルに書き加えておけばいいんだね！」

> **Gemini:**
> その通りです！まずは手動でアップロードして、将来的にはジムの人が自分で写真をアップロードできるような機能も作れますよ。
>
> それでは、これらのアイデアを詰め込んだ、新しい`DetailScreen`のコードを一緒に組み立てていきましょう。

---

美咲は、もらった写真を一枚一枚Firebase Storageにアップロードし、その公開URLを取得した。そして、そのURLを`gym_data_v2.json`に新しい項目`image_url`として追加し、`gym_data_v3.json`を作成した。

そして、Geminiの助言を元に、生まれ変わった詳細画面のコードを書き上げた。

#### **`lib/screens/detail_screen.dart` (大幅リニューアル後)**

```dart
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/gym.dart'; // Gymモデルもimage_urlなどを追加して更新

class DetailScreen extends StatelessWidget {
  final Gym gym;

  const DetailScreen({super.key, required this.gym});

  // ( _launchURL関数は変更なし )

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // AppBarを透明にして、画像がステータスバーの領域まで広がるようにする
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        // アイコンに見やすくなるよう少し影をつける
        leading: CircleAvatar(
          backgroundColor: Colors.black.withOpacity(0.3),
          child: BackButton(color: Colors.white),
        ),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. ヒーローイメージ
            _buildHeroImage(),

            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 2. 設備情報タグ
                  _buildSectionTitle('設備'),
                  _buildAmenityTags(),
                  
                  // 3. 運営者からのメッセージ
                  if (gym.notes != null && gym.notes!.isNotEmpty)
                    _buildOwnerMessage(),

                  // ( 従来の基本情報などもここに続く... )
                  _buildSectionTitle('基本情報'),
                  // ...
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ヒーローイメージウィジェット
  Widget _buildHeroImage() {
    return Stack(
      children: [
        // 画像を読み込み、URLがなければプレースホルダーを表示
        gym.imageUrl != null
            ? Image.network(
                gym.imageUrl!,
                width: double.infinity,
                height: 300,
                fit: BoxFit.cover,
                // 読み込み中のインジケーター
                loadingBuilder: (context, child, progress) {
                  return progress == null ? child : const SizedBox(height: 300, child: Center(child: CircularProgressIndicator()));
                },
                // エラー時の表示
                errorBuilder: (context, error, stackTrace) {
                  return const SizedBox(height: 300, child: Icon(Icons.broken_image, size: 50));
                },
              )
            : Container(height: 300, color: Colors.grey),
        // 画像の上にグラデーションとジム名を重ねる
        Positioned.fill(
          child: Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.black.withOpacity(0.6), Colors.transparent],
                begin: Alignment.bottomCenter,
                end: Alignment.topCenter,
              ),
            ),
          ),
        ),
        Positioned(
          bottom: 20,
          left: 16,
          right: 16,
          child: Text(
            gym.name,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 28,
              fontWeight: FontWeight.bold,
              shadows: [Shadow(blurRadius: 10.0, color: Colors.black)],
            ),
          ),
        ),
      ],
    );
  }

  // 設備情報タグを表示するウィジェット
  Widget _buildAmenityTags() {
    return Wrap(
      spacing: 8.0,
      runSpacing: 4.0,
      children: [
        if (gym.hasLeadWall == true) const AmenityChip(icon: Icons.line_weight, label: 'リード壁'),
        if (gym.hasAutoBelay == true) const AmenityChip(icon: Icons.security, label: 'オートビレイ'),
        if (gym.hasKidsArea == true) const AmenityChip(icon: Icons.child_friendly, label: 'キッズエリア'),
        if (gym.hasParking == '有') const AmenityChip(icon: Icons.local_parking, label: '駐車場'),
        if (gym.hasShower == '有') const AmenityChip(icon: Icons.shower, label: 'シャワー'),
        if (gym.hasShop == '有') const AmenityChip(icon: Icons.store, label: 'ショップ'),
      ],
    );
  }
  
  // 運営者からのメッセージウィジェット
  Widget _buildOwnerMessage() {
    return Container(
      margin: const EdgeInsets.only(top: 24.0),
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: Colors.brown.withOpacity(0.05),
        borderRadius: BorderRadius.circular(8.0),
        border: Border.all(color: Colors.brown.withOpacity(0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.storefront, color: Colors.brown),
              SizedBox(width: 8),
              Text(
                'ジムからのメッセージ',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.brown),
              ),
            ],
          ),
          const SizedBox(height: 8.0),
          Text(gym.notes!, style: const TextStyle(fontSize: 15, height: 1.6)),
        ],
      ),
    );
  }

  // ( _buildSectionTitle, _buildInfoRow などは適宜流用 )
}

// AmenityChipのカスタムウィジェット定義
class AmenityChip extends StatelessWidget {
  final IconData icon;
  final String label;
  const AmenityChip({super.key, required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    return Chip(
      avatar: Icon(icon, size: 18, color: Colors.brown[700]),
      label: Text(label),
      backgroundColor: Colors.brown[100],
    );
  }
}
```

アプリを再起動し、九州のジム「クライミングパーク・フォレストウォール」の詳細画面を開く。
画面いっぱいに、メールで送られてきた温かみのあるジムの写真が広がり、その上に白い文字でジム名が浮かび上がっている。スクロールすると、「リード壁」「駐車場」「シャワー」といった情報が、可愛らしいタグで並んでいた。そして、ハイライトされた特別なブロックには、店長からの「窓から見える山の景色が自慢です」というメッセージが表示されていた。

「…伝わる。」

美咲は確信した。これなら、ただのデータではなく、ジムの雰囲気や運営者の想いがユーザーに直接伝わる。
デジタルのコードと、アナログなコミュニケーション。その二つが交差した時、彼女のアプリは単なる情報ツールを超え、ジムとクライマーを心で繋ぐ「架け橋」へと姿を変えたのだった。