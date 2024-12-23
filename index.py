import calendar
from datetime import datetime
from flask import Flask, Response

app = Flask(__name__)

@app.route("/calendar")
def monthly_block_calendar():
    #== 月情報と当日 ==#
    now = datetime.now()
    year = now.year
    month = now.month
    today = now.day
    
    #== カレンダ設定: 月曜始まり ==#
    cal = calendar.TextCalendar(firstweekday=0)  # 0=Monday, 6=Sunday
    month_matrix = cal.monthdayscalendar(year, month)  # [[日1週目], [日2週目], ...]

    #== レイアウト設定 ==#
    cell_w = 50
    cell_h = 50
    rows = len(month_matrix)
    cols = 7  # 月曜始まりで1行あたり7列
    svg_w = cell_w * cols
    svg_h = cell_h * rows

    #== SVGのヘッダ ==#
    svg_parts = [
        f'<svg width="{svg_w}" height="{svg_h}" ',
        '     xmlns="http://www.w3.org/2000/svg"',
        '     xmlns:xlink="http://www.w3.org/1999/xlink">',
        # 背景を白にしたい場合の例
        f'<rect width="{svg_w}" height="{svg_h}" fill="white" />'
    ]
    
    #== 各セルに日付を配置 ==#
    for row_idx, week in enumerate(month_matrix):
        for col_idx, day_num in enumerate(week):
            if day_num == 0:
                # 0は当該月でない日付なので表示しない
                continue
            
            # セルの中央座標
            cx = col_idx * cell_w + cell_w/2
            cy = row_idx * cell_h + cell_h/2
            
            # 当日の場合は赤色の円を描画
            if day_num == today:
                # 円の半径は適宜調整
                r = min(cell_w, cell_h) * 0.3
                svg_parts.append(
                    f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="red" />'
                )
            
            # 日付文字を配置
            # テキストの配置補正(上下左右のバランス)は適宜微調整
            svg_parts.append(
                f'<text x="{cx}" y="{cy + 5}" font-size="16" text-anchor="middle" '
                f' dominant-baseline="middle" fill="black">'
                f'{day_num}</text>'
            )

    #== SVG閉じタグ ==#
    svg_parts.append('</svg>')
    svg_str = "\n".join(svg_parts)
    
    return Response(svg_str, mimetype='image/svg+xml')


if __name__ == "__main__":
    app.run(debug=True)
