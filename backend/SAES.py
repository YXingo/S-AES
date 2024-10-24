# SAES.py

# S-AES 算法的实现，包括加密和解密函数

# S盒和逆S盒
SBox = [
    0x9, 0x4, 0xA, 0xB,
    0xD, 0x1, 0x8, 0x5,
    0x6, 0x2, 0x0, 0x3,
    0xC, 0xE, 0xF, 0x7
]

SBox_inv = [
    0xA, 0x5, 0x9, 0xB,
    0x1, 0x7, 0x8, 0xF,
    0x6, 0x0, 0x2, 0x3,
    0xC, 0x4, 0xD, 0xE
]

# 轮常量
RCON = [0x80, 0x30]


# GF(2^4)上的乘法
def gf_mult(a, b):
    """在 GF(2^4) 上进行多项式乘法，模多项式为 x^4 + x + 1 (0b10011)"""
    p = 0
    for _ in range(4):
        if b & 0x1:
            p ^= a
        carry = a & 0x8  # 检查最高位
        a <<= 1
        if carry:
            a ^= 0b10011  # 模多项式
        b >>= 1
    return p & 0xF  # 结果为4位


# 子字节替换
def sub_nibbles(state):
    """使用 SBox 对状态中的每个nibble进行替换"""
    return [SBox[nibble] for nibble in state]


def inv_sub_nibbles(state):
    """使用逆 SBox 对状态中的每个nibble进行替换"""
    return [SBox_inv[nibble] for nibble in state]


# 行移位
def shift_rows(state):
    """ShiftRows 操作，交换 s1 和 s3"""
    return [state[0], state[3], state[2], state[1]]


def inv_shift_rows(state):
    """逆 ShiftRows 操作，交换 s1 和 s3"""
    return [state[0], state[3], state[2], state[1]]  # 与 ShiftRows 相同


# 列混合
def mix_columns(state):
    """MixColumns 操作，矩阵 [[1,4],[4,1]]"""
    s0, s1, s2, s3 = state
    s0_prime = s0 ^ gf_mult(4, s2)
    s1_prime = s1 ^ gf_mult(4, s3)
    s2_prime = gf_mult(4, s0) ^ s2
    s3_prime = gf_mult(4, s1) ^ s3
    return [s0_prime, s1_prime, s2_prime, s3_prime]


def inv_mix_columns(state):
    """逆 MixColumns 操作，矩阵 [[9,2],[2,9]]"""
    s0, s1, s2, s3 = state
    s0_prime = gf_mult(9, s0) ^ gf_mult(2, s2)
    s1_prime = gf_mult(9, s1) ^ gf_mult(2, s3)
    s2_prime = gf_mult(2, s0) ^ gf_mult(9, s2)
    s3_prime = gf_mult(2, s1) ^ gf_mult(9, s3)
    return [s0_prime, s1_prime, s2_prime, s3_prime]


# 轮密钥加
def add_round_key(state, key):
    """AddRoundKey 操作，将状态与轮密钥进行异或"""
    return [s ^ k for s, k in zip(state, key)]


# 密钥扩展
def key_expansion(key):
    """密钥扩展函数，输入16位密钥，输出轮密钥列表"""
    # 初始化 w0 到 w5
    w = [0] * 6
    # 分割密钥为 w0 和 w1（8位）
    w[0] = (key >> 8) & 0xFF  # 高8位
    w[1] = key & 0xFF  # 低8位

    # 计算 w2
    temp = w[1]
    temp = ((SBox[temp >> 4] << 4) | SBox[temp & 0x0F]) ^ RCON[0]
    w[2] = w[0] ^ temp

    # 计算 w3
    w[3] = w[2] ^ w[1]

    # 计算 w4
    temp = w[3]
    temp = ((SBox[temp >> 4] << 4) | SBox[temp & 0x0F]) ^ RCON[1]
    w[4] = w[2] ^ temp

    # 计算 w5
    w[5] = w[4] ^ w[3]

    # 生成轮密钥
    k0 = [w[0] >> 4, w[0] & 0xF, w[1] >> 4, w[1] & 0xF]
    k1 = [w[2] >> 4, w[2] & 0xF, w[3] >> 4, w[3] & 0xF]
    k2 = [w[4] >> 4, w[4] & 0xF, w[5] >> 4, w[5] & 0xF]
    return k0, k1, k2


# 加密函数
def encrypt(plaintext, key):
    """
    使用 S-AES 加密16位的明文
    :param plaintext: 16位整数明文
    :param key: 16位整数密钥
    :return: 16位整数密文
    """
    # 将明文转换为状态（4个nibble）
    state = [
        (plaintext >> 12) & 0xF,
        (plaintext >> 8) & 0xF,
        (plaintext >> 4) & 0xF,
        plaintext & 0xF
    ]

    # 密钥扩展
    k0, k1, k2 = key_expansion(key)

    # 初始轮密钥加
    state = add_round_key(state, k0)

    # 第一轮
    state = sub_nibbles(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, k1)

    # 第二轮
    state = sub_nibbles(state)
    state = shift_rows(state)
    state = add_round_key(state, k2)

    # 将状态转换回16位整数
    ciphertext = (state[0] << 12) | (state[1] << 8) | (state[2] << 4) | state[3]
    return ciphertext


# 解密函数
def decrypt(ciphertext, key):
    """
    使用 S-AES 解密16位的密文
    :param ciphertext: 16位整数密文
    :param key: 16位整数密钥
    :return: 16位整数明文
    """
    # 将密文转换为状态（4个nibble）
    state = [
        (ciphertext >> 12) & 0xF,
        (ciphertext >> 8) & 0xF,
        (ciphertext >> 4) & 0xF,
        ciphertext & 0xF
    ]

    # 密钥扩展
    k0, k1, k2 = key_expansion(key)

    # 初始轮密钥加
    state = add_round_key(state, k2)

    # 第一轮
    state = inv_shift_rows(state)
    state = inv_sub_nibbles(state)
    state = add_round_key(state, k1)
    state = inv_mix_columns(state)

    # 第二轮
    state = inv_shift_rows(state)
    state = inv_sub_nibbles(state)
    state = add_round_key(state, k0)

    # 将状态转换回16位整数
    plaintext = (state[0] << 12) | (state[1] << 8) | (state[2] << 4) | state[3]
    return plaintext


if __name__ == '__main__':
    # 测试加密
    plaintext = '6bc1'  # 16 进制字符串
    key = '3a94'  # 16 进制字符串
    print(encrypt(int(plaintext, 16), int(key, 16)))
