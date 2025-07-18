---
title: 第6章　AIと作る！未来のAIアルバム作成アプリ 
---

この章では、AIの力を借りて、ただのアルバムではない「賢いアルバムアプリ」の開発に挑戦します。スマートフォンのカメラやAIと連携する、現代的なアプリ開発の面白さを体験しましょう！

### ステップ1：未来的なアイデアをAIにぶつけてみる

あなたの「こんなのできたら面白いな」という発想が、最高のアプリの出発点になります。

**【あなた（初心者）】**
写真を撮りっぱなしで整理できないことが多いです。写真を撮ったら、その写真がどんな内容かAIに簡単な説明文を自動でつけてもらって、アルバムに保存するようなアプリは作れませんか？

---
**【AIメンター】**
それは、ものすごく面白くて、まさに「未来のアプリ」という感じの素晴らしいアイデアです！スマートフォンのカメラ機能と、AIの画像認識能力を組み合わせる、非常に挑戦しがいのあるプロジェクトですね。

このアプリは、これまでよりも少し複雑な技術（カメラ操作、AIとの通信など）が必要になります。そのため、いきなり全部を完成させようとすると、途中で迷子になってしまうかもしれません。

そこで、**アプリを3つのステップに分けて、一つずつ確実にクリアしていく「ロードマップ」**を提案します。

*   **ステップ1：【最優先】カメラで写真を撮って表示する**
    *   まずは、アプリからカメラを起動し、撮った写真を画面に表示する、という基本の骨格を作ります。
*   **ステップ2：AIとの連携**
    *   撮った写真をAIに送り、説明文を生成してもらう機能を追加します。
*   **ステップ3：保存機能の実装**
    *   写真とAIが作った説明文を、スマホのギャラリーに保存します。

このロードマップに沿って、まずは**ステップ1の「カメラ機能」**から確実に動かしていきましょう！

---

### ステップ2：最初のステップのFlutterコードを手に入れる

AIメンターに、ロードマップの最初のステップを動かすためのコードを作成してもらいましょう。

**【AIメンター】**
承知いたしました！では、ロードマップのステップ1である「カメラで写真を撮って、その場で表示する」機能を持つFlutterアプリのコードを作成します。

**【重要】このコードを動かすための事前準備**
このアプリはカメラ機能を使うため、コードを貼り付けるだけでなく、いくつかの設定が追加で必要になります。

1.  **`pubspec.yaml` ファイルにパッケージを追加:**
    ```yaml
    dependencies:
      flutter:
        sdk: flutter
      camera: ^0.10.5+9 # バージョンは最新のものにしてください
      path_provider: ^2.0.12
      path: ^1.8.2
    ```2.  **AndroidとiOSのための権限設定:**
    *   カメラやマイクへのアクセス許可をユーザーに求めるための設定が必要です。これは少し複雑なので、まずは`pubspec.yaml`の編集だけを行い、もしエラーが出たら「Flutter camera 設定方法」と検索したり、私にエラーメッセージを教えてください。

準備ができたら、以下のコードを `lib/main.dart` に貼り付けてみてください。

---

### 【コピー＆ペーストで動く】AIアルバムアプリ（ステップ1：撮影機能）

```dart
// 必要なパッケージをインポート
import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

// グローバル変数として利用可能なカメラのリストを保持
late List<CameraDescription> cameras;

// メイン関数：アプリ起動前にカメラを初期化する
Future<void> main() async {
  // Flutterアプリの実行準備
  WidgetsFlutterBinding.ensureInitialized();
  // 利用可能なカメラのリストを取得
  cameras = await availableCameras();
  // アプリを起動
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AIアルバムアプリ',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      // 最初に表示するのはカメラ撮影画面
      home: CameraScreen(cameras: cameras),
    );
  }
}

// --- 画面1：カメラ撮影画面 ---
class CameraScreen extends StatefulWidget {
  final List<CameraDescription> cameras;

  const CameraScreen({super.key, required this.cameras});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    // カメラコントローラーを初期化（最初のカメラを使用）
    _controller = CameraController(
      widget.cameras[0],
      ResolutionPreset.medium,
    );
    // コントローラーの初期化は非同期で行われる
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    // 画面が破棄される時にコントローラーも破棄
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('写真を撮る')),
      body: FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            // カメラのプレビューを表示
            return CameraPreview(_controller);
          } else {
            // 初期化中はローディングインジケーターを表示
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
      // 撮影ボタン
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          try {
            // カメラの初期化が完了していることを確認
            await _initializeControllerFuture;
            // 写真を撮影し、一時ファイルとして保存
            final image = await _controller.takePicture();

            // 撮った写真を表示する画面に遷移
            if (!mounted) return;
            await Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => DisplayPictureScreen(imagePath: image.path),
              ),
            );
          } catch (e) {
            // エラーが発生した場合はコンソールに出力
            print(e);
          }
        },
        child: const Icon(Icons.camera_alt),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }
}

// --- 画面2：撮った写真の表示画面 ---
class DisplayPictureScreen extends StatelessWidget {
  final String imagePath;

  const DisplayPictureScreen({super.key, required this.imagePath});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('撮った写真')),
      // 写真をファイルパスから読み込んで表示
      body: Center(child: Image.file(File(imagePath))),
    );
  }
}
```

はい、承知いたしました。
PC上のエミュレータで動いていた自分のアプリが、手元のスマートフォンで初めて動いた時の感動は、アプリ開発における最高の瞬間の一つです。

初心者の方がその感動をスムーズに体験できるよう、つまずきやすいポイントを丁寧に解説したマニュアルを作成します。

---

### 自分のAndroidスマホで動かそう！Flutterアプリ実機テストガイド

<span style="color:red;">注意: WindowsPCでは、iPhone用のアプリをビルドできません。そのため、iPnone用のアプリを作る場合は、Macが必要になります。でも、簡単ではありませんが、Macを持たずに自分の作ったアプリを、手元のiPhoneで動かす方法があります。次章で詳しく説明する**GitHub Actions**でビルドし、「**TestFlight**」で公開す方法です。</span>

このアプリは、本物のスマートフォンでアプリを動かしてみたいですよね。実機でテストすることで、パフォーマンスや操作感をより正確に確認できます。
このガイドに沿って、あなたのアプリをAndroidの実機で動かしてみましょう！

#### ステップ1：スマートフォンの「隠し設定」をONにする

まず、あなたのAndroidスマートフォンを「開発用のマシン」としてPCに認識させるための、特別な設定を行います。これは普段は隠されている機能なので、ちょっとした裏技のようでワクワクしますよ。

1.  **「設定」アプリを開く**
    *   スマートフォンの歯車アイコン「設定」を開きます。

2.  **「ビルド番号」を探して、連打する！**
    *   **「設定」→「デバイス情報」（または「端末情報」）→「ソフトウェア情報」**と進みます。
    *   その中に**「ビルド番号」**という項目があります。この項目を、**指で7回連続でタップ**してください！
    *   タップするたびに「デベロッパーになるまであと〇ステップです」というメッセージが表示され、7回タップすると「これでデベロッパーになりました！」と表示されます。

    > 💡 **Tip:** 「ビルド番号」の場所は、スマートフォンのメーカーによって多少異なります。「[あなたのスマホ機種名] 開発者モード」で検索すると、より詳しい情報が見つかります。

3.  **「開発者向けオプション」を有効にする**
    *   「設定」メニューの一番下あたりに戻ると、**「開発者向けオプション」**という新しい項目が出現しています。これこそが隠し設定です。
    *   「開発者向けオプション」を開き、スイッチがONになっていることを確認します。

4.  **「USBデバッグ」をONにする**
    *   「開発者向けオプション」のリストをスクロールし、**「USBデバッグ」**という項目を見つけて、スイッチをONにします。
    *   「USBデバッグを許可しますか？」という警告が出ますが、「OK」をタップしてください。

これで、スマートフォンの準備は完了です！

#### ステップ2：PCとスマートフォンを接続する

次に、PCとスマートフォンをUSBケーブルで物理的につなぎます。

1.  **USBケーブルで接続する**
    *   PCとスマートフォンを、データ転送が可能なUSBケーブルで接続します。充電専用ケーブルでは動かないので注意してください。

2.  **接続の許可をする**
    *   スマートフォン側に**「このパソコンからのUSBデバッグを許可しますか？」**というポップアップが表示されます。
    *   「このパソコンからのUSBデバッグを常に許可する」にチェックを入れ、「許可」（または「OK」）をタップします。これは非常に重要なステップなので、見逃さないようにしましょう。

#### ステップ3：PCにスマホを認識させる（接続確認）

PCがスマートフォンを正しく開発デバイスとして認識しているか、Flutterの「健康診断」コマンドで確認します。

1.  **コマンドプロンプト（またはターミナル）を開く**
2.  `flutter devices` と入力して、Enterキーを押します。

成功すれば、以下のようにあなたのスマートフォンの名前が表示されます。
```
1 connected device:
[あなたのスマホ名] (mobile) • [デバイスID] • android-arm64 • Android [バージョン]
```

> ⚠️ **トラブルシューティング：デバイスが表示されない場合**
>
> *   **Windowsユーザーの場合：** PCがスマホを認識するための「USBドライバ」が不足している可能性があります。「[スマホのメーカー名] USBドライバ」で検索し、メーカー公式サイトからドライバをインストールしてください。
> *   **スマホ側の設定を確認：** USBケーブルを接続した際に、スマホの通知センターを開き、USBの接続モードが「ファイル転送」または「MTP」になっているか確認してください。「充電のみ」になっている場合は変更が必要です。
> *   **物理的な問題：** 別のUSBケーブルや、PCの別のUSBポートを試してみてください。

#### ステップ4：いよいよアプリを実行する！

ここまで来れば、あと一歩です！

##### VSCodeやAndroid Studioを使っている場合

1.  エディタの右下（VSCodeの場合）または上部（Android Studioの場合）に、デバイスを選択するボタンがあります。
2.  そこをクリックすると、先ほど接続したあなたの**スマートフォンの名前**が表示されているはずです。それを選択します。
3.  あとは、いつものように「実行（デバッグの開始）」ボタン（通常は `F5` キー）を押すだけです！

##### コマンドプロンプトから実行する場合

1.  あなたのFlutterプロジェクトのフォルダに移動します。
    `cd C:\dev\myapp`
2.  `flutter run` と入力して、Enterキーを押します。

---

初回はビルドに少し時間がかかりますが、じっと待っていると…あなたのスマートフォンの画面に、見慣れたFlutterのサンプルアプリ（またはあなたが作ったアプリ）が自動的にインストールされ、起動します！

**おめでとうございます！** これであなたは、PCの中だけでなく、本物のデバイスで動くアプリを作れる、正真正銘のアプリ開発者です。実機でもホットリロードが使える便利さも、ぜひ体験してみてください。

### 次のステップ（未来への挑戦）

おめでとうございます！これで、あなたのアプリはカメラと対話する第一歩を踏み出しました。
この基盤の上に、未来的な機能を追加していきましょう。

*   **次の目標（ステップ2）：AIとの連携**
    *   写真表示画面に「AIに説明文を生成させる」ボタンを追加し、AIに写真を送る処理に挑戦します。これには「**Gemini API**」などの技術を使います。
*   **最終目標（ステップ3）：保存機能の実装**
    *   写真とAIが作った説明文を、スマホのギャラリーに保存する機能を追加します。

一歩ずつ、着実に進めていけば、必ずこの未来的なアプリを完成させることができます。次のステップに進みたくなったら、いつでも声をかけてくださいね！


