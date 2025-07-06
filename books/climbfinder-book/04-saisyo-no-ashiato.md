---
title: "第四章：最初の足跡"
---

#### **第四章：最初の足跡**

仲間たちとアプリを使いながら、美咲は新たな欲求に気づいた。「このジム、最近ホールド替えしたらしいよ」「ここの課題、面白いけど辛めだね」――そんな「生きた情報」をアプリで共有できたら、もっと便利で、もっと楽しくなるはずだ。

「よし、コメント機能を追加しよう！」

静的なJSONファイルだけでは実現できないこの機能のために、彼女は「Firebase」という新しい技術の壁に挑む決意をした。クラウドデータベース「Firestore」を使えば、みんなのコメントをアプリに即座に反映できるという。

Firebaseのセットアップ、パッケージの追加、`main.dart`での初期化…。一つ一つの手順は、まるで新しいホールドに手を伸ばすような、未知への挑戦だった。

**1. 依存関係の追加 (`pubspec.yaml`)**
```yaml
# pubspec.yaml
dependencies:
  flutter:
    sdk: flutter
  # ... 既存のパッケージ
  url_launcher: ^6.1.14

  # Firebase関連のパッケージを追加
  firebase_core: ^2.24.2     # Firebaseを初期化するために必須
  cloud_firestore: ^4.14.0 # Firestoreデータベースを使うため
  intl: ^0.18.1              # 日付フォーマット用に後で使う
```

**2. Firebaseの初期化 (`lib/main.dart`)**
```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'package:firebase_core/firebase_core.dart'; // インポート
import 'firebase_options.dart'; // Firebase CLIで自動生成されるファイル

// main関数を非同期に変更して、Firebaseの初期化を待つ
void main() async {
  // Flutterアプリの実行前に、ウィジェットのバインディングを確実に行う
  WidgetsFlutterBinding.ensureInitialized();
  // Firebaseを初期化する
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const ClimbFinderApp());
}

// ... 以下、ClimbFinderAppのコードは変更なし
```

彼女は`StreamBuilder`というウィジェットを知った。それは、データベースを監視し、データが更新されると自動で画面を描き直してくれる魔法のような仕組みだった。この仕組みを使い、美咲は詳細画面にコメント機能を追加していった。

---
#### **【コメント機能のコード】**

**1. コメントのデータモデル (`lib/models/comment.dart`)**
```dart
// lib/models/comment.dart
import 'package:cloud_firestore/cloud_firestore.dart';

class Comment {
  final String id;
  final int gymId;
  final String userName;
  final String text;
  final Timestamp timestamp;

  Comment({
    required this.id,
    required this.gymId,
    required this.userName,
    required this.text,
    required this.timestamp,
  });

  // FirestoreのドキュメントからCommentオブジェクトを生成する
  factory Comment.fromDocument(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return Comment(
      id: doc.id,
      gymId: data['gymId'],
      userName: data['userName'] ?? '名無しさん',
      text: data['text'] ?? '',
      timestamp: data['timestamp'] ?? Timestamp.now(),
    );
  }
}
```

**2. コメント機能が追加された詳細画面 (`lib/screens/detail_screen.dart`)**
```dart
// lib/screens/detail_screen.dart
import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:intl/intl.dart';
import '../models/gym.dart';
import '../models/comment.dart';

// 状態を管理するため、StatefulWidgetに変更
class DetailScreen extends StatefulWidget {
  final Gym gym;
  const DetailScreen({super.key, required this.gym});

  @override
  State<DetailScreen> createState() => _DetailScreenState();
}

class _DetailScreenState extends State<DetailScreen> {
  final _firestore = FirebaseFirestore.instance;
  final _nameController = TextEditingController();
  final _commentController = TextEditingController();

  // コメントをFirestoreに追加する関数
  Future<void> _addComment() async {
    final userName = _nameController.text;
    final text = _commentController.text;

    if (userName.isEmpty || text.isEmpty) return;

    await _firestore.collection('comments').add({
      'gymId': widget.gym.id,
      'userName': userName,
      'text': text,
      'timestamp': FieldValue.serverTimestamp(),
    });

    // 投稿後にダイアログを閉じ、テキストフィールドをクリア
    Navigator.of(context).pop();
    _nameController.clear();
    _commentController.clear();
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
            TextField(controller: _commentController, decoration: const InputDecoration(labelText: 'コメント')),
          ],
        ),
        actions: [
          TextButton(child: const Text('キャンセル'), onPressed: () => Navigator.of(context).pop()),
          ElevatedButton(child: const Text('投稿'), onPressed: _addComment),
        ],
      ),
    );
  }
  
  // コメントリストを表示するウィジェット
  Widget _buildCommentList() {
    return StreamBuilder<QuerySnapshot>(
      stream: _firestore
          .collection('comments')
          .where('gymId', isEqualTo: widget.gym.id)
          .orderBy('timestamp', descending: true)
          .snapshots(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
        
        // 「まだコメントはありません。」この文字が、リリース直後の美咲の不安を映し出していた。
        if (snapshot.data!.docs.isEmpty) {
          return const Padding(
            padding: EdgeInsets.all(16.0),
            child: Center(child: Text('まだコメントはありません。')),
          );
        }

        final comments = snapshot.data!.docs.map((doc) => Comment.fromDocument(doc)).toList();

        return ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: comments.length,
          itemBuilder: (context, index) {
            final comment = comments[index];
            return Card(
              margin: const EdgeInsets.symmetric(vertical: 6.0),
              child: ListTile(
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.gym.name)),
      // 「詳細画面の右下にある『+』ボタン」
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddCommentDialog,
        child: const Icon(Icons.add_comment),
        tooltip: 'コメントを追加',
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ... (既存のジム詳細情報)
            const SizedBox(height: 24),
            const Text('コメント', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            _buildCommentList(), // ここでコメントリストが表示される
          ],
        ),
      ),
    );
  }
}
```
---

コメント機能をリリースしたものの、最初の数日間、アプリは静まり返っていた。詳細画面を開いても、「まだコメントはありません。」という無機質な文字が美咲を迎えるだけ。自分の作った機能が誰にも使われないのではないか、という不安が胸をよぎる。

「そうだ、まずは自分で使ってみなくちゃ！」

美咲は週末、アプリで調べて気になっていた隣町のジム「クライミングパーク ストーン・マジック」へ向かった。傾斜の強い壁に苦戦しながらも、夢中で課題に打ち込む。登り終えた後、スマートフォンのアプリを開き、詳細画面の右下にある「+」ボタンをタップした。

「名前は…Misaでいいかな」

彼女は深呼吸して、キーボードを叩いた。

> **Misa:** 初めて来ました！マンスリー課題の3番、ゴール前のムーブが面白かったです。全体的にパワフルな課題が多い印象。また来ます！

「投稿」ボタンを押すと、`_addComment`関数が走り、入力されたテキストがFirestoreに送信される。そして、その変化を`StreamBuilder`が即座に検知し、画面を再描画した。さっきまで「まだコメントはありません。」と表示されていた場所に、今まさに自分が投稿したコメントがリストとして現れた。

それは、広大なデジタル空間に刻んだ、最初の小さなチョーク跡のようだった。
