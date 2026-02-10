from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# Cấu hình thư mục lưu ảnh
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_and_process():
    # --- PHẦN 1: NHẬN VÀ LƯU ẢNH (Ưu điểm của hàm 1) ---
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'Không có ảnh gửi lên'}), 400

    file = request.files['image']
    
    # Tạo tên file theo thời gian để không bị trùng
    filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Lưu ảnh xuống ổ cứng máy trạm (Quan trọng để sau này train AI)
    file.save(filepath)
    print(f"--> [Server] Đã lưu ảnh tại: {filepath}")

    # --- PHẦN 2: XỬ LÝ AI (Giả lập logic của hàm 2) ---
    # Tại đây, sau này bạn sẽ gọi hàm AI: price = AI_model.predict(filepath)
    # Hiện tại mình giả lập giá tiền ngẫu nhiên hoặc cố định
    fuel_price = 55000 
    
    # --- PHẦN 3: TẠO MÃ QR TRẢ VỀ (Ưu điểm của hàm 2) ---
    # Tạo nội dung QR
    momo_content = f"2|99|0909xxxxxx|Name|email@gmail.com|0|0|{fuel_price}|Thanh toan xang"
    
    # Tạo hình ảnh QR trong bộ nhớ RAM (không cần lưu ra ổ cứng)
    qr = qrcode.make(momo_content)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    
    # Mã hóa ảnh QR thành chuỗi Base64 để gửi về điện thoại
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    # --- PHẦN 4: TRẢ KẾT QUẢ VỀ CLIENT ---
    return jsonify({
        'status': 'success',
        'price': fuel_price,      # Để hiện số tiền
        'qr_image': qr_base64,    # Để hiện hình mã QR
        'message': 'Đã nhận ảnh và xử lý thành công'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)