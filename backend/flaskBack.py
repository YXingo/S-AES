# flaskBack.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from SAES import SAES, generate_random_bin_key, generate_random_ascii_key, xor, bin_to_string

app = Flask(__name__)
CORS(app)  # 允许跨域请求


# 二进制加密
@app.route('/binEncryption', methods=['POST'])
def bin_encryption():
    data = request.get_json()
    plain_text = data.get('binEnPlainText')
    secret_key = data.get('binEnSecretKey')

    if not plain_text or not secret_key:
        return jsonify({'error': '明文或密钥为空'}), 400

    engine = SAES(secret_key)
    cipher_text = engine.encrypt(plain_text)
    return jsonify({'binEnCipherText': cipher_text})


# 二进制解密
@app.route('/binDecryption', methods=['POST'])
def bin_decryption():
    data = request.get_json()
    cipher_text = data.get('binDeCipherText')
    secret_key = data.get('binDeSecretKey')

    if not cipher_text or not secret_key:
        return jsonify({'error': '密文或密钥为空'}), 400

    engine = SAES(secret_key)
    plain_text = engine.decrypt(cipher_text)
    return jsonify({'binDePlainText': plain_text})


# ASCII加密
@app.route('/asciiEncryption', methods=['POST'])
def ascii_encryption():
    data = request.get_json()
    plain_text = data.get('asciiEnPlainText')
    secret_key = data.get('asciiEnSecretKey')

    if not plain_text or not secret_key:
        return jsonify({'error': '明文或密钥为空'}), 400

    # 转换为二进制表示
    binary_plain = ''.join([format(ord(c), '08b') for c in plain_text])
    binary_key = ''.join([format(ord(c), '08b') for c in secret_key])

    engine = SAES(binary_key)
    cipher_text = engine.encrypt(binary_plain)
    # print('>>> cipher_text: ', cipher_text)
    # 转换回ASCII字符串（可能是乱码）
    ascii_cipher = bin_to_string(cipher_text)
    print('>>> ascii_cipher: ', ascii_cipher)
    return jsonify({'asciiEnCipherText': ascii_cipher})


# ASCII解密
@app.route('/asciiDecryption', methods=['POST'])
def ascii_decryption():
    data = request.get_json()
    cipher_text = data.get('asciiDeCipherText')
    secret_key = data.get('asciiDeSecretKey')

    if not cipher_text or not secret_key:
        return jsonify({'error': '密文或密钥为空'}), 400

    # 转换为二进制表示
    binary_cipher = ''.join([format(ord(c), '08b') for c in cipher_text])
    binary_key = ''.join([format(ord(c), '08b') for c in secret_key])

    engine = SAES(binary_key)
    plain_binary = engine.decrypt(binary_cipher)
    # 转换回ASCII字符串
    ascii_plain = bin_to_string(plain_binary)
    return jsonify({'asciiDePlainText': ascii_plain})


# 双重加密
@app.route('/doubleEncryption', methods=['POST'])
def double_encryption():
    data = request.get_json()
    plain_text = data.get('doubleEnPlainText')
    secret_key1 = data.get('doubleEnSecretKey1')
    secret_key2 = data.get('doubleEnSecretKey2')

    if not plain_text or not secret_key1 or not secret_key2:
        return jsonify({'error': '明文或密钥为空'}), 400

    # 第一轮加密
    engine1 = SAES(secret_key1)
    intermediate = engine1.encrypt(plain_text)
    # 第二轮加密
    engine2 = SAES(secret_key2)
    final_cipher = engine2.encrypt(intermediate)

    return jsonify({'doubleEnCipherText': final_cipher})


# 双重解密
@app.route('/doubleDecryption', methods=['POST'])
def double_decryption():
    data = request.get_json()
    cipher_text = data.get('doubleDeCipherText')
    secret_key1 = data.get('doubleDeSecretKey1')
    secret_key2 = data.get('doubleDeSecretKey2')

    if not cipher_text or not secret_key1 or not secret_key2:
        return jsonify({'error': '密文或密钥为空'}), 400

    # 逆第二轮解密
    engine2 = SAES(secret_key2)
    intermediate = engine2.decrypt(cipher_text)
    # 逆第一轮解密
    engine1 = SAES(secret_key1)
    plain_text = engine1.decrypt(intermediate)

    return jsonify({'doubleDePlainText': plain_text})


# 三重加密
@app.route('/tripleEncryption', methods=['POST'])
def triple_encryption():
    data = request.get_json()
    plain_text = data.get('tripleEnPlainText')
    secret_key1 = data.get('tripleEnSecretKey1')
    secret_key2 = data.get('tripleEnSecretKey2')
    secret_key3 = data.get('tripleEnSecretKey3')

    if not plain_text or not secret_key1 or not secret_key2 or not secret_key3:
        return jsonify({'error': '明文或密钥为空'}), 400

    # 第一轮加密
    engine1 = SAES(secret_key1)
    intermediate1 = engine1.encrypt(plain_text)
    # 第二轮加密
    engine2 = SAES(secret_key2)
    intermediate2 = engine2.encrypt(intermediate1)
    # 第三轮加密
    engine3 = SAES(secret_key3)
    final_cipher = engine3.encrypt(intermediate2)

    return jsonify({'tripleEnCipherText': final_cipher})


# 三重解密
@app.route('/tripleDecryption', methods=['POST'])
def triple_decryption():
    data = request.get_json()
    cipher_text = data.get('tripleDeCipherText')
    secret_key1 = data.get('tripleDeSecretKey1')
    secret_key2 = data.get('tripleDeSecretKey2')
    secret_key3 = data.get('tripleDeSecretKey3')

    if not cipher_text or not secret_key1 or not secret_key2 or not secret_key3:
        return jsonify({'error': '密文或密钥为空'}), 400

    # 逆第三轮解密
    engine3 = SAES(secret_key3)
    intermediate2 = engine3.decrypt(cipher_text)
    # 逆第二轮解密
    engine2 = SAES(secret_key2)
    intermediate1 = engine2.decrypt(intermediate2)
    # 逆第一轮解密
    engine1 = SAES(secret_key1)
    plain_text = engine1.decrypt(intermediate1)

    return jsonify({'tripleDePlainText': plain_text})


# 中间相遇攻击
@app.route('/attack', methods=['POST'])
def attack():
    data = request.get_json()
    cipher_text = data.get('attackCipherText')
    plain_text = data.get('attackPlainText')

    if not cipher_text or not plain_text:
        return jsonify({'error': '密文或明文为空'}), 400

    # 这里的中间相遇攻击需要具体的算法实现
    # 由于S-AES较为简单，这里假设密码由两个秘密密钥组成
    # 我们将尝试暴力搜索匹配的密钥对

    possible_keys = generate_all_possible_keys()

    for key1 in possible_keys:
        engine1 = SAES(key1)
        intermediate = engine1.encrypt(plain_text)
        for key2 in possible_keys:
            engine2 = SAES(key2)
            if engine2.encrypt(intermediate) == cipher_text:
                return jsonify({
                    'attackSecretKey1': key1,
                    'attackSecretKey2': key2
                })

    return jsonify({'error': '未找到合适的密钥对'}), 400


def generate_all_possible_keys():
    # 生成所有可能的16-bit密钥
    # 注意：总共有65536个可能性，这对于示例来说可能过大
    # 请根据实际需求调整
    keys = []
    for i in range(0, 1 << 16):
        keys.append(format(i, '016b'))
    return keys


# 工作模式加密 (CBC模式)
@app.route('/workEncryption', methods=['POST'])
def work_encryption():
    data = request.get_json()
    plain_text = data.get('workEnPlainText')
    secret_key = data.get('workEnSecretKey')
    iv = data.get('workEnVector')

    if not plain_text or not secret_key or not iv:
        return jsonify({'error': '明文、密钥或IV为空'}), 400

    # 分块处理，每16位一块
    blocks = [plain_text[i:i + 16] for i in range(0, len(plain_text), 16)]
    if len(blocks[-1]) < 16:
        blocks[-1] = blocks[-1].ljust(16, '0')  # 填充

    cipher_blocks = []
    previous = iv
    engine = SAES(secret_key)

    for block in blocks:
        # XOR与前一个密文块或IV
        xored = xor(block, previous)
        # 加密
        cipher = engine.encrypt(xored)
        cipher_blocks.append(cipher)
        previous = cipher

    cipher_text = ''.join(cipher_blocks)
    return jsonify({'workEnCipherText': cipher_text})


# 工作模式解密 (CBC模式)
@app.route('/workDecryption', methods=['POST'])
def work_decryption():
    data = request.get_json()
    cipher_text = data.get('workDeCipherText')
    secret_key = data.get('workDeSecretKey')
    iv = data.get('workDeVector')

    if not cipher_text or not secret_key or not iv:
        return jsonify({'error': '密文、密钥或IV为空'}), 400

    # 分块处理，每16位一块
    blocks = [cipher_text[i:i + 16] for i in range(0, len(cipher_text), 16)]

    plain_blocks = []
    previous = iv
    engine = SAES(secret_key)

    for block in blocks:
        # 解密
        decrypted = engine.decrypt(block)
        # XOR与前一个密文块或IV
        plain = xor(decrypted, previous)
        plain_blocks.append(plain)
        previous = block

    plain_text = ''.join(plain_blocks).rstrip('0')  # 去除填充
    return jsonify({'workDePlainText': plain_text})


# 随机生成二进制密钥
@app.route('/getBinKey', methods=['POST'])
def get_bin_key():
    key = generate_random_bin_key()
    return jsonify({'secretKey': key})


# 随机生成ASCII密钥
@app.route('/getKey', methods=['POST'])
def get_key():
    key = generate_random_ascii_key()
    return jsonify({'secretKey': key})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
