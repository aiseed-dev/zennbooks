import os
import re
import subprocess
import argparse
from typing import List

def correct_bolding_logic(original_content: str) -> str:
    """
    GFM互換性のない太字記法を修正するコアロジック。
    例: **「テキスト」** -> 「**テキスト**」
    """
    # 正規表現パターン: ** と ** で囲まれた、中身のテキストをキャプチャする
    # re.DOTALLフラグにより、.（ドット）が改行にもマッチするようになります
    pattern = re.compile(r'\*\*(.*?)\*\*', re.DOTALL)
    
    def replacer(match: re.Match) -> str:
        """re.subに渡すための置換用関数"""
        # マッチした全体（例: **「テキスト」**）
        full_match = match.group(0)
        # マッチした中身（例: 「テキスト」）
        inner_text = match.group(1)

        if not inner_text:
            return full_match

        left_brackets = '「（『【'
        right_brackets = '」）』】'

        prefix = ''
        suffix = ''

        # 条件A: 最初の文字が左括弧クラスか？
        if inner_text.startswith(tuple(left_brackets)):
            prefix = inner_text[0]
            inner_text = inner_text[1:]

        # 条件B: 最後の文字が右括弧クラスか？
        # inner_textが空になっていないかチェック
        if inner_text and inner_text.endswith(tuple(right_brackets)):
            suffix = inner_text[-1]
            inner_text = inner_text[:-1]
        
        # prefixかsuffixのどちらかが設定された場合のみ、再構築を行う
        if prefix or suffix:
            # f-stringを使って新しい形式を組み立てる
            return f'{prefix}**{inner_text}**{suffix}'
        else:
            # 条件に一致しない場合（通常の太字など）は、一切変更せずにそのまま返す
            return full_match

    return pattern.sub(replacer, original_content)

def get_git_files(repo_path: str) -> List[str]:
    """Gitで管理されているMarkdownファイルの一覧を取得する"""
    try:
        # cwdでコマンドの実行ディレクトリを指定
        result = subprocess.run(
            ['git', 'ls-files', '*.md'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False # エラー時に例外を発生させない
        )
        if result.returncode != 0:
            print(f'❌ git ls-filesの実行に失敗: {result.stderr}')
            return []
        # splitlines()で改行区切りの出力をリストに変換
        return [line for line in result.stdout.splitlines() if line]
    except FileNotFoundError:
        print('❌ Gitコマンドの実行に失敗しました。Gitはインストールされていますか？')
        return []
    except Exception as e:
        print(f'❌ 不明なエラーが発生しました: {e}')
        return []


def fix_markdown_bolding(repo_path: str, dry_run: bool):
    """Markdownファイル内のGFM互換性問題を修正するメイン関数"""
    print('--- Markdown GFM互換性修正プログラム (Python版) ---')
    print(f'🔍 ターゲットディレクトリ: {repo_path}')
    if dry_run:
        print('👕 ドライランモードで実行します。ファイルは変更されません。')
    print('-' * 40)
    
    markdown_files = get_git_files(repo_path)
    if not markdown_files:
        print('📄 処理対象のMarkdownファイルが見つかりませんでした。')
        return

    fixed_files_count = 0
    
    for md_file_relative in markdown_files:
        # os.path.joinでOSに依存しない安全なパス結合を行う
        file_path = os.path.join(repo_path, md_file_relative)
        if not os.path.exists(file_path):
            continue

        try:
            # with構文で安全にファイルを開く。エンコーディングはutf-8を推奨
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            new_content = correct_bolding_logic(original_content)

            # 実際に変更があった場合のみ処理
            if original_content != new_content:
                print(f'❗ GFM互換性の問題を {md_file_relative} で発見。')
                fixed_files_count += 1
                
                if not dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print('   -> ✅ ファイルを修正し、上書き保存しました。')
                else:
                    print('   -> (ドライランのため、変更はスキップしました)')

        except Exception as e:
            print(f'❌ ファイル処理中にエラーが発生しました ({md_file_relative}): {e}')


    print('-' * 40)
    if fixed_files_count > 0:
        if not dry_run:
            print(f'🎉 完了！合計 {fixed_files_count} 個のファイルを修正しました。')
            print('git diff で変更内容を確認し、問題がなければコミット＆プッシュしてください。')
        else:
            print(f'👕 ドライラン完了。合計 {fixed_files_count} 個のファイルで問題が発見されました。')
            print('実際に修正するには、--dry-runオプションを外して再度実行してください。')
    else:
        print('👍 素晴らしい！修正が必要なファイルは見つかりませんでした。')
    print('--- プログラムを終了します ---')

def main():
    """コマンドライン引数を解析し、メイン処理を呼び出す"""
    parser = argparse.ArgumentParser(
        description='Markdownファイル内のGFM互換性のない太字記法を修正します。'
    )
    parser.add_argument(
        '-p', '--path', 
        required=True, 
        help='レビュー対象のリポジトリのパス'
    )
    parser.add_argument(
        '-d', '--dry-run', 
        action='store_true', 
        help='実際にファイルを変更せず、修正対象のファイルを表示するだけ（ドライラン）'
    )
    
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f'❌ エラー: 指定されたパスが見つかりません: {args.path}')
        return
        
    fix_markdown_bolding(args.path, args.dry_run)

# Pythonスクリプトとして直接実行された場合にmain()を呼び出す
if __name__ == '__main__':
    main()