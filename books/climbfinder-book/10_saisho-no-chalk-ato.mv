---
title: s第十章：最初のチョーク跡
---

詳細画面が格段にリッチになり、美咲は自分のアプリに大きな手応えを感じていた。しかし、彼女のビジョンはまだ完成していなかった。今のアプリは、まだ一方通行の情報提供に過ぎない。

「今度は、ユーザーが主役になる番。クライマーたちの『生きた声』を、このアプリに響かせたい！」

彼女が目指すのは、第五章でGeminiと共に決意した**コメント機能**の実装だ。
「このジムの新しい課題、面白いよ！」
「出張で来たけど、駅から近くて助かった！」
そんな何気ない一言が、次に来る誰かのための貴重な道標になる。

そのために、彼女はCloud Firestoreの力を借りる。詳細画面に、リアルタイムで更新されるコメント欄を追加する。この挑戦は、これまでで最も複雑なものになる予感がした。

---

**美咲:**
「Gemini、いよいよコメント機能に挑戦するよ！Firebaseのセットアップは終わってる。詳細画面に、そのジムに関するコメントのリストと、新しくコメントを投稿できるフォームを追加したいんだ。何から手をつければいいかな？」

> **Gemini:**
> 美咲さん、ついにその時が来ましたね！アプリに魂を吹き込む、最も重要な機能の一つです。
>
> まず、Firestoreに**コメントデータを保存するための設計**を考えましょう。`comments`という名前の「コレクション」を作成し、そこに個々のコメントを「ドキュメント」として保存していくのが一般的です。
>
> 各コメントドキュメントには、以下のような情報を含めると良いでしょう。
> *   `gymId`: どのジムへのコメントか紐付けるためのID。
> *   `userName`: 投稿者の名前。
> *   `text`: コメント本文。
> *   `timestamp`: 投稿日時。新しい順に並び替えるために使います。

**美咲:**
「なるほど、`gymId`で紐付けるんだね。それで、Firestoreのデータをリアルタイムで画面に表示するにはどうするの？`FutureBuilder`とは違うの？」

> **Gemini:**
> 素晴らしい質問です！`FutureBuilder`は一度きりの非同期処理に向いていますが、コメントのように「誰かが投稿したら即座に画面に反映させたい」というリアルタイムな更新には、**`StreamBuilder`**というウィジェットが最適です。

**美咲:**
「`StreamBuilder`…！川の流れ（Stream）みたいに、データが流れ込んでくるのを待ち構えるイメージ？」

> **Gemini:**
> まさにその通りです！Firestoreの特定のデータ（例えば、`gymId`が1のジムのコメント）を「購読」すると、そのデータに変更があるたびに`StreamBuilder`に新しいデータが流れてきます。`StreamBuilder`はその都度、UIを自動で再描画してくれるんです。
>
> 投稿フォームは、`AlertDialog`（ポップアップダイアログ）を使ってシンプルに実装するのがおすすめです。
>
> この二つの要素を組み合わせた、コメント機能全体のコードを組み立てていきましょう。

---

Geminiの設計図を元に、美咲はコードと格闘した。`StatefulWidget`への変更、`TextEditingController`の管理、そして初めて使う`StreamBuilder`…。一つ一つの新しい概念が、新しいホールドのように彼女の前に現れる。

#### **`lib/screens/detail_screen.dart` (コメント機能追加)**
※長くなるため、コメント機能に関連する部分を中心に抜粋・改修

```dart
import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart'; // Firestoreをインポート
import 'package:intl/intl.dart'; // 日付フォーマット用にインポート
import '../models/gym.dart';
import '../models/comment.dart'; // 新しく作るCommentモデル

// 状態を管理するため、StatefulWidgetに変更
class DetailScreen extends StatefulWidget {
  final Gym gym;
  const DetailScreen({super.key, required this.gym});

  @override
  State<DetailScreen> createState() => _DetailScreenState();
}

class _DetailScreenState extends State<DetailScreen> {
  final _firestore = FirebaseFirestore.instance;
  final _nameController = TextEditingController(text: "名無しさん"); // デフォルト名
  final _commentController = TextEditingController();

  @override
  void dispose() {
    _nameController.dispose();
    _commentController.dispose();
    super.dispose();
  }

  // コメントをFirestoreに追加する関数
  Future<void> _addComment() async {
    final userName = _nameController.text;
    final text = _commentController.text;

    if (userName.isEmpty || text.isEmpty) {
      // 簡単なバリデーション
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('名前とコメントを入力してください')),
      );
      return;
    }

    await _firestore.collection('comments').add({
      'gymId': widget.gym.id,
      'userName': userName,
      'text': text,
      'timestamp': FieldValue.serverTimestamp(), // サーバー側のタイムスタンプを使用
    });

    Navigator.of(context).pop(); // ダイアログを閉じる
    _commentController.clear();  // コメント欄をクリア
  }

  // コメント投稿用のダイアログを表示する関数
  void _showAddCommentDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('コメントを投稿'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: _nameController, decoration: const InputDecoration(labelText: 'お名前')),
            TextField(controller: _commentController, decoration: const InputDecoration(labelText: 'コメント'), autofocus: true),
          ],
        ),
        actions: [
          TextButton(child: const Text('キャンセル'), onPressed: () => Navigator.of(context).pop()),
          ElevatedButton(child: const Text('投稿'), onPressed: _addComment),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // ... (extendBodyBehindAppBar, AppBar は変更なし)

      // コメント追加ボタンをFloatingActionButtonとして配置
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddCommentDialog,
        backgroundColor: Colors.brown,
        child: const Icon(Icons.add_comment, color: Colors.white,),
        tooltip: 'コメントを追加',
      ),

      body: SingleChildScrollView(
        child: Column(
          children: [
            // ... (ヒーローイメージなどは変更なし)
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // ... (設備情報タグ、運営者メッセージなど)
                  
                  // コメントセクション
                  _buildSectionTitle('みんなの声'),
                  _buildCommentList(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  // StreamBuilderを使ったコメントリスト
  Widget _buildCommentList() {
    return StreamBuilder<QuerySnapshot>(
      // どのデータを購読するか指定
      stream: _firestore
          .collection('comments')
          .where('gymId', isEqualTo: widget.gym.id) // このジムのコメントに絞り込み
          .orderBy('timestamp', descending: true)  // 新しい順に並び替え
          .snapshots(), // 変更を監視
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }
        if (!snapshot.hasData || snapshot.data!.docs.isEmpty) {
          // この文字が、リリース直後の美咲の不安を映し出していた。
          return const Padding(
            padding: EdgeInsets.symmetric(vertical: 20.0),
            child: Center(child: Text('まだコメントはありません。一番乗りになろう！')),
          );
        }

        final comments = snapshot.data!.docs.map((doc) => Comment.fromDocument(doc)).toList();

        return ListView.builder(
          // SingleChildScrollViewの中なので、サイズとスクロールの制御が必要
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: comments.length,
          itemBuilder: (context, index) {
            final comment = comments[index];
            return Card(
              margin: const EdgeInsets.symmetric(vertical: 6.0),
              child: ListTile(
                leading: CircleAvatar(child: Text(comment.userName.substring(0, 1))),
                title: Text(comment.text),
                subtitle: Text(
                  '${comment.userName} - ${DateFormat('yyyy/MM/dd HH:mm').format(comment.timestamp.toDate())}',
                ),
              ),
            );
          },
        );
      },
    );
  }
}

// 新しく lib/models/comment.dart を作成
/*
import 'package:cloud_firestore/cloud_firestore.dart';
class Comment {
  // ... (id, gymId, userName, text, timestampプロパティ)
  factory Comment.fromDocument(DocumentSnapshot doc) { ... }
}
*/
```

---

機能をリリースしたものの、最初の数日間、アプリは静まり返っていた。詳細画面を開いても、「まだコメントはありません。一番乗りになろう！」という、自分で書いた無機質な文字が美咲を迎えるだけ。自分の作った機能が誰にも使われないのではないか、という不安が胸をよぎる。

「そうだ、まずは自分で使ってみなくちゃ！」

美咲は週末、アプリで調べて気になっていた隣町のジム「クライミングパーク ストーン・マジック」へ向かった。傾斜の強い壁に苦戦しながらも、夢中で課題に打ち込む。登り終えた後、スマートフォンのアプリを開き、詳細画面の右下にある「+」ボタンをタップした。

「名前は…Misaでいいかな」

彼女は深呼吸して、キーボードを叩いた。

> **Misa:** 初めて来ました！マンスリー課題の3番、ゴール前のムーブが面白かったです。全体的にパワフルな課題が多い印象。また来ます！

「投稿」ボタンを押すと、`_addComment`関数が走り、入力されたテキストがFirestoreに送信される。そして、その変化を`StreamBuilder`が即座に検知し、画面を再描画した。さっきまで「まだコメントはありません。」と表示されていた場所に、今まさに自分が投稿したコメントがカードとして現れた。

それは、広大なデジタル空間に刻んだ、最初の小さなチョーク跡のようだった。