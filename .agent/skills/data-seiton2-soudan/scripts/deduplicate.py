import pandas as pd
import sys
import os

def process_data(input_file, output_file):
    try:
        # CSV読み込み
        # Shift-JISまたはCP932で読み込む（日本のExcel製CSVで一般的）
        try:
            df = pd.read_csv(input_file, encoding='cp932')
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='utf-8')

        print(f"元のデータ件数: {len(df)}")

        # 1. 相談の成立フラグを作成（イベント名 > 0 を成立とみなす）
        df['is_valid'] = df['イベント名'] > 0

        # 2. 優先順位を付けて並べ替え
        # 第1優先: 相談成立 (True > False の順)
        # 第2優先: イベント名 (降順: 大きい/新しいものが先)
        df_sorted = df.sort_values(
            by=['整理番号', 'is_valid', 'イベント名'],
            ascending=[True, False, False]
        )

        # 3. 重複排除
        # 整理番号ごとに、最も優先順位の高い1行（成立最新 or 未成立のみならその1枚）だけを残す
        df_unique = df_sorted.drop_duplicates(subset='整理番号', keep='first').copy()

        # 作業用列を削除
        df_unique = df_unique.drop(columns=['is_valid'])

        print(f"重複排除後のデータ件数: {len(df_unique)}")

        # 結果を保存
        df_unique.to_csv(output_file, index=False, encoding='cp932')
        print(f"結果を保存しました: {output_file}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    input_path = "/Users/katouayuki/Desktop/skills/2026相談データ_分析用_整頓済.csv"
    output_path = "/Users/katouayuki/Desktop/skills/2026相談データ_分析用_名寄せ済.csv"
    process_data(input_path, output_path)
