import pandas as pd
import numpy as np

# 設定
input_file = "/Users/katouayuki/Desktop/skills/2026入試_個別の相談記録一覧_相談番号不問2026発行20260106_041922_947.xlsx"
output_file = "/Users/katouayuki/Desktop/skills/2026相談データ_分析用_整頓済.csv"

def clean_data():
    try:
        # データの読み込み
        df = pd.read_excel(input_file)
        cols = df.columns
        
        # ターゲットデータの作成
        target_data = pd.DataFrame()
        
        # 1. 重要項目の抽出
        target_data['整理番号'] = df.iloc[:, 1]
        target_data['イベント名'] = df.iloc[:, 3]
        target_data['地区名'] = df.iloc[:, 11]
        target_data['中学校名'] = df.iloc[:, 12]
        
        # 内申点の特定 (「内申」という文字が含まれる列を探す)
        naishin_cols = [c for c in df.columns if "内申" in str(c)]
        if naishin_cols:
            # 調査で見つかった内申点（おそらく16-24あたり）を数値化して合計
            target_data['内申点_合計'] = df[naishin_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1)
        else:
            # キーワードで見つからない場合はインデックスで推測（前回の調査から16:25付近）
            target_data['内申点_合計'] = df.iloc[:, 16:25].apply(pd.to_numeric, errors='coerce').sum(axis=1)

        # 偏差値
        target_data['偏差値_平均'] = pd.to_numeric(df.iloc[:, 76], errors='coerce')
        
        # 志望コース・区分 (79: コース区分, 80: 単願/併願 と推測)
        target_data['志望コース'] = df.iloc[:, 79]
        # 「単願」「併願」というキーワードを列名から探す
        tangan_col_idx = -1
        for i, col in enumerate(df.columns):
            if "単願" in str(col) or "併願" in str(col) or "区分" in str(col):
                if i > 70: # 偏差値エリアより後ろ
                    tangan_col_idx = i
                    break
        
        if tangan_col_idx != -1:
            target_data['単願併願'] = df.iloc[:, tangan_col_idx]
        else:
            target_data['単願併願'] = df.iloc[:, 80] if len(df.columns) > 80 else "不明"

        # 2. 匿名化（氏名カラムは含めないことで達成）
        # 氏名関連カラムのインデックス: 4, 5, 6, 7
        
        # 3. CSV出力
        target_data.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"✅ ファイルを保存しました: {output_file}")
        
        # 4. 分析（サマリー表示）
        print("\n--- 分析サマリー ---")
        
        # 志望コースごとの内申点・偏差値平均
        # 欠損値を除去して集計
        analysis_df = target_data.dropna(subset=['志望コース'])
        course_summary = analysis_df.groupby('志望コース')[['内申点_合計', '偏差値_平均']].mean()
        print("\n[志望コース別平均]")
        print(course_summary)
        
        # 地域別の相談者数（上位10件）
        area_summary = target_data['地区名'].value_counts().head(10)
        print("\n[地域別(地区名)相談者数 (TOP 10)]")
        print(area_summary)
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    clean_data()
