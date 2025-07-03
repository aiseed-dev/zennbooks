---
title: "第11章：【実践】データをグラフに！MatplotlibとStreamlitで動くWebアプリを作ろう"
---

おめでとうございます！あなたはデータを加工し、レポートとして見せるスキルを身につけました。しかし、データが持つ本当の物語を伝えるには、**「視覚化（ビジュアライゼーション）」**、つまりグラフの力が不可欠です。

この章では、Pythonで美しいグラフを作成するための定番ライブラリ**「Matplotlib」**と、そのグラフを驚くほど簡単にインタラクティブなWebアプリにしてしまう魔法のツール**「Streamlit」**を学びます。

これができれば、あなたは単にデータを処理するだけでなく、**データから得られた知見（インサイト）を、誰もが直感的に理解できる形で共有する**ことができるようになります。データサイエンティストとしての大きな一歩ですよ！

### なぜグラフとWebアプリなのか？

*   **Matplotlib**: Pythonにおけるグラフ描画の「お父さん」のような存在。棒グラフ、折れ線グラフ、円グラフ、散布図など、あらゆる種類のグラフを自由に描くことができます。数字の羅列だけでは見えないデータの傾向やパターンを、一瞬で明らかにしてくれます。
*   **Streamlit**: 「Pythonスクリプトを、たった数行のコードでWebアプリに変身させる」という、まさに魔法のフレームワークです。複雑なHTMLやJavaScriptの知識は一切不要。あなたが書いたPythonコードが、そのままWebページ上のスライダーやボタン、そして美しいグラフとして動き出します。

### 1. 今回のゴール：ジムの分布を地図上にプロットするWebアプリ

第9章で作成した`gym_list.json`には、各ジムの「緯度」と「経度」のデータが入っています。このデータを使って、**徳島県の地図上にジムの位置をプロットするインタラクティブなWebアプリ**を、AIと一緒に作ってみましょう！

### 2. AIへの指示（プロンプト）を考えよう 🗣️
さあ、AIに私たちのアイデアを伝えます。今回は少し複雑なので、段階的に指示するのがコツです。

**あなたからAIへの指示（プロンプト）例:**
```
Pythonで、StreamlitとMatplotlibを使ったWebアプリを作成したいです。
【要件】
1. 'gym_list.json' をPandasで読み込み、DataFrameを作成してください。
2. Matplotlibを使い、緯度(latitude)と経度(longitude)のデータを使って散布図（scatter plot）を作成してください。
3. この散布図を、StreamlitのWebページに表示してください。
4. アプリのタイトルは「徳島県ジムマップ」としてください。
```
### 3. AIが生成したコードと実行準備 🛠️

AIは、これらのライブラリを組み合わせた、以下のようなコードを生成してくれるでしょう。
**AIが生成したコード例 (`dashboard_app.py`):**

```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib # Matplotlibの日本語化

# --- アプリの基本設定 ---
st.set_page_config(layout="wide") # ページをワイド表示にする
st.title('徳島県 ジムマップ')
st.write('JSONデータからジムの位置をプロットした簡易的なマップです。')

# --- データ読み込み ---
# エラーハンドリングとキャッシュ機能を追加
@st.cache_data
def load_data(json_path):
    try:
        df = pd.read_json(json_path)
        # 緯度・経度が数値型であることを確認
        df['緯度'] = pd.to_numeric(df['緯度'], errors='coerce')
        df['経度'] = pd.to_numeric(df['経度'], errors='coerce')
        df.dropna(subset=['緯度', '経度'], inplace=True)
        return df
    except Exception as e:
        st.error(f"データの読み込み中にエラーが発生しました: {e}")
        return pd.DataFrame()

df_gyms = load_data('gym_list.json')

if not df_gyms.empty:
    # --- 地図プロット ---
    fig, ax = plt.subplots(figsize=(10, 10))
    
    ax.scatter(df_gyms['経度'], df_gyms['緯度'], alpha=0.7, c='blue', s=50)
    ax.set_title('ジムの分布')
    ax.set_xlabel('経度')
    ax.set_ylabel('緯度')
    ax.grid(True)
    
    # 各点に店舗名を表示（少し見にくくなる可能性あり）
    for i, row in df_gyms.iterrows():
        ax.text(row['経度'], row['緯度'], row['店舗名'], fontsize=9)
    
    # StreamlitにMatplotlibのグラフを表示
    st.pyplot(fig)

    # --- データテーブル表示 ---
    st.write('### データ一覧')
    st.dataframe(df_gyms)
else:
    st.warning('表示するデータがありません。')
```
**実行前の準備:**
必要なライブラリをインストールします。PyCharmのターミナルで実行してください。

```bash
pip install streamlit pandas matplotlib japanize-matplotlib
```
### 4. 実行とインタラクティブなWebアプリの体験！ ✅
1.  **ファイル作成**: PyCharmで `dashboard_app.py` というファイル名で上記のコードを保存します。`gym_list.json` が同じフォルダにあることを確認してください。
2.  **アプリ起動**: PyCharmのターミナルで、以下のコマンドを実行してStreamlitアプリを起動します。
    ```bash
    streamlit run dashboard_app.py
    ```
3.  **ブラウザで確認**: 自動的にWebブラウザが立ち上がり、**「徳島県 ジムマップ」というタイトルが付いた、あなたのWebアプリケーション**が表示されます！
    *   散布図が表示され、各ジムの位置がプロットされているはずです。
    *   グラフの下には、ソートやフィルタリングが可能なインタラクティブなデータテーブルも表示されています。
>
---

**お疲れ様でした！あなたはデータを分析し、動くWebアプリとして公開する力を手に入れました！**
>
これこそが、データサイエンスの成果を多くの人に届けるための、モダンで強力なワークフローです。面倒なWeb開発の知識がなくても、Pythonだけでここまでできることに驚いたのではないでしょうか？
>
さて、Pythonサイドの準備は本当に万端です。データを作り、加工し、分析し、そしてWebアプリとして公開する。この一連の流れをマスターしたあなたなら、次の冒険もきっと乗り越えられます。
>
次の章から、いよいよ**Flutterでのスマホアプリ開発**が始まります！最高のクライマックスに向けて、出発しましょう！🚀