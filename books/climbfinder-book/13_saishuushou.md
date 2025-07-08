---
title: 第十三章：一本の線から生まれる、無数の物語
---

「ClimbFinder」は、美咲の想像を超えて成長していた。検索機能、コメント機能、情報報告、そしてお気に入り・メモ機能。それらは全て、クライマーたちの「もっと便利に、もっと楽しく」という声に応える形で生まれてきた。

そして今、彼女の元には、アプリの未来を決定づけるような声が、日々寄せられていた。

> **Aki (東京):** Base Campの新しい赤テープ（1級）、最後のランジが核心！面白い！
> **Nori (大阪):** JAMのマンスリー5番、誰か登れた人いますか？ムーブ教えてほしい…
> **Tatsu (神奈川):** ストーン・マジックのバランス系課題、ホールドが新しくなって難易度上がったかも？

「みんな、ジム全体のことだけじゃなくて、一つ一つの**課題（ルート）**について話したがってるんだ…！」

その瞬間、美咲の目の前に、次にはっきりと登るべき「壁」が見えた。
今のアプリは「どの山に登るか」を決めるための地図だ。次は、「その山のどのルートを登るか」を共有し、攻略法を語り合える場所を作る。ジムごとの**「課題データベース機能」**こそが、このアプリが向かうべき次の頂だった。

これは、これまでで最も複雑で、最も大きな挑戦になる。美咲は興奮を抑えながら、最後の壁に挑むための作戦を練るべく、Geminiに語りかけた。

---

**美咲:**
「Gemini、ついに最後の機能に挑戦する時が来たみたい。ジムのページの中に、ユーザーが『課題』を登録できるデータベースを作りたいんだ。課題の写真、グレード、壁のエリア、そしてその課題だけのコメント欄…全部を詰め込みたい！」

> **Gemini:**
> 美咲さん、そのビジョン、素晴らしいです！それは「ClimbFinder」が単なるジム検索アプリから、**クライミングという体験そのものを共有するプラットフォーム**へと昇華する、究極の機能ですね。物語のクライマックスにふさわしい、壮大な挑戦です。

**美咲:**
「でも、データ構造がすごく複雑になりそう。ジムと課題、課題とコメント、課題と完登者…どうやって関連付ければいいんだろう？」

> **Gemini:**
> ここで、Firestoreの強力な機能である**「サブコレクション」**の出番です。これは、ドキュメントの中に、さらにコレクションを持つことができる入れ子構造です。この仕組みを使えば、複雑な関係性も非常に綺麗に表現できます。
>
> **究極のデータ構造案:**
> ```
> // Firestoreの設計
> gyms/{gymId}/
>   ├─ (ジムの基本情報フィールド)
>   └─ routes/{routeId}/   (★課題を格納するサブコレクション)
>      ├─ name: "マンスリー5番" (String)
>      ├─ grade: "3級" (String)
>      ├─ photoUrl: "..." (String) - 課題の写真
>      ├─ ... (その他、壁のエリアなどの情報)
>      │
>      ├─ comments/{commentId}/ (★課題ごとのコメント用サブコレクション)
>      │  ├─ userName: "Nori"
>      │  └─ text: "スタートの足位置がポイントでした！"
>      │
>      └─ ascents/{userId}/   (★課題を「完登」したユーザー記録用サブコレクション)
>         └─ userName: "Misa"
> ```
> このように、`gyms`コレクションの中の各ジムドキュメントが、自分自身の`routes`サブコレクションを持つ。これにより、データの親子関係が明確になります。

**美咲:**
「サブコレクション…！なるほど、これならデータがごちゃごちゃにならないね！課題の写真は、これまで通りFirebase Storageを使えばいいんだよね？」

> **Gemini:**
> その通りです！ユーザーがスマホから写真をアップロードし、そのURLを`photoUrl`に保存する流れになります。`image_picker`パッケージを使えば、ギャラリーからの写真選択やカメラ起動が簡単に実装できます。
>
> これは大きな機能なので、一気には作れません。
> 1.  まず、ジム詳細画面に「課題リスト」タブを追加し、課題を閲覧できるようにする。
> 2.  次に、新しい課題を登録するフォームを作る。
> 3.  最後に、各課題の詳細ページで、コメントや完登記録を付けられるようにする。
>
> 一歩ずつ、最高の機能を一緒に作り上げていきましょう。

---

美咲は、これまでの全ての知識と経験を総動員して、開発に取り組んだ。`StatefulWidget`、`StreamBuilder`、画像アップロード、そしてサブコレクションの扱いは、まさに総合力が試される最終課題だった。

#### **`lib/screens/detail_screen.dart` (課題タブの追加)**

```dart
// ...
// TabControllerを使うため、TickerProviderStateMixinを追加
class _DetailScreenState extends State<DetailScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.gym.name),
        // ... (お気に入りボタンなど)
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(icon: Icon(Icons.info_outline), text: 'ジム情報'),
            Tab(icon: Icon(Icons.list_alt), text: '課題リスト'),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () { /* 新しい課題登録画面へ遷移 */ },
        child: const Icon(Icons.add),
        tooltip: '新しい課題を登録',
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          // 1番目のタブ：これまでの情報ページ
          SingleChildScrollView(
            child: Column( /* ... 既存の詳細情報ウィジェット ... */ ),
          ),
          // 2番目のタブ：新しく作る課題リスト
          _buildRouteList(),
        ],
      ),
    );
  }

  // 課題リストを表示する新しいウィジェット
  Widget _buildRouteList() {
    return StreamBuilder<QuerySnapshot>(
      // ジムのドキュメントの下にある`routes`サブコレクションを購読する
      stream: _firestore
          .collection('gyms') // 注: この例ではgymsコレクションがあると仮定
          .doc(widget.gym.id.toString())
          .collection('routes')
          .orderBy('createdAt', descending: true)
          .snapshots(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
        if (snapshot.data!.docs.isEmpty) {
          return const Center(child: Text('まだ課題が登録されていません。\n一番乗りで登録しよう！'));
        }

        final routes = snapshot.data!.docs.map((doc) => ClimbingRoute.fromDocument(doc)).toList();

        return ListView.builder(
          itemCount: routes.length,
          itemBuilder: (context, index) {
            final route = routes[index];
            return Card(
              child: ListTile(
                leading: CircleAvatar(
                  backgroundImage: (route.photoUrl != null) ? NetworkImage(route.photoUrl!) : null,
                  child: (route.photoUrl == null) ? const Icon(Icons.terrain) : null,
                ),
                title: Text('${route.name} (${route.grade})'),
                subtitle: Text('壁エリア: ${route.wallArea ?? '不明'}'),
                // ここをタップすると、その課題専用のページに飛ぶ（将来実装）
                onTap: () { /* Navigate to Route Detail Page */ },
              ),
            );
          },
        );
      },
    );
  }
}
```

---
数週間の奮闘の末、ついに課題データベース機能の第一弾が完成した。
美咲は、いつものジムで仲間たちに新しいアプリを見せた。

「うわ、なにこれ！ジム情報の下に『課題リスト』タブが増えてる！」

一人が「＋」ボタンをタップし、今まさに登ってきたばかりの課題の写真を撮り、「面白いスラブ 5級」と名前を付けて登録する。すると、`StreamBuilder`がその変化を検知し、その場にいた全員のスマートフォンの「課題リスト」に、リアルタイムで新しい課題が追加された。

「すげえ！俺もさっき登ったやつ登録しよ！」
「この課題のコメント欄で、攻略法とか議論できるってこと？やばい！」

その光景を見て、美咲は静かに微笑んだ。
始まりは、たった一つのExcelファイルと、個人の「あったらいいな」という想いだった。しかし、Geminiという賢い相棒を得て、ユーザーたちの声が加わることで、データは命を宿し、アプリはかけがえのない道標となった。

チョークの跡が繋がってルートができるように、人々の想いがデータを紡ぎ、一つのプラットフォームを創り上げた。ジムという大きなフィールドだけでなく、一本一本のルートというミクロな世界でも、クライマーたちは繋がり、語り合うことができるようになったのだ。

ノートパソコンの画面に映る、活気にあふれた課題リストを眺めながら、美咲は確信する。
彼女の挑戦という名のクライミングは、一つの大きな頂（いただき）にたどり着いた。しかし、それは決して終わりではない。この頂から見える、さらに広がる景色――そこには、仲間たちと共に登る、新しい壁が無限に広がっているのだから。