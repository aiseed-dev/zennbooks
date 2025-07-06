---
title: "第五章：響き合う声"
---

#### **第五章：響き合う声**

その翌週、変化は訪れた。
美咲がアプリを開くと、ホーム画面のジムリストに見慣れない表示が追加されていた。各ジム名の横に、小さな数字の入ったバッジがついている。これは、彼女が「どのジムが盛り上がっているか一目でわかったら楽しいかも」と、こっそり追加しておいたコメント数を表示する機能だった。

そして、「クライミングパーク ストーン・マジック」の項目の横には、`[1]`という数字が輝いていた。自分の投稿だ。

彼女がドキドキしながらその項目をタップして詳細画面を開くと、自分のコメントの下に、見知らぬユーザーからの新しい投稿があった。

> **Tatsu:** Misaさんのコメント見て来ました！3番、確かに面白いですね！僕は5番のバランス系が好きでした。駐車場が広いのも助かります。

「見てくれた人がいる…！」

自分の投稿が、誰かの行動のきっかけになった。顔も知らない誰かと、同じ壁の思い出を共有している。美咲の心に、温かい光が灯った。

その日を境に、アプリは少しずつ賑やかになっていく。
札幌のジムには、出張で訪れたサラリーマンから「出張ついでにひと汗。駅から近くて便利でした」というコメントが。埼玉のジムには、地元の高校生から「新しいルートセット、最高！垂壁の緑テープが楽しい」というフレッシュな声が寄せられた。

大阪のユーザーが「ここのジム、キッズエリアが充実してて子連れにおすすめ」と書き込めば、福岡のユーザーが「うちの近所にもそういうジム欲しいな」と返信するかのように、別のジムに「子連れOKですか？」と質問を投稿する。

美咲は、毎晩アプリを開くのが楽しみになった。そこには、日本中のクライマーたちの「今日の挑戦」や「ささやかな発見」が、リアルタイムで集積されていた。

彼女は時々、開発者としてFirebaseのコンソールを覗き込んだ。そこには、ユーザーたちの声がデータとして刻まれていく、生々しい記録があった。

```
// Firebase Firestoreの "comments" コレクションの中身 (イメージ)

// Collection: comments
[
  // Document 1
  {
    "docId": "aX2fGz...",
    "gymId": 99, // クライミングパーク ストーン・マジックのID
    "userName": "Misa",
    "text": "初めて来ました！マンスリー課題の3番、ゴール前のムーブが面白かったです...",
    "timestamp": "November 12, 2023 at 3:15:07 PM UTC+9"
  },
  
  // Document 2 (Tatsuさんの投稿)
  {
    "docId": "bY8hJk...",
    "gymId": 99, // 同じくストーン・マジック
    "userName": "Tatsu",
    "text": "Misaさんのコメント見て来ました！3番、確かに面白いですね！...",
    "timestamp": "November 19, 2023 at 5:40:11 PM UTC+9"
  },

  // Document 3 (札幌のジムへの投稿)
  {
    "docId": "cZ1iLp...",
    "gymId": 1, // NAC札幌クライミングジムのID
    "userName": "出張クライマー",
    "text": "出張ついでにひと汗。東札幌駅から近くて便利でした",
    "timestamp": "November 21, 2023 at 8:22:30 PM UTC+9"
  },

  // Document 4 (埼玉のジムへの投稿)
  {
    "docId": "dE4kMn...",
    "gymId": 2, // Climb Park Base Camp のID
    "userName": "Tomo",
    "text": "新しいルートセット、最高！特に垂壁の緑テープが楽しい",
    "timestamp": "November 22, 2023 at 6:55:01 PM UTC+9"
  },
  
  // ... こうして、データは増え続けていく
]
```

`gym_data_en.json`という静的な骨格に、ユーザーたちの声という血肉が与えられ、アプリは生き物のように成長を始めたのだ。

---
#### **【コメント数バッジ機能のコード】**

美咲がホーム画面に「こっそり追加した」コメント数表示機能のコード。

**`lib/screens/home_screen.dart`の改修**

```dart
// lib/screens/home_screen.dart
import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;
import 'package:cloud_firestore/cloud_firestore.dart'; // Firestoreをインポート
import '../models/gym.dart';
import 'detail_screen.dart';

class _HomeScreenState extends State<HomeScreen> {
  // ... (既存の変数)
  Map<int, int> _commentCounts = {}; // ジムIDをキー、コメント数を値とするMapを追加

  @override
  void initState() {
    super.initState();
    // 既存の処理に加えて、コメント数を取得する処理を呼び出す
    _loadAllData(); 
    _searchController.addListener(_filterGyms);
  }

  // ジムデータとコメント数を両方読み込むように改修
  Future<void> _loadAllData() async {
    // setStateを一度で済ませるために、ローディング状態を管理
    setState(() { _isLoading = true; });
    
    // Future.waitで、JSON読み込みとFirestoreからの読み込みを並行して実行
    await Future.wait([
      _loadGymData(),
      _loadCommentCounts(),
    ]);

    setState(() { _isLoading = false; });
  }

  Future<void> _loadGymData() async {
    // ... (既存のJSON読み込み処理、setStateはここでは行わない)
    final String response = await rootBundle.loadString('assets/gym_data_en.json');
    final List<dynamic> data = json.decode(response);
    _allGyms = data.map((json) => Gym.fromJson(json)).toList();
    _filteredGyms = _allGyms;
  }

  // 新しく追加した、全コメント数を集計する関数
  Future<void> _loadCommentCounts() async {
    final snapshot = await FirebaseFirestore.instance.collection('comments').get();
    final counts = <int, int>{};

    for (var doc in snapshot.docs) {
      final gymId = doc.data()['gymId'] as int?;
      if (gymId != null) {
        // gymIdをキーにして、コメント数をインクリメント
        counts[gymId] = (counts[gymId] ?? 0) + 1;
      }
    }
    _commentCounts = counts;
  }

  // ... (_filterGymsメソッドは変更なし)

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // ... (AppBarと検索バーは変更なし)
      body: Column(
        children: [
          // ... (検索バー)
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: _filteredGyms.length,
                    itemBuilder: (context, index) {
                      final gym = _filteredGyms[index];
                      // 表示するコメント数を取得
                      final count = _commentCounts[gym.id] ?? 0;

                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        child: ListTile(
                          title: Text(gym.name, style: const TextStyle(fontWeight: FontWeight.bold)),
                          subtitle: Text(gym.prefecture ?? ''),
                          // trailingにコメント数バッジを追加
                          trailing: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              // コメントが1件以上ある場合のみバッジを表示
                              if (count > 0)
                                Chip(
                                  label: Text('$count'),
                                  labelStyle: const TextStyle(color: Colors.white, fontSize: 12),
                                  backgroundColor: Colors.brown.shade300,
                                  padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 0),
                                  visualDensity: VisualDensity.compact,
                                ),
                              const SizedBox(width: 8),
                              const Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey),
                            ],
                          ),
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(builder: (context) => DetailScreen(gym: gym)),
                            );
                          },
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}

```