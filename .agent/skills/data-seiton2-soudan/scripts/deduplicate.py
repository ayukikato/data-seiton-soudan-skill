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

        # 1. 「イベント名」を相談日程の代わりとして使用（数値が大きいほど新しいと仮定）
        # ※本来は日付列が望ましいが、サンプルデータでは「イベント名」が日程の順序を示しているように見える
        # ただし 0.0 は未成立や不明の可能性があるため、後で処理
        
        # 2. 相談の成立判断
        # サンプルデータにはステータス列がないため、
        # 「イベント名」が 0.0 を「未成立/未相談」、それ以外を「成立」とみなす
        df_valid = df[df['イベント名'] > 0].copy()
        
        # もし相談成立データが1つもない場合は、全データから最新を選ぶ
        if len(df_valid) == 0:
            print("警告: 相談成立（イベント名 > 0）のデータが見つかりません。全データから最新を抽出します。")
            df_valid = df.copy()

        # 3. 重複排除
        # 整理番号でグループ化し、イベント名（日程）が最大（最新）のものを残す
        # 同じイベント名の場合は、最後の行を採用
        df_sorted = df_valid.sort_values(by=['整理番号', 'イベント名'], ascending=[True, False])
        df_unique = df_sorted.drop_duplicates(subset='整理番号', keep='first')

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
