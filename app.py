from flask import Flask, request, render_template_string
from datetime import datetime
from flask import redirect, url_for, session

app = Flask(__name__)
app.secret_key = '123456'  # 請換成你自己的安全密鑰

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>巴渝商店</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .alert-top {
            font-size: 1.3rem;
            font-weight: bold;
            text-align: center;
        }
    </style>
</head>
<body class="bg-light">
<div class="container py-4">
    {% if submitted %}
    <div class="alert alert-success alert-top">✅ 訂單已送出成功！</div>
    {% endif %}
    <h1 class="text-center mb-4">🛒 巴渝商店</h1>
    <form method="POST" class="bg-white p-4 rounded shadow-sm">
        <div class="mb-3">
            <label class="form-label">姓名 *</label>
            <input type="text" name="name" class="form-control" required>
        </div>
        <div class="mb-3">
            <label class="form-label">電話 *</label>
            <input type="tel" name="phone" class="form-control" required>
        </div>
        <div class="mb-3">
            <label class="form-label">商品選擇</label><br>
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" name="product" value="巴渝臘肉" id="product1">
                <label class="form-check-label" for="product1">巴渝臘肉</label>
                <input type="number" name="quantity_巴渝臘肉" class="form-control mt-1" placeholder="數量" min="0">
            </div>
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" name="product" value="巴渝香腸" id="product2">
                <label class="form-check-label" for="product2">巴渝香腸</label>
                <input type="number" name="quantity_巴渝香腸" class="form-control mt-1" placeholder="數量" min="0">
            </div>
        </div>
        <div class="mb-3">
            <label class="form-label">7-11 門市地址 <span class="text-muted">(7-11 配送，滿3000免運費)</span></label>
            <input type="text" name="address" class="form-control" placeholder="請填寫門市地址">
        </div>
        <div class="mb-3">
            <label class="form-label">備註</label>
            <textarea name="notes" class="form-control" rows="1" placeholder="其他需求..."></textarea>
        </div>
        <button type="submit" class="btn btn-primary w-100">送出訂單</button>
    </form>
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def shop():
    submitted = session.pop('submitted', False)

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        notes = request.form.get('notes', '')
        address = request.form.get('address', '')
        products = request.form.getlist('product')

        order_lines = [f"📝 訂單時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]
        order_lines.append(f"姓名：{name}")
        order_lines.append(f"電話：{phone}")
        for p in products:
            qty = request.form.get(f'quantity_{p}', '0')
            order_lines.append(f"✔️ {p} x {qty}")
        if address.strip():
            order_lines.append(f"📦 配送地址（7-11）：{address}")
            if any(loc in address for loc in ['彰化', '花壇', '鹿港']):
                order_lines.append("🚗 可親自配送地區")
        if notes.strip():
            order_lines.append(f"備註：{notes}")
        order_lines.append('-' * 30)

        with open('orders.txt', 'a', encoding='utf-8') as f:
            f.write('\n'.join(order_lines) + '\n')

        session['submitted'] = True
        return redirect(url_for('shop'))

    return render_template_string(HTML_TEMPLATE, submitted=submitted)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
