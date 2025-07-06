---
title: "最終章：みんなで育てるデジタル岩場"
---

#### **最終章：みんなで育てるデジタル岩場**

今や、美咲の作った「ClimbFinder」は、ただのジム検索アプリではなかった。
それは、日本中のクライマーたちの経験と善意が集まる、一つの大きな「デジタル岩場」になっていた。

初心者はベテランのおすすめを頼りに新しいジムの扉を叩き、遠征するクライマーは地元のリアルな情報を得て計画を立てる。そして美咲自身も、開発者として、一人のクライマーとして、そのコミュニティの成長を喜び、毎晩アプリを開いては新しいコメントに目を通すのが日課になっていた。

そんなある日、彼女はいくつかのジムのコメント欄で、共通のパターンがあることに気づく。

> **Aki (東京):** Base Campの新しい赤テープ（1級）、最後のランジが核心！面白い！
> **Nori (大阪):** JAMのマンスリー5番、誰か登れた人いますか？ムーブ教えてほしい…
> **Tatsu (神奈川):** ストーン・マジックのバランス系課題、ホールドが新しくなって難易度上がったかも？

「みんな、ジム全体のことだけじゃなくて、一つ一つの**課題（ルート）**について話したがってるんだ…！」

その瞬間、美咲の目の前に、次にはっきりと登るべき「壁」が見えた。
今のアプリは「どの山に登るか」を決めるための地図だ。次は、「その山のどのルートを登るか」を共有し、攻略法を語り合える場所を作る。ジムごとの「課題データベース機能」こそが、このアプリが向かうべき次の頂だった。

彼女はすぐにノートパソコンを開き、新しい機能の設計を始めた。Firestoreのデータ構造が、これまで以上に複雑になる。美咲は興奮を抑えながら、理想の構造をスケッチしていった。

---
#### **【次の壁：課題データベース機能の設計】**

**1. Firestoreの新しいデータ構造（設計メモ）**

```
// Firestoreの新しい設計案

// gyms/{gymId}/ (既存のジム情報)
//   └─ routes/{routeId}/ (★新しく追加するサブコレクション)
//      ├─ name: "マンスリー5番" (String)
//      ├─ grade: "3級" (String)
//      ├─ wall_area: "強傾斜壁" (String)
//      ├─ photo_url: "https://firebasestorage.googleapis.com/..." (String) - 課題の写真
//      ├─ creator_name: "Tatsu" (String) - 最初にこの課題を登録した人
//      ├─ created_at: (Timestamp)
//      │
//      └─ comments/{commentId}/ (課題ごとのコメント用サブコレクション)
//         ├─ user_name: "Nori"
//         ├─ text: "スタートの足位置がポイントでした！"
//         └─ timestamp: (Timestamp)
//
//      └─ ascents/{userId}/ (「完登」したユーザーの記録用サブコレクション)
//         ├─ user_name: "Misa"
//         └─ ascended_at: (Timestamp)
```

この「サブコレクション」という仕組みを使えば、ジムと課題、そして課題とコメントを綺麗に関連付けられる。美咲は、この設計を実現するための新しいデータモデルをDartで書き始めた。

**2. 課題データモデル (`lib/models/climbing_route.dart`)**

```dart
// lib/models/climbing_route.dart

import 'package:cloud_firestore/cloud_firestore.dart';

class ClimbingRoute {
  final String id;
  final String name;
  final String grade;
  final String? wallArea;
  final String? photoUrl;
  final String creatorName;
  final Timestamp createdAt;

  ClimbingRoute({
    required this.id,
    required this.name,
    required this.grade,
    this.wallArea,
    this.photoUrl,
    required this.creatorName,
    required this.createdAt,
  });

  factory ClimbingRoute.fromDocument(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return ClimbingRoute(
      id: doc.id,
      name: data['name'] ?? '名称未設定',
      grade: data['grade'] ?? '不明',
      wallArea: data['wall_area'],
      photoUrl: data['photo_url'],
      creatorName: data['creator_name'] ?? '名無しさん',
      createdAt: data['created_at'] ?? Timestamp.now(),
    );
  }
}
```

**3. UIプロトタイプ（ジム詳細画面の改修案）**

美咲は、ユーザーがどう触るかを想像しながら、新しいUIのプロトタイプを組んでみた。ジムの詳細画面に「情報」と「課題リスト」のタブを追加する。

```dart
// lib/screens/detail_screen.dart (未来の改修案)

class _DetailScreenState extends State<DetailScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }
  
  // 課題リストを表示する新しいウィジェット
  Widget _buildRouteList() {
    return StreamBuilder<QuerySnapshot>(
      // ジムのドキュメントの下にある`routes`サブコレクションを購読する
      stream: _firestore
          .collection('gyms')
          .doc(widget.gym.id.toString()) // ※実際のIDに合わせて調整
          .collection('routes')
          .orderBy('created_at', descending: true)
          .snapshots(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
        if (snapshot.data!.docs.isEmpty) {
          return const Center(child: Text('まだ課題が登録されていません。'));
        }

        final routes = snapshot.data!.docs.map((doc) => ClimbingRoute.fromDocument(doc)).toList();

        return ListView.builder(
          itemCount: routes.length,
          itemBuilder: (context, index) {
            final route = routes[index];
            return Card(
              child: ListTile(
                leading: CircleAvatar( // 課題の写真を表示
                  backgroundImage: (route.photoUrl != null) 
                    ? NetworkImage(route.photoUrl!) 
                    : null,
                  child: (route.photoUrl == null) ? const Icon(Icons.terrain) : null,
                ),
                title: Text('${route.name} (${route.grade})'),
                subtitle: Text('エリア: ${route.wallArea ?? '不明'}'),
                // ここをタップすると、その課題専用のコメントページに飛ぶ（将来実装）
                onTap: () { /* Navigate to Route Detail Page */ },
              ),
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.gym.name),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(icon: Icon(Icons.info), text: 'ジム情報'),
            Tab(icon: Icon(Icons.line_style), text: '課題リスト'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          // 1番目のタブ：これまでの情報ページ
          SingleChildScrollView(
            // ... これまでの詳細情報ウィジェット
          ),
          // 2番目のタブ：新しく作る課題リスト
          _buildRouteList(),
        ],
      ),
      // ...
    );
  }
}
```

---
ノートパソコンの画面に映し出された新しいUIの設計図を眺めながら、美咲は微笑んだ。この機能が完成すれば、ユーザーはジムという大きなフィールドだけでなく、一本一本のルートというミクロな世界でも繋がることができる。

始まりは、たった一つのExcelファイルと、個人の「あったらいいな」という想いだった。しかし、みんなの声が加わることで、データは命を宿し、アプリはかけがえのない道標となった。チョークの跡が繋がっていくように、人々の想いがデータを紡ぎ、今日もどこかで、誰かの新たな一歩を支えている。

そして、その繋がりはさらに深く、濃密なものになろうとしていた。美咲の挑戦という名のクライミングは、まだまだ終わりそうにない。
