---
title: 第五章：無数の星から、探す一粒の光
---

美咲のアプリは、基本的なリスト表示と詳細表示ができるようになった。しかし、リストには全国のジムがずらりと並んでいるだけ。東京に住んでいるクライマーが北海道のジム情報を毎回スクロールして越えていくのは、明らかに不便だった。

「これじゃあ、情報が多すぎて逆に探しにくい…！ジムが増えれば増えるほど、使いにくくなっちゃう。」

宝の地図も、広大すぎれば宝の場所を見つけられない。美咲は、ユーザーが求める情報へ一直線にたどり着ける「道」を作る必要性を感じていた。

彼女が思い描いたのは、三つの強力な絞り込み機能だ。
1.  **フリーワード検索:** ジム名の一部や市町村名で検索できる。
2.  **地方別フィルタ:** 「関東」「近畿」などで大まかに絞り込む。
3.  **都道府県別フィルタ:** 地方を選んだ後、さらに「東京都」「大阪府」で絞り込む。

この複雑な条件をどうやって管理し、UIに反映させるか。美咲は、新たな相棒となったGeminiに設計の相談を持ちかけた。

---

**美咲:**
「Gemini、アプリの実用性を上げるために、検索とフィルタ機能をつけたいんだ。フリーワード検索と、地方→都道府県っていう段階的な絞り込みを考えてる。これらを組み合わせた時の状態管理って、どうやるのがスマートかな？」

> **Gemini:**
> 美咲さん、素晴らしい着眼点です！それはユーザー体験を劇的に向上させる、非常に重要な機能改善ですね。
>
> 複数のフィルタ条件を管理するには、**UIの状態（State）を司る変数を明確に定義する**ことが鍵になります。`StatefulWidget`内に、以下のような状態変数を用意しましょう。
>
> *   `_searchQuery`: 検索バーに入力された文字列。
> *   `_selectedRegion`: 選択されている地方名（例: "関東"）。
> *   `_selectedPrefecture`: 選択されている都道府県名（例: "東京都"）。
>
> そして、これらの状態変数が変更されるたびに、表示用のジムリストを再生成するロジックを動かします。

**美咲:**
「なるほど、状態変数を元に毎回リストを作り直すんだね。地方と都道府県の選択肢はどうやって作るのがいいかな？特に、地方を選ぶと都道府県の選択肢が変わる、っていう連動が難しそう。」

> **Gemini:**
> そこは良いUIデザインの見せ所ですね。**`DropdownButton`**というウィジェットを使うのがおすすめです。
>
> *   **地方のドロップダウン:** アプリが保持している全ジムデータから、重複しない地方のリストを動的に生成して選択肢にします。
> *   **都道府県のドロップダウン:** ここがポイントです。地方が選択されたら、その地方に属する都道府県だけのリストを動的に生成し、都道府県ドロップダウンの選択肢を更新します。
>
> この連動を実現するために、`setState`をうまく使って画面を再描画させます。UIの骨格を一緒に作ってみましょう。

**美咲:**
「`DropdownButton`！それに選択肢を動的に作るのか…。すごく実践的だね！ぜひ、そのコードの骨格をお願い！」

---

Geminiの設計思想を元に、美咲はホーム画面を`StatefulWidget`に書き換え、検索とフィルタリングのロジックを組み込んでいった。これまで`FutureBuilder`だけで完結していたシンプルな画面が、複雑な状態管理を持つ高機能な画面へと変貌を遂げていく。

#### **`lib/screens/home_screen.dart` (検索・フィルタ機能追加)**
※`StatefulWidget`への変更と、フィルタリングロジックが中心

```dart
import 'package:flutter/material.dart';
// ... (他のimport)

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Gym> _allGyms = [];          // 全ジムのオリジナルリスト
  List<Gym> _filteredGyms = [];   // フィルタリング後の表示用リスト
  
  // 状態管理用の変数
  final TextEditingController _searchController = TextEditingController();
  String? _selectedRegion;
  String? _selectedPrefecture;

  // 選択肢用のリスト
  List<String> _regions = [];
  List<String> _prefectures = [];

  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadGymData();
    _searchController.addListener(_filterGyms);
  }
  
  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _loadGymData() async {
    // ... (JSON読み込み処理)
    final gyms = await loadGyms(); // loadGymsは以前の章で定義済みとする
    setState(() {
      _allGyms = gyms;
      _filteredGyms = gyms;
      // 地方の選択肢を生成（重複を除外）
      _regions = _allGyms.map((g) => g.region ?? '').toSet().where((r) => r.isNotEmpty).toList()..sort();
      _isLoading = false;
    });
  }

  void _onRegionChanged(String? newRegion) {
    setState(() {
      _selectedRegion = newRegion;
      _selectedPrefecture = null; // 地方が変わったら都道府県はリセット
      // 都道府県の選択肢を更新
      if (newRegion != null) {
        _prefectures = _allGyms
            .where((g) => g.region == newRegion)
            .map((g) => g.prefecture ?? '')
            .toSet().where((p) => p.isNotEmpty).toList()..sort();
      } else {
        _prefectures = [];
      }
      _filterGyms();
    });
  }

  void _onPrefectureChanged(String? newPrefecture) {
    setState(() {
      _selectedPrefecture = newPrefecture;
      _filterGyms();
    });
  }
  
  // すべてのフィルタリングロジックを集約
  void _filterGyms() {
    List<Gym> results = _allGyms;

    // 1. 地方でフィルタ
    if (_selectedRegion != null) {
      results = results.where((gym) => gym.region == _selectedRegion).toList();
    }
    // 2. 都道府県でフィルタ
    if (_selectedPrefecture != null) {
      results = results.where((gym) => gym.prefecture == _selectedPrefecture).toList();
    }
    // 3. フリーワードでフィルタ
    final query = _searchController.text.toLowerCase();
    if (query.isNotEmpty) {
      results = results.where((gym) {
        return gym.name.toLowerCase().contains(query) ||
               (gym.address?.toLowerCase() ?? '').contains(query);
      }).toList();
    }

    setState(() {
      _filteredGyms = results;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ClimbFinder')),
      body: Column(
        children: [
          // --- 検索・フィルタUI ---
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
              children: [
                TextField(
                  controller: _searchController,
                  decoration: const InputDecoration(
                    labelText: 'ジム名や住所で検索',
                    prefixIcon: Icon(Icons.search),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    Expanded(
                      child: DropdownButton<String>(
                        isExpanded: true,
                        value: _selectedRegion,
                        hint: const Text('地方を選択'),
                        onChanged: _onRegionChanged,
                        items: _regions.map<DropdownMenuItem<String>>((String value) {
                          return DropdownMenuItem<String>(value: value, child: Text(value));
                        }).toList(),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: DropdownButton<String>(
                        isExpanded: true,
                        value: _selectedPrefecture,
                        hint: const Text('都道府県を選択'),
                        // 地方が選ばれていないときは非活性
                        onChanged: _prefectures.isEmpty ? null : _onPrefectureChanged,
                        items: _prefectures.map<DropdownMenuItem<String>>((String value) {
                          return DropdownMenuItem<String>(value: value, child: Text(value));
                        }).toList(),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          const Divider(),
          // --- ジムリスト ---
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: _filteredGyms.length,
                    itemBuilder: (context, index) {
                      final gym = _filteredGyms[index];
                      // (CardとListTileを使ったリスト項目は以前の章で作成済み)
                      return Card(
                        child: ListTile(
                          title: Text(gym.name),
                          subtitle: Text(gym.address ?? ''),
                          onTap: () { /* DetailScreenへ遷移 */ },
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

---

アプリを再起動した美咲は、その変化に興奮した。画面上部に検索バーと二つのドロップダウンメニューが追加されている。
「地方を選択」をタップすると、「北海道」「東北」「関東」…と、データに存在する地方が綺麗に並んでいる。
「関東」を選ぶ。すると、隣の「都道府県を選択」が活性化し、タップすると「茨城県」「栃木県」「群馬県」…と、関東の都県だけが表示された。
そして、「東京都」を選ぶと、下のリストが瞬時に絞り込まれ、都内のジムだけが表示される。
さらに検索バーに「渋谷」と打ち込むと、リストには渋谷区のジムだけが残った。

「これだ…！これなら、どんなにジムが増えても迷わない！」

無数に散らばっていた星の中から、ユーザーが自分だけの一粒の光を見つけ出せるようになった瞬間だった。アプリは単なる情報の羅列から、ユーザーの意図を汲み取るインテリジェントな「道具」へと進化した。この強力な検索基盤があれば、これからどんなにデータが増えても、ユーザーを迷わせることはないだろう。美咲は、確かな自信を胸に、次のステップへと進むのだった。