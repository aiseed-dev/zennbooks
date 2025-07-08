---
title: 第十一章：みんなで描く最新の地図
---

コメント機能が追加され、アプリには少しずつクライマーたちの生の声が集まり始めた。美咲は、毎晩のように新しい投稿を眺めるのが楽しみになっていた。そんなある日、彼女は一つのコメントに目を留めた。

> **Kenji (神奈川県):** このジム、アプリだと駐車場『有』になってるけど、最近コインパーキングが閉鎖されて、今は実質『無』ですよー！これから行く人は注意！

「！」

美咲はハッとした。これは、Geminiがデータ偵察した時点、あるいはジムが情報提供してくれた時点では正しかった情報が、**時間と共に古くなってしまった**典型的な例だ。静的な`gym_data.json`を更新するのは現実的ではないし、ジムの運営者がわざわざ「駐車場がなくなりました」と連絡をくれるとも限らない。

「コメントで指摘してくれるのもありがたいけど、もっと直接的にデータを修正できる仕組みが必要だ…」

ユーザーが情報の誤りを「報告」し、その報告が一定数集まったら、アプリの表示を自動的に更新する。そんな集合知を活用したシステムは作れないだろうか。美咲はこの新しい挑戦について、いつものようにGeminiに相談した。

---

**美咲:**
「Gemini、また新しい課題が見つかったよ。ジムの情報って、日々変わるんだね。ユーザーが『この情報、間違ってるよ』って簡単に報告できる機能を追加したいんだ。例えば『駐車場』の項目に『情報が違うかも？』みたいなボタンを付けて。」

> **Gemini:**
> 美咲さん、素晴らしい気づきです！それはアプリを「自己修復機能を持つ、生きたデータベース」へと進化させる、非常に重要な一歩です。ユーザーからのフィードバックを構造化して収集するわけですね。

**美咲:**
「そう！そして、複数の人が同じ報告をしたら、その情報の確からしさが上がる。例えば、3人以上が『駐車場は無い』と報告したら、詳細画面の表示を『有り』から『無し（みんなの情報より）』みたいに自動で切り替えたい。」

> **Gemini:**
> 完璧な設計思想です。その仕組みを実現するために、Cloud Firestoreに新しいコレクションを作りましょう。`gym_info_reports`といった名前で、ユーザーからの報告を蓄積します。
>
> **データ構造の提案:**
> *   コレクション: `gym_info_reports`
> *   ドキュメントID: `gym_101_has_parking` のように、「ジムID」と「情報項目」を組み合わせたもの。
> *   フィールド:
>     *   `yes_votes`: 「この情報は正しい（有り）」と投票したユーザー数。
>     *   `no_votes`: 「この情報は間違っている（無し）」と投票したユーザー数。

**美咲:**
「なるほど、カウンター方式か！これなら誰が投票したかを記録しなくていいから、プライバシー的にも安心だね。でも、データベースの値を書き換えるとき、複数のユーザーが同時に投票したら、カウントがおかしくなったりしない？」

> **Gemini:**
> 非常に鋭い指摘です。その問題を解決するために、Firestoreには**「トランザクション」**や**「アトミックなインクリメント」**という仕組みがあります。`FieldValue.increment(1)`という命令を使えば、「現在の値に1を足す」という処理を安全に（アトミックに）実行でき、同時書き込みによる競合を防げます。
>
> UI側では、`StreamBuilder`を使ってこの投票数をリアルタイムで監視し、表示を切り替えるのが良いでしょう。

**美咲:**
「`FieldValue.increment`、覚えておく！じゃあ、この仕組みを詳細画面の設備情報の部分に組み込んでみたい。コードのイメージを教えてくれる？」

> **Gemini:**
> 承知しました。既存の設備情報表示ウィジェットを、ユーザーからのフィードバックも反映できるように大胆に改修しましょう。

---

Geminiの設計に基づき、美咲は詳細画面のコードにメスを入れた。静的な情報を表示するだけだったウィジェットが、ユーザーの投票によって表示内容が変化する、動的なウィジェットへと生まれ変わっていく。

#### **`lib/screens/detail_screen.dart` (情報報告機能を追加)**

```dart
// ... (既存のimport)

class _DetailScreenState extends State<DetailScreen> {
  // ... (既存の変数)

  // ユーザーからの情報報告をFirestoreに送信する関数
  Future<void> _reportInfo(String infoType, String voteType) async {
    final docRef = _firestore.collection('gym_info_reports').doc('gym_${widget.gym.id}');
    final fieldToUpdate = '$infoType.$voteType'; // 例: 'has_parking.no_votes'

    // setのmerge:trueでドキュメントやフィールドが無くてもエラーにせず作成
    await docRef.set({
      infoType: {
        voteType: FieldValue.increment(1)
      }
    }, SetOptions(merge: true));

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('情報提供ありがとうございます！')),
    );
  }

  // 情報報告を促すダイアログ
  void _showReportDialog(String infoType, String title) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('「$title」の情報は正しいですか？'),
        content: const Text('現在の情報が間違っている場合は報告してください。'),
        actions: [
          TextButton(
            child: const Text('間違っている (今は無い/違う)'),
            onPressed: () {
              Navigator.of(context).pop();
              _reportInfo(infoType, 'no_votes');
            },
          ),
          TextButton(
            child: const Text('合っている'),
            onPressed: () {
              Navigator.of(context).pop();
              _reportInfo(infoType, 'yes_votes');
            },
          ),
        ],
      ),
    );
  }
  
  // 設備情報を表示するウィジェットを、ユーザーからの情報も反映できるように改修
  Widget _buildAmenityRow(IconData icon, String title, String? staticStatus, String infoType) {
    // 1. gym_data.jsonに明確な情報（"有" or "無"）がある場合
    if (staticStatus != null && staticStatus.isNotEmpty) {
      return StreamBuilder<DocumentSnapshot>(
        stream: _firestore.collection('gym_info_reports').doc('gym_${widget.gym.id}').snapshots(),
        builder: (context, snapshot) {
          int yesVotes = 0;
          int noVotes = 0;

          if (snapshot.hasData && snapshot.data!.exists) {
            final data = snapshot.data!.data() as Map<String, dynamic>;
            final reportData = data[infoType] as Map<String, dynamic>?;
            yesVotes = reportData?['yes_votes'] ?? 0;
            noVotes = reportData?['no_votes'] ?? 0;
          }

          // 2. ユーザー報告が3票以上あり、かつ元の情報と矛盾する場合、表示を上書き
          // 例: 元は「有」だが、「無し」の投票が多数派の場合
          if (noVotes > yesVotes && noVotes >= 3 && staticStatus == '有') {
            return _buildVotedRow(icon, title, '無し (みんなの情報より)', Colors.red.shade700, infoType);
          }
          // 例: 元は「無」だが、「有り」の投票が多数派の場合
          if (yesVotes > noVotes && yesVotes >= 3 && staticStatus == '無') {
            return _buildVotedRow(icon, title, '有り (みんなの情報より)', Colors.green.shade700, infoType);
          }

          // 3. 上書き条件に満たない場合は、元の情報を表示
          return _buildStaticRow(icon, title, staticStatus, infoType);
        },
      );
    }
    // (JSONにない新しい項目用のロジックは、今回は省略)
    return const SizedBox.shrink();
  }
  
  // 元の情報を表示する部分
  Widget _buildStaticRow(IconData icon, String title, String staticStatus, String infoType) {
    return ListTile(
      leading: Icon(icon, color: Colors.grey[700]),
      title: Text(title),
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(staticStatus, style: TextStyle(fontWeight: FontWeight.bold, color: staticStatus == '有' ? Colors.green : Colors.red)),
          IconButton(
            icon: const Icon(Icons.flag_outlined, size: 20),
            tooltip: '情報が間違っている場合はこちら',
            onPressed: () => _showReportDialog(infoType, title),
          ),
        ],
      ),
    );
  }
  
  // 投票結果を反映して表示する部分
  Widget _buildVotedRow(IconData icon, String title, String text, Color color, String infoType) {
    return ListTile(
      leading: Icon(icon, color: Colors.grey[700]),
      title: Text(title),
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(text, style: TextStyle(fontWeight: FontWeight.bold, color: color)),
          IconButton(
            icon: const Icon(Icons.flag, size: 20, color: Colors.blue),
            tooltip: 'ご報告ありがとうございます',
            onPressed: () => _showReportDialog(infoType, title),
          ),
        ],
      ),
    );
  }
}
```

---

新しいバージョンをリリースして数日後、美咲はKenjiさんのコメントがあったジムの詳細画面を開いた。駐車場情報の横に、新しく設置した小さな旗のアイコン（`IconButton`）が表示されている。

彼女は、自分がKenjiさんになったつもりで、その旗アイコンをタップした。
「『駐車場』の情報は正しいですか？」というダイアログが表示される。
「間違っている (今は無い/違う)」をタップ。
「情報提供ありがとうございます！」というスナックバーが一瞬表示された。

この瞬間、Firestoreの`gym_info_reports`コレクションでは、`gym_XXX_has_parking`というドキュメントの`no_votes`カウンターが1つ増えた。

美咲は、この機能がクライマーたちの善意によって正しく機能することを願った。そして、Kenjiさんと同じように駐車場がなくなったことに気づいた他の二人のユーザーが、同じように報告を完了した時――

`StreamBuilder`が`no_votes`が3になったことを検知し、画面を再描画する。
詳細画面の表示が、緑色の「有り」から、赤色の「無し (みんなの情報より)」へと自動的に切り替わる。

それは、中央の管理者がいなくても、ユーザーコミュニティ自身の力で情報の鮮度を保ち、地図を最新の状態に描き変えていく、自己組織化するシステムの誕生だった。美咲のアプリは、また一つ、賢く、そして強くなった。