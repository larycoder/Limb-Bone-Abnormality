from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Đường dẫn đến file CSV mẫu
csv_path = 'HG001.hiseq4000.wes_truseq.50x.R.indels.hg19_multianno.csv'

# Đọc dữ liệu từ file CSV bằng pandas
df = pd.read_csv(csv_path)

@app.route('/', methods=['GET', 'POST'])
def display_csv_columns():
    if request.method == 'POST':
        # Lấy danh sách các cột được chọn từ form
        selected_columns = request.form.getlist('columns')

        # Tạo DataFrame mới chỉ với các cột được chọn
        selected_df = df[selected_columns]
        selected_df=selected_df.head(20)

        # Chuyển đổi DataFrame thành HTML
        table_html = selected_df.to_html(classes='table table-striped', index=False)

        # Render template với dữ liệu HTML
        return render_template('display_columns.html', table_html=table_html, columns=df.columns)

    # Nếu là request GET, hiển thị form chọn cột
    return render_template('select_columns.html', columns=df.columns)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1212, debug=True)
