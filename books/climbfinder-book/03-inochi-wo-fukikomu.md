---
title: "第三章：アプリに命を吹き込む"
---

#### **第三章：アプリに命を吹き込む**

データモデルが完成し、いよいよUI（ユーザーインターフェース）の構築に取り掛かった。`FutureBuilder`と`ListView.builder`を組み合わせ、非同期で読み込んだジムのリストを画面に表示する。

最初に表示されたのは、ジムの名前が並んだだけの、そっけないリストだった。

```dart
// main.dart (UI構築の初期段階)

// ... (json読み込みとGymクラスの定義は完了)

// そっけないリスト表示のコード
class HomeScreen extends StatelessWidget {
  // ... (Future<List<Gym>>を返す非同期関数があるとする)

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ClimbFinder')),
      body: FutureBuilder<List<Gym>>(
        future: loadGyms(), // ジムデータを読み込む非同期関数
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError || !snapshot.hasData) {
            return const Center(child: Text('データの読み込みに失敗しました'));
          }
          
          final gyms = snapshot.data!;

          // 「とりあえず名前だけでも…」と美咲が最初に作ったリスト
          return ListView.builder(
            itemCount: gyms.length,
            itemBuilder: (context, index) {
              // ListTileすら使っていない、本当にシンプルな表示
              return Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text(gyms[index].name),
              );
            },
          );
        },
      ),
    );
  }
}
```

だが、美咲にとっては魔法のように見えた。あのExcelの表が、自分の手でアプリの画面に生まれ変わったのだ。

「もっと見やすく、もっと便利にしなくちゃ」

彼女のデザイナー魂に火がついた。`ListTile`を`Card`ウィジェットで囲んで立体感を出し、岩や自然をイメージしたアースカラーを基調としたデザインに決めた。仲間たちが気にしていた「駐車場の有無」は、`"有"`なら緑のチェック、`"`無`"`なら赤のバツ印のアイコンで表示するようにした。`website`の項目があれば、リンクアイコンをタップすれば`url_launcher`がそのジムの公式サイトを開いてくれる。

この機能を実現するため、彼女はまず`pubspec.yaml`に`url_launcher`を追加した。

```yaml
# pubspec.yaml
dependencies:
  flutter:
    sdk: flutter
  # URLを開くためのパッケージを追加
  url_launcher: ^6.1.14
```

そして、ホーム画面と詳細画面のコードを、彼女のこだわりを詰め込みながら書き上げていった。

---
#### **【完成したコード】**

**1. `lib/screens/home_screen.dart` (ホーム画面)**
検索機能と、美しくデザインされたジムリストを持つメイン画面。

```dart
import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;
import '../models/gym.dart';
import 'detail_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Gym> _allGyms = [];
  List<Gym> _filteredGyms = [];
  bool _isLoading = true;
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadGymData();
    _searchController.addListener(_filterGyms);
  }

  Future<void> _loadGymData() async {
    // ... (JSON読み込み処理)
    final String response = await rootBundle.loadString('assets/gym_data_en.json');
    final List<dynamic> data = json.decode(response);
    setState(() {
      _allGyms = data.map((json) => Gym.fromJson(json)).toList();
      _filteredGyms = _allGyms;
      _isLoading = false;
    });
  }

  void _filterGyms() {
    // ... (検索フィルタリング処理)
    final query = _searchController.text.toLowerCase();
    setState(() {
      _filteredGyms = _allGyms.where((gym) {
        return gym.name.toLowerCase().contains(query) || 
               (gym.prefecture?.toLowerCase() ?? '').contains(query);
      }).toList();
    });
  }
  
  // 美咲こだわりの設備アイコン表示ウィジェット
  Widget _buildAmenityIcon(String? status, IconData icon) {
    if (status == '有') {
      return Icon(icon, color: Colors.green, size: 20);
    } else if (status == '無') {
      return Icon(icon, color: Colors.red, size: 20);
    }
    // データがnullの場合は何も表示しない
    return const SizedBox.shrink(); 
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ClimbFinder'),
        backgroundColor: Colors.brown,
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                labelText: 'ジム名や地名で検索',
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12.0)),
              ),
            ),
          ),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: _filteredGyms.length,
                    itemBuilder: (context, index) {
                      final gym = _filteredGyms[index];
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        child: ListTile(
                          title: Text(gym.name, style: const TextStyle(fontWeight: FontWeight.bold)),
                          subtitle: Text(gym.prefecture ?? ''),
                          trailing: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              _buildAmenityIcon(gym.hasParking, Icons.local_parking),
                              const SizedBox(width: 8),
                              _buildAmenityIcon(gym.hasShower, Icons.shower),
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

**2. `lib/screens/detail_screen.dart` (詳細画面)**
リスト項目をタップしたときに表示される、ジムの詳細情報ページ。`url_launcher`がここで活躍する。

```dart
import 'package:flutter/material.dart';
import '../models/gym.dart';
import 'package:url_launcher/url_launcher.dart';

class DetailScreen extends StatelessWidget {
  final Gym gym;

  const DetailScreen({super.key, required this.gym});

  // URLをブラウザで開くための関数
  Future<void> _launchURL(String? urlString) async {
    if (urlString == null || urlString.isEmpty) return;

    final Uri url = Uri.parse(urlString);
    if (!await launchUrl(url)) {
      // 実際にはSnackBarなどでユーザーにエラーを通知するのが親切
      throw 'Could not launch $url';
    }
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
            // ... (住所、アクセス、電話番号などの情報を表示)
            Text(gym.address ?? '住所情報なし', style: const TextStyle(fontSize: 16)),
            const SizedBox(height: 16),
            if (gym.website != null && gym.website!.isNotEmpty)
              InkWell(
                onTap: () => _launchURL(gym.website),
                child: Row(
                  children: [
                    Icon(Icons.link, color: Colors.blue[700]),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        '公式サイトを見る',
                        style: TextStyle(
                          color: Colors.blue[700],
                          decoration: TextDecoration.underline,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            // ... (その他の詳細情報を表示)
          ],
        ),
      ),
    );
  }
}
```
---
数週間後、アプリ「ClimbFinder」はほぼ完成した。トップページには検索バーがあり、「東京」と入れれば都内のジムだけがフィルタリングされる。リストの項目をタップすれば、住所や設備情報がまとまった詳細画面に飛ぶ。

いつものジムで、美咲は仲間たちにおそるおそるアプリを見せた。
「うわ、見やすい！駐車場あるかどうかがすぐわかるの、めっちゃ助かる！」
「このジム、サイトあったんだ。タップしたらすぐ飛べるの便利！」

仲間たちの称賛の声に、美咲の胸は熱くなった。自分が「欲しい」と思ったものが、他の誰かの「役に立つ」ものになった。デジタルの壁を乗り越えた先には、こうして誰かと喜びを分かち合える瞬間が待っていた。