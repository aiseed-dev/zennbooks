---
title: 付録：ClimbFinder 全体コードサマリー
---

これは、物語を通して高田美咲とGeminiが作り上げてきたクライミングジム検索アプリ「ClimbFinder」の最終的なコード構成の概要です。各ファイルは物語の進行と共に機能追加・改修が重ねられています。

#### **1. プロジェクト構造（`lib`ディレクトリ内）**

```
lib/
├── main.dart                   # アプリのエントリーポイント、Firebase初期化
|
├── models/                     # データモデルクラス
│   ├── gym.dart                # ジム情報のデータモデル
│   ├── comment.dart            # コメントのデータモデル
│   └── climbing_route.dart     # 課題のデータモデル
|
├── screens/                    # 各画面のUIを定義
│   ├── home_screen.dart        # ホーム画面（リスト、検索、フィルタ）
│   ├── detail_screen.dart      # ジム詳細画面（タブ、情報、課題リスト）
│   └── (add_route_screen.dart) # (将来実装：課題追加画面)
|
└── services/                   # ビジネスロジックや外部サービスとの連携
    └── favorite_service.dart   # お気に入り・メモ機能のロジック
```

#### **2. 主要ファイルの最終コード**

##### **`main.dart`**
アプリの起動、Firebaseの初期化、そして基本的なテーマ設定を行います。

```dart
import 'package:climb_finder/screens/home_screen.dart';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package.firebase_auth/firebase_auth.dart';
import 'firebase_options.dart';

void main() async {
  // Flutterアプリの実行前に、ウィジェットのバインディングを確実に行う
  WidgetsFlutterBinding.ensureInitialized();
  
  // Firebaseを初期化する
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // 匿名認証でサインイン（ユーザーごとのデータを扱うため）
  await FirebaseAuth.instance.signInAnonymously();

  runApp(const ClimbFinderApp());
}

class ClimbFinderApp extends StatelessWidget {
  const ClimbFinderApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ClimbFinder',
      theme: ThemeData(
        primarySwatch: Colors.brown,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.brown,
          foregroundColor: Colors.white,
        ),
        floatingActionButtonTheme: const FloatingActionButtonThemeData(
          backgroundColor: Colors.brown,
          foregroundColor: Colors.white,
        )
      ),
      home: const HomeScreen(),
    );
  }
}
```

##### **`models/gym.dart`**
`gym_data.json`と対応する、最も基本的なデータモデルです。物語を通して、Geminiによる拡充やジムからの情報提供でプロパティが増えていきました。

```dart
class Gym {
  final int id;
  final String name;
  final String? region;
  final String? prefecture;
  final String? address;
  final String? access;
  final String? website;
  final String? phoneNumber;
  final bool? hasLeadWall;
  final bool? hasAutoBelay;
  final bool? hasKidsArea;
  final String? hasParking;
  final String? hasShower;
  final String? hasShop;
  final String? imageUrl; // ジムの写真URL
  final String? notes; // ジムからのメッセージや備考

  Gym({
    required this.id,
    required this.name,
    this.region,
    this.prefecture,
    this.address,
    this.access,
    this.website,
    this.phoneNumber,
    this.hasLeadWall,
    this.hasAutoBelay,
    this.hasKidsArea,
    this.hasParking,
    this.hasShower,
    this.hasShop,
    this.imageUrl,
    this.notes,
  });

  factory Gym.fromJson(Map<String, dynamic> json) {
    return Gym(
      id: json['id'],
      name: json['name'] ?? '名前不明',
      // ... 他のプロパティのマッピング
      imageUrl: json['image_url'],
      notes: json['notes'],
    );
  }
}
```

##### **`screens/home_screen.dart`**
アプリの入り口となる画面。検索、地方/都道府県フィルタ、そしてジムのリスト表示を担います。`StatefulWidget`として複雑な状態を管理しています。

```dart
import 'package:flutter/material.dart';
// ... (他のimport)

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Gym> _allGyms = [];
  List<Gym> _filteredGyms = [];
  
  // 状態管理用の変数
  final TextEditingController _searchController = TextEditingController();
  String? _selectedRegion;
  String? _selectedPrefecture;

  // ... (initState, dispose, _loadGymData, _filterGymsなどのロジックは第5章参照)

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ClimbFinder')),
      body: Column(
        children: [
          // --- 検索・フィルタUI ---
          // (第5章で作成したTextFieldとDropdownButtonのUI)
          
          const Divider(),
          
          // --- ジムリスト ---
          Expanded(
            child: ListView.builder(
              itemCount: _filteredGyms.length,
              itemBuilder: (context, index) {
                final gym = _filteredGyms[index];
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                  child: ListTile(
                    title: Text(gym.name, style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text(gym.prefecture ?? ''),
                    trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => DetailScreen(gym: gym),
                        ),
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

##### **`screens/detail_screen.dart`**
アプリの心臓部ともいえる多機能画面。タブ切り替え、ヒーローイメージ、設備タグ、コメント、情報報告、お気に入り、メモ、そして課題データベースの表示など、物語の全機能がここに集約されています。

```dart
import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
// ... (他のimport)

class DetailScreen extends StatefulWidget {
  final Gym gym;
  const DetailScreen({super.key, required this.gym});

  @override
  State<DetailScreen> createState() => _DetailScreenState();
}

class _DetailScreenState extends State<DetailScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final FavoriteService _favoriteService = FavoriteService();
  final TextEditingController _noteController = TextEditingController();

  // ... (initState, dispose, 各種ダイアログ表示関数などは第9, 10, 12章参照)
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.gym.name),
        actions: [ /* お気に入りボタン (第12章参照) */ ],
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(icon: Icon(Icons.info_outline), text: 'ジム情報'),
            Tab(icon: Icon(Icons.list_alt), text: '課題リスト'),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () { /* 課題追加画面へ */ },
        child: const Icon(Icons.add),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          // [タブ1: ジム情報]
          SingleChildScrollView(
            child: Column(
              children: [
                _buildHeroImage(), // (第8章参照)
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildAmenityTags(), // (第8章参照)
                      _buildOwnerMessage(), // (第8章参照)
                      _buildAmenityRowWithReport(), // (第10章参照)
                      _buildNoteSection(), // (第12章参照)
                      _buildCommentList(), // (第9章参照)
                    ],
                  ),
                ),
              ],
            ),
          ),
          // [タブ2: 課題リスト]
          _buildRouteList(), // (第13章参照)
        ],
      ),
    );
  }
  // ... (各種_buildXXXウィジェットメソッド)
}
```

---
この付録は、美咲とGeminiの長い旅の軌跡そのものです。シンプルなリスト表示から始まり、検索、Firebase連携、ユーザー参加機能、そしてサブコレクションを活用した複雑なデータベースへと、一歩一歩、着実に進化してきました。

このコードが、これからFlutterを学ぶ誰かにとって、新たな冒険への第一歩を踏み出すための「最初のホールド」となることを願って。