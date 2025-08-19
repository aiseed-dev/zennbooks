import yaml
import os

# --- 設定 ---
CONFIG_FILE = 'config.yaml'
BOOK_DIR = 'windows-ai-app'

def create_zenn_chapter_files():
    """
    config.yamlを読み込み、Zennの本の各章のMarkdownファイルを生成します。
    """
    # 1. config.yamlの存在を確認
    path = os.path.join(BOOK_DIR, CONFIG_FILE)
    if not os.path.exists(path):
        print(f"エラー: 設定ファイル '{CONFIG_FILE}' が見つかりませんでした。")
        return

    # 2. config.yamlを読み込む
    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"✅ '{CONFIG_FILE}' を正常に読み込みました。")
    except Exception as e:
        print(f"エラー: '{CONFIG_FILE}' の読み込み中にエラーが発生しました: {e}")
        return

    # 3. 'chapters'キーから章のリストを取得
    chapters = config.get('chapters')
    if not chapters or not isinstance(chapters, list):
        print(f"エラー: '{CONFIG_FILE}' に 'chapters' のリストが見つかりません。")
        return

    # 5. 各章のファイルを作成
    for i, chapter_slug in enumerate(chapters):
        file_path = os.path.join(BOOK_DIR, f"{chapter_slug}.md")

        # ファイルが既に存在する場合はスキップ
        if os.path.exists(file_path):
            print(f"🔵 スキップ: '{file_path}' は既に存在します。")
            continue


        # Zennのフロントマターを含むコンテンツを作成

        # ファイルに書き込む
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("---\ntitle: ")         
            print(f"🎉 作成成功: '{file_path}'")
        except Exception as e:
            print(f"❌ 作成失敗: '{file_path}' ({e})")

    print("-" * 30)
    print("すべての処理が完了しました。")

# --- メイン処理 ---
if __name__ == "__main__":
    create_zenn_chapter_files()
