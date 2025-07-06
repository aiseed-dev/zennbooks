---
title: "第六章：データの壁を越えて"
---

#### **第六章：データの壁を越えて**

ある日、美咲はアプリのコメントを眺めていて、あることに気づいた。

> **Kenji (神奈川県):** このジム、リード壁はあるけど、オートビレイはないのかな？情報が知りたいです。

美咲は`gym_data_en.json`を開いた。`has_lead`、`has_auto_belay`…。これらの項目は`null`のまま放置されているものがほとんどだった。健太がくれた元のExcelデータが不完全だったのだ。彼女が最初に作ったデータは、完璧ではなかった。

「みんなが知りたい情報は、これだ…！」

彼女はすぐに行動に移した。静的なJSONファイルを更新するのは現実的ではない。ならば、ユーザー自身が情報を更新できるようにすればいい。彼女は、Firestoreにもう一つ新しいコレクションを作ることにした。

```
// Firestoreに新しく設計したコレクション (設計メモ)

// Collection: gym_info_aggregates
// 各ジムの補足情報を、ユーザー投票によって集計するための場所。
// ドキュメントIDは "gym_1", "gym_2" のように、ジムIDと紐づける。

// Document: "gym_101" (とあるジムのデータ)
{
  "has_auto_belay": {
    "yes": 5, // 「はい」と投票したユーザー数
    "no": 1   // 「いいえ」と投票したユーザー数
  },
  "has_lead_wall": {
    "yes": 12,
    "no": 0
  }
  // ... 他の設備情報も同様に集計できる
}
```

この設計を元に、彼女は夜な夜なコードを書き上げた。詳細画面に「情報提供」ボタンを追加し、「オートビレイはありますか？」といった質問にユーザーが「はい」「いいえ」で答えられるようにした。そして、その回答をFirestoreに安全に集計する仕組みを実装した。

---
#### **【ユーザー情報提供機能のコード】**

**`lib/screens/detail_screen.dart`の最終進化**

```dart
// lib/screens/detail_screen.dart

// ... (既存のimport)

class _DetailScreenState extends State<DetailScreen> {
  // ... (既存の変数)

  // ユーザーからの情報をFirestoreに送信する関数
  // 複数のユーザーが同時に投票しても問題ないように、トランザクション処理を使用
  Future<void> _submitInfo(String infoType, String value) async {
    final docRef = _firestore.collection('gym_info_aggregates').doc('gym_${widget.gym.id}');

    await _firestore.runTransaction((transaction) async {
      final snapshot = await transaction.get(docRef);

      if (!snapshot.exists) {
        // ドキュメントがなければ新規作成
        transaction.set(docRef, {
          infoType: {value: 1}
        });
      } else {
        // ドキュメントがあれば、該当のカウンターを1増やす
        final currentCount = (snapshot.data()![infoType]?[value] ?? 0) as int;
        transaction.update(docRef, {'$infoType.$value': currentCount + 1});
      }
    });

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('情報提供ありがとうございます！')),
    );
  }

  // 情報提供を促すダイアログ
  void _showProvideInfoDialog(String infoType, String title) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(title),
        content: const Text('このジムの情報を教えてください。'),
        actions: [
          TextButton(
            child: const Text('いいえ'),
            onPressed: () {
              Navigator.of(context).pop();
              _submitInfo(infoType, 'no');
            },
          ),
          TextButton(
            child: const Text('はい'),
            onPressed: () {
              Navigator.of(context).pop();
              _submitInfo(infoType, 'yes');
            },
          ),
        ],
      ),
    );
  }
  
  // 設備情報を表示するウィジェットを、ユーザーからの情報も反映できるように改修
  Widget _buildAmenityRow(IconData icon, String title, String? staticStatus, String infoType) {
    // 1. gym_data_en.jsonに明確な情報（"有" or "無"）があれば、それを表示
    if (staticStatus != null && staticStatus.isNotEmpty) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 8.0),
        child: Row(
          children: [
            Icon(icon, color: Colors.grey[700]),
            const SizedBox(width: 16),
            Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
            const Spacer(),
            Text(
              staticStatus,
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: staticStatus == '有' ? Colors.green : Colors.red,
              ),
            ),
          ],
        ),
      );
    }

    // 2. JSONに情報がない場合、Firestoreの集計データをリアルタイムで表示
    return StreamBuilder<DocumentSnapshot>(
      stream: _firestore.collection('gym_info_aggregates').doc('gym_${widget.gym.id}').snapshots(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) return const SizedBox.shrink(); // ローディング中は何も表示しない

        final data = snapshot.data?.data() as Map<String, dynamic>?;
        final infoData = data?[infoType] as Map<String, dynamic>?;
        final yesVotes = infoData?['yes'] ?? 0;
        final noVotes = infoData?['no'] ?? 0;
        final totalVotes = yesVotes + noVotes;

        // 3. 投票数に応じて表示を切り替える
        Widget statusWidget;
        if (totalVotes < 3) { // 投票が3票未満なら「情報提供」を促す
          statusWidget = TextButton(
            onPressed: () => _showProvideInfoDialog(infoType, '$title はありますか？'),
            child: const Text('情報を提供する'),
          );
        } else if (yesVotes > noVotes) { // 「はい」が多数派
          statusWidget = Text('有り (みんなの情報)', style: TextStyle(color: Colors.green.shade700, fontWeight: FontWeight.bold));
        } else { // 「いいえ」が多数派
          statusWidget = Text('無し (みんなの情報)', style: TextStyle(color: Colors.red.shade700, fontWeight: FontWeight.bold));
        }
        
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 8.0),
          child: Row(
            children: [
              Icon(icon, color: Colors.grey[700]),
              const SizedBox(width: 16),
              Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
              const Spacer(),
              statusWidget,
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // ... (AppBar, FloatingActionButton)
      body: SingleChildScrollView(
        child: Column(
          children: [
            // ... (既存の基本情報)
            // 設備情報セクションの呼び出し方を変更
            _buildSectionHeader('設備'),
            _buildAmenityRow(Icons.local_parking, '駐車場', widget.gym.hasParking, 'has_parking'),
            _buildAmenityRow(Icons.shower, 'シャワー', widget.gym.hasShower, 'has_shower'),
            _buildAmenityRow(Icons.escalator_warning, 'キッズエリア', null, 'has_kids_area'), // JSONにない項目も追加
            _buildAmenityRow(Icons.security, 'オートビレイ', null, 'has_auto_belay'), // Kenjiさんのための項目
            // ... (コメントセクション)
          ],
        ),
      ),
    );
  }
  // ...
}
```
---

> **Kenjiさんへ (開発者Misaより):** 皆様からの情報提供を元に、オートビレイの有無を表示できるようにアップデートしました！ご協力ありがとうございます！

美咲は、アプリの「お知らせ」欄にそう書き込んだ。すると、すぐに反応があった。

> **Kenji:** うわ、すごい！開発者さん見てるんですね！早速情報提供しました。ありがとう！

Kenjiが「情報を提供する」ボタンを押し、「はい」を選択すると、`_submitInfo`関数が実行される。Firestoreの`gym_info_aggregates`コレクションで、該当ジムの`has_auto_belay`カウンターが一つ増える。
そして、彼を含めて3人が投票を終えた瞬間、`StreamBuilder`がその変化を捉え、彼のスマートフォンの画面表示が「情報を提供する」から「有り (みんなの情報)」へとリアルタイムに切り替わった。

それから、ユーザーたちは競うように情報を提供してくれた。まるで、みんなで協力して新しいルートを開拓していくように。「駐車場は3台まで」「シャワーは有料（100円）」「ここのショップ、意外と品揃えいいですよ」――JSONファイルだけでは絶対に得られなかった、細やかで血の通った情報が、コメントや新たな情報提供機能を通じて、アプリをどんどん豊かにしていくのだった。
