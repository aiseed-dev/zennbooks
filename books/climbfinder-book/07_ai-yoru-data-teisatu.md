---
title: 第七章：AIによるデータ偵察（ルビ：リーコン）
---

Firebaseのセットアップを終え、コメント機能の実装に思いを巡らせていた美咲。しかし、その前に一つの考えが頭をよぎった。

「ユーザーに情報を提供してもらうのも素晴らしいけど、最初のスタートラインはできるだけ高い方がいいよね。今の`gym_data_en.json`は情報が少なすぎる。せめて、全国のジムの公式サイトくらいは網羅しておきたいな…」

健太からもらったリストには、ウェブサイトが空欄のものが多数あった。これを一つ一つ手作業で検索して埋めていくのは、途方もない作業だ。

その時、彼女はいつも頼りにしている相棒の、もう一つの能力を思い出した。

---

**美咲:**
「Gemini、ちょっと大きな相談があるんだ。私の`gym_data_en.json`、ウェブサイトのURLが抜けてるデータがたくさんある。これを、AIの力で自動的に検索して埋めることってできないかな？例えば、『（ジム名） （都道府県）』でウェブ検索して、公式サイトっぽいURLを見つけてくる、みたいな。」

> **Gemini:**
> 美咲さん、それは非常にスマートでパワフルなアイデアです！まさに私の得意分野の一つですよ。私はリアルタイムでウェブを検索し、情報を収集・要約する能力を持っています。その力を使えば、データ拡充のプロセスを劇的に加速できます。

**美咲:**
「ほんと！？すごい！じゃあ、今のJSONデータに足りない『リード壁の有無』とか『オートビレイの有無』みたいな情報も、公式サイトを読み解いて推測したりできる？」

> **Gemini:**
> はい、可能です。もちろん100%の精度ではありませんが、公式サイト内の「施設案内」や「料金案内」といったページを解析し、「リードクライミング」「オートビレイ」といったキーワードの有無から、設備の存在を高い確率で推測できます。
>
> このプロセスを**「データ偵察（リーコン）」**と名付けましょう。具体的には、以下の手順で進めます。
> 1.  まず、現在の`gym_data_en.json`を私が読み込みます。
> 2.  各ジムデータについて、特に情報が欠けている項目（`website`, `phone_number`など）を特定します。
> 3.  ジム名と地域情報を元にウェブ検索を実行し、公式サイトのURLを特定します。
> 4.  見つかった公式サイトの内容を分析し、新しい項目（`has_lead_wall`, `has_auto_belay`など）の情報を推測します。
> 5.  これらの拡充された情報を元に、**新しいバージョンのJSONファイル**を生成します。

**美咲:**
「まさに未来の技術って感じ…！ぜひお願いしたい！追加したい項目はこんな感じかな。」

*   `has_lead_wall` (リード壁の有無)
*   `has_auto_belay` (オートビレイの有無)
*   `has_kids_area` (キッズエリアの有無)
*   `business_hours` (営業時間)
*   `closing_day` (定休日)

> **Gemini:**
> 承知しました。素晴らしい項目リストです。これらの情報を追加することで、アプリの価値は飛躍的に向上しますね。
>
> それでは、データ偵察を開始します。少し時間がかかるかもしれませんが、コーヒーでも飲みながら待っていてください。

---

美咲がGeminiに`gym_data_en.json`の全データをテキストとして貼り付けると、Geminiは静かに、しかし猛烈な勢いで処理を開始した。美咲のPC画面には何も映らないが、その向こう側で、AIがインターネットという広大な情報の海を駆け巡っているのが想像できた。

「Climb Park Base Camp 埼玉県入間市 公式サイト」… 検索、URL特定、ページ解析。
「NAC札幌クライミングジム 施設案内」… 検索、キーワード抽出。
「Climbing JAM 大阪市北区」… 検索、"閉店"の情報を検知。

数分後、Geminiからの応答があった。

> **Gemini:**
> 美咲さん、データ偵察が完了しました。いくつかのウェブサイトは見つかりませんでしたが、大半のデータについて情報を拡充・更新できました。
>
> 新しい項目を追加し、判明した情報を埋め込んだ`gym_data_v2.json`を生成します。また、元のデータ構造との互換性を保ちつつ、新しい項目は`null`を許容するようにしたので、既存のFlutterコードを少し修正するだけで対応できます。

美咲は、生成された新しいJSONファイルを見て目を見張った。

#### **`gym_data_v2.json` (一部抜粋)**

```json
// gym_data_v2.json
[
    {
        "id": 1,
        "region": "北海道",
        "prefecture": "北海道",
        "city": "札幌市白石区",
        "address": "北海道札幌市白石区東札幌3条2丁目1-7",
        "access": "地下鉄東西線「東札幌」駅より徒歩3分",
        "name": "NAC札幌クライミングジム",
        "website": "https://www.nacadventures.jp/nac-sapporo",
        "phone_number": "011-812-7979",
        "wall_area": null,
        "wall_height": 10.0,
        "has_parking": "有",
        "has_shower": "無",
        "has_shop": "有",
        "notes": "",
        // --- ▼ Geminiによって追加された情報 ▼ ---
        "has_lead_wall": true,
        "has_auto_belay": true,
        "has_kids_area": true,
        "business_hours": "平日 13:00-22:00 / 土日祝 10:00-20:00",
        "closing_day": "不定休"
    },
    {
        "id": 2,
        "region": "関東",
        "prefecture": "埼玉県",
        "city": "入間市",
        "address": "埼玉県入間市東町7-1-7",
        "access": "圏央道「入間IC」から約10分",
        "name": "Climb Park Base Camp",
        "website": "https://b-camp.jp/iruma/",
        "phone_number": "04-2936-8585",
        "wall_area": 1200,
        "wall_height": 15,
        "has_parking": "有",
        "has_shower": "有",
        "has_shop": "有",
        "notes": "日本最大級のクライミングジム",
        // --- ▼ Geminiによって追加された情報 ▼ ---
        "has_lead_wall": true,
        "has_auto_belay": false,
        "has_kids_area": true,
        "business_hours": "平日 12:00-23:00 / 土日祝 10:00-21:00",
        "closing_day": "なし"
    },
    {
        "id": 3,
        // ...
        "notes": "2023年に閉店",
        // --- ▼ Geminiによって追加された情報 ▼ ---
        "has_lead_wall": null,
        "has_auto_belay": null,
        "has_kids_area": null,
        "business_hours": null,
        "closing_day": "閉店"
    }
]
```
`null`だらけだったデータが、具体的な情報で満たされている。営業時間に定休日、そしてクライマーが知りたかった設備の有無まで。`true`/`false`/`null`というブール型とNull許容の組み合わせで、情報の有無が明確に表現されていた。

「すごい…これがAIの力…」

美咲は、この新しい`gym_data_v2.json`をプロジェクトに組み込むため、`Gym`モデルクラスを早速修正した。

#### **`lib/models/gym.dart` (改修後)**
```dart
class Gym {
  // ... (既存のプロパティ)

  // 新しく追加されたプロパティ
  final bool? hasLeadWall;
  final bool? hasAutoBelay;
  final bool? hasKidsArea;
  final String? businessHours;
  final String? closingDay;

  Gym({
    // ... (既存のコンストラクタ引数)
    
    // 新しい引数
    this.hasLeadWall,
    this.hasAutoBelay,
    this.hasKidsArea,
    this.businessHours,
    this.closingDay,
  });

  factory Gym.fromJson(Map<String, dynamic> json) {
    return Gym(
      // ... (既存のfromJsonロジック)

      // 新しい項目のマッピング
      hasLeadWall: json['has_lead_wall'],
      hasAutoBelay: json['has_auto_belay'],
      hasKidsArea: json['has_kids_area'],
      businessHours: json['business_hours'],
      closingDay: json['closing_day'],
    );
  }
}
```

数人がかりでも数日はかかりそうな作業を、Geminiはわずか数分で終えてしまった。静的だったデータは、AIの偵察によって一気に豊かになり、アプリの価値を大きく引き上げた。

もちろん、AIの情報が100%正しいとは限らない。だからこそ、この後で実装するユーザーによる情報更新機能（Firebase）が活きてくる。

AIによる「面」でのデータ拡充と、ユーザーによる「点」での情報修正・追加。この二つのアプローチを組み合わせることで、美咲のアプリはどこよりも正確で、どこよりも温かいデータベースへと進化を遂げようとしていた。