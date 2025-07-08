---
title: 第十二章：心に刻む、未来のホールド
---

美咲のアプリ「ClimbFinder」は、多くのユーザーに使われるようになっていた。コメント機能や情報報告機能によって、アプリは日々成長し、クライマーにとって欠かせないツールとなりつつあった。

そんなある日、美咲は友人との会話の中で、新たなニーズに気づく。

「この間、ClimbFinderで大阪の面白そうなジム見つけたんだよね。でも、いざ出張が決まった時に『あれ、どこのジムだっけ？』って忘れちゃってさ。気になるジムをメモしておけると嬉しいな。」

確かに、アプリの情報は流動的だ。良いジムを見つけても、すぐに行けるとは限らない。ユーザーが「いつか登りたい」と思った未来のホールドを、心の中にだけでなく、アプリの中にも刻みつけておける場所が必要だ。

美咲は、**「お気に入り（ブックマーク）機能」**の実装を決意した。さらに、単にリストアップするだけでなく、**そのジムに関する個人的なメモ**（例：「あの課題を落とす！」「次はXXさんと一緒に来たい」）を残せるようにすれば、もっとパーソナルで愛着の湧く機能になるはずだ。

この「ユーザーごとのデータ」をどう管理するか。美咲は、これまで以上にパーソナライズされた機能に挑むため、Geminiの扉を叩いた。

---

**美咲:**
「Gemini、次の新機能の相談だよ！ユーザーがジムを『お気に入り』登録して、さらにそのジムに個人的な『メモ』を残せる機能を作りたいんだ。これは、ユーザーごとにデータが違うから、Firebaseに保存するのが良さそうだよね？」

> **Gemini:**
> 美咲さん、素晴らしいアイデアです！アプリが単なる情報ツールから、ユーザー一人ひとりの「クライミングログ」や「夢のリスト」へと進化する、非常に重要な一歩ですね。
>
> おっしゃる通り、この機能にはFirebaseが最適です。しかし、これまでの`comments`や`gym_info_reports`とは少し違うアプローチが必要になります。なぜなら、**「誰が」**お気に入りに登録したかを管理する必要があるからです。

**美咲:**
「たしかに…！ということは、ついにユーザー認証（ログイン機能）が必要になる？」

> **Gemini:**
> 本格的にやるならその通りですが、まずはもっとシンプルに始めましょう。多くのアプリで使われている**「匿名認証」**という方法があります。
>
> **Firebase Authentication**の匿名認証を使えば、ユーザーが明示的にメールアドレスやパスワードを登録しなくても、裏側でユニークなユーザーIDを自動的に割り振ることができます。このIDを使えば、機種変更しない限りはそのユーザーを識別し続けられます。

**美咲:**
「匿名認証！それならユーザーに面倒な登録をさせずに済むね！それで、お気に入りとメモのデータはどうやって保存するの？」

> **Gemini:**
> Firestoreに、ユーザーごとのデータを格納する新しいコレクションを作りましょう。例えば`user_favorites`というコレクションです。
>
> **データ構造の提案:**
> *   コレクション: `user_favorites`
> *   ドキュメントID: **匿名認証で取得したユーザーID**
> *   ドキュメントのフィールド:
>     *   `bookmarked_gyms`: お気に入りにしたジムIDのリスト（例: `[1, 25, 101]`）
>     *   `gym_notes`: ジムごとのメモを格納するマップ。
>         ```json
>         {
>           "1": "札幌出張の時に絶対行く！",
>           "101": "Kenjiさんおすすめの駐車場情報を確認する。"
>         }
>         ```
>
> この構造なら、一つのドキュメントを読むだけで、そのユーザーのお気に入りと全メモを取得できます。

**美咲:**
「すごく分かりやすい構造！これなら実装できそう。お気に入りボタンは、状態によってアイコンが変わるようにしたいな。登録済みなら塗りつぶされたハート、未登録なら枠線だけのハート、みたいに。」

> **Gemini:**
> いいですね！UI/UXの観点からも非常に重要です。`StatefulWidget`と`StreamBuilder`を組み合わせ、Firestoreのデータを監視しながらボタンの表示をリアルタイムに切り替えましょう。メモ機能は、詳細画面に専用の入力欄を設けるのが良さそうです。

---

美咲は、まずFirebase Authenticationをプロジェクトに追加し、アプリ起動時に匿名でサインインする処理を組み込んだ。そして、Geminiの設計通りに`user_favorites`コレクションを扱うためのロジックを実装していく。

#### **`lib/services/favorite_service.dart` (お気に入り機能を管理するサービスクラス)**
※ロジックをUIから分離するために、専用のクラスを作成

```dart
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

class FavoriteService {
  final _firestore = FirebaseFirestore.instance;
  final _auth = FirebaseAuth.instance;

  // 現在のユーザーIDを取得
  String? get _userId => _auth.currentUser?.uid;

  // ユーザーのお気に入りドキュメントへの参照
  DocumentReference? get _userDocRef {
    if (_userId == null) return null;
    return _firestore.collection('user_favorites').doc(_userId);
  }

  // お気に入り状態を監視するStream
  Stream<DocumentSnapshot>? get userFavoritesStream => _userDocRef?.snapshots();

  // お気に入り追加/削除
  Future<void> toggleFavorite(int gymId, bool isFavorite) async {
    if (_userDocRef == null) return;
    if (isFavorite) {
      await _userDocRef!.update({'bookmarked_gyms': FieldValue.arrayRemove([gymId])});
    } else {
      await _userDoc-Ref!.set({'bookmarked_gyms': FieldValue.arrayUnion([gymId])}, SetOptions(merge: true));
    }
  }

  // メモを更新
  Future<void> updateNote(int gymId, String note) async {
    if (_userDocRef == null) return;
    await _userDocRef!.set({
      'gym_notes': {gymId.toString(): note}
    }, SetOptions(merge: true));
  }
}
```

#### **`lib/screens/detail_screen.dart` (お気に入りボタンとメモ欄を追加)**

```dart
// ...

class _DetailScreenState extends State<DetailScreen> {
  final FavoriteService _favoriteService = FavoriteService();
  final TextEditingController _noteController = TextEditingController();
  
  // ...

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.gym.name),
        // AppBarにお気に入りボタンを配置
        actions: [
          StreamBuilder<DocumentSnapshot>(
            stream: _favoriteService.userFavoritesStream,
            builder: (context, snapshot) {
              if (!snapshot.hasData) return const IconButton(icon: Icon(Icons.favorite_border), onPressed: null);
              
              final data = snapshot.data?.data() as Map<String, dynamic>?;
              final bookmarkedGyms = data?['bookmarked_gyms'] as List<dynamic>? ?? [];
              final isFavorite = bookmarkedGyms.contains(widget.gym.id);

              return IconButton(
                icon: Icon(isFavorite ? Icons.favorite : Icons.favorite_border, color: isFavorite ? Colors.red : Colors.white),
                onPressed: () => _favoriteService.toggleFavorite(widget.gym.id, isFavorite),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // ... (既存のジム情報)

            // --- 個人用メモセクション ---
            _buildSectionTitle('個人用メモ'),
            StreamBuilder<DocumentSnapshot>(
              stream: _favoriteService.userFavoritesStream,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  final data = snapshot.data?.data() as Map<String, dynamic>?;
                  final notes = data?['gym_notes'] as Map<String, dynamic>? ?? {};
                  _noteController.text = notes[widget.gym.id.toString()] ?? '';
                }
                return TextField(
                  controller: _noteController,
                  decoration: const InputDecoration(
                    hintText: 'このジムに関するメモを自由に残せます...',
                    border: OutlineInputBorder(),
                  ),
  -                maxLines: 3,
                  onChanged: (text) {
                    // ここでdebounce処理を入れると、より洗練される
                    _favoriteService.updateNote(widget.gym.id, text);
                  },
                );
              },
            ),

            // ... (コメントセクションなど)
          ],
        ),
      ),
    );
  }
}
```

---

新しい機能をリリースした美咲は、早速自分で使ってみた。隣町の「クライミングパーク ストーン・マジック」の詳細画面を開き、右上に追加された枠線だけのハートをタップする。すると、アイコンが瞬時に真っ赤な塗りつぶされたハートに変わった。Firestoreの`user_favorites`コレクションに、彼女の匿名ユーザーIDで新しいドキュメントが作られ、`bookmarked_gyms`リストにジムのIDが追加された瞬間だ。

次に、画面下部のメモ欄に「マンスリー3番、リベンジする！」と打ち込む。キーボードを叩くたびに、`onChanged`イベントが発火し、Firestoreの`gym_notes`マップが更新されていく。

アプリを一度閉じて、また開く。別のジムのページを見た後、再びストーン・マジックのページに戻ると、ハートは赤いまま、メモもきちんと残っている。

それは、アプリが初めて「美咲」という一人のユーザーを記憶し、彼女だけの情報を保持した瞬間だった。

この機能によって、「ClimbFinder」は単なるジムのカタログから、ユーザー一人ひとりのクライミングライフに寄り添う、パーソナルな「手帳」へと姿を変えた。ユーザーはもう、気になるジムを見つけても忘れることはない。心に刻んだ未来のホールドを、いつでもこのアプリで確かめることができるのだから。