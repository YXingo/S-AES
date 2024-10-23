# flaskBack.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import SAES

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


# 加密接口
@app.route('/encrypt', methods=['POST'])
def handle_encryption():
    data = request.json
    plain_text = data.get('plainText')
    key = data.get('key')

    if not plain_text or not key:
        return jsonify({'error': '缺少明文或密钥'}), 400

    try:
        # 将明文和密钥从十六进制字符串转换为整数
        plaintext_int = int(plain_text, 16)
        key_int = int(key, 16)

        # 调用加密函数
        cipher_int = SAES.encrypt(plaintext_int, key_int)

        # 将密文转换为十六进制字符串
        cipher_text = format(cipher_int, '04x')  # 4个十六进制字符（16位）

        return jsonify({'cipherText': cipher_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 解密接口
@app.route('/decrypt', methods=['POST'])
def handle_decryption():
    data = request.json
    cipher_text = data.get('cipherText')
    key = data.get('key')

    if not cipher_text or not key:
        return jsonify({'error': '缺少密文或密钥'}), 400

    try:
        # 将密文和密钥从十六进制字符串转换为整数
        ciphertext_int = int(cipher_text, 16)
        key_int = int(key, 16)

        # 调用解密函数
        plaintext_int = SAES.decrypt(ciphertext_int, key_int)

        # 将明文转换为十六进制字符串
        plain_text = format(plaintext_int, '04x')  # 4个十六进制字符（16位）

        return jsonify({'plainText': plain_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 运行 Flask 应用
if __name__ == '__main__':
    app.run(debug=DEBUG)
