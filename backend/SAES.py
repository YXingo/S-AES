# SAES.py
import random

# S-Box and Inverse S-Box
S_BOX = {
    '0000': '1010',
    '0001': '0100',
    '0010': '1101',
    '0011': '0001',
    '0100': '1000',
    '0101': '0101',
    '0110': '0110',
    '0111': '1011',
    '1000': '1110',
    '1001': '0010',
    '1010': '0000',
    '1011': '0011',
    '1100': '1111',
    '1101': '1001',
    '1110': '0111',
    '1111': '1100',
}

INV_S_BOX = {v: k for k, v in S_BOX.items()}


def xor(a, b):
    if len(a) != len(b):
        raise ValueError("两个输入必须具有相同的长度")
    return ''.join(['0' if bit_a == bit_b else '1' for bit_a, bit_b in zip(a, b)])


def multiply(a, b):
    # 在 GF(2^4) 上实现乘法
    p = 0
    for i in range(4):
        if b & 1:
            p ^= a
        carry = a & 0x8
        a <<= 1
        if carry:
            a ^= 0x13  # 模多项式 x^4 + x + 1
        b >>= 1
    return p & 0xF  # 只保留 4 位


class SAES:
    def __init__(self, key):
        if len(key) != 16 or not all(c in '01' for c in key):
            raise ValueError("密钥必须是16位的二进制字符串")
        self.key = key  # 16-bit key as string
        self.keys = self.key_schedule(key)
        print(f'Round keys: {self.keys}')

    def key_schedule(self, key):
        # 生成初始子密钥
        w = [key[:8], key[8:]]
        for i in range(4):  # 生成 w2 到 w5
            temp = w[-1]
            temp = self.key_schedule_core(temp, i)
            w.append(xor(w[-2], temp))
        # 将六个 8 位的子密钥组合成三个 16 位的轮密钥
        if len(w) < 6:
            raise ValueError(f'生成的子密钥不足，当前长度: {len(w)}')
        round_keys = [w[0] + w[1], w[2] + w[3], w[4] + w[5]]
        return round_keys

    def key_schedule_core(self, word, iteration):
        # Rotate nibbles
        word = word[4:] + word[:4]
        # Substitute using S_BOX
        word = ''.join([S_BOX[word[i:i + 4]] for i in range(0, len(word), 4)])
        # XOR with RCON
        RCON = ['1000', '0011', '0100', '0010']  # 对应4次迭代
        if iteration >= len(RCON):
            raise ValueError(f"RCON 没有定义第 {iteration} 轮的值")
        word = xor(word, RCON[iteration] + '0000')
        return word

    def add_round_key(self, state, key):
        return xor(state, key)

    def substitute_nibbles(self, state):
        substituted = ''.join([S_BOX[state[i:i + 4]] for i in range(0, len(state), 4)])
        return substituted

    def inverse_substitute_nibbles(self, state):
        substituted = ''.join([INV_S_BOX[state[i:i + 4]] for i in range(0, len(state), 4)])
        return substituted

    def shift_rows(self, state):
        """
        Shift the rows of the state.
        [s0 s1]
        [s2 s3] -> [s0 s1]
                   [s3 s2]
        """
        return state[:8] + state[12:] + state[8:12]

    def inverse_shift_rows(self, state):
        """
        Inverse Shift Rows of the state.
        [s0 s1]
        [s3 s2] -> [s0 s1]
                   [s2 s3]
        """
        return state[:8] + state[12:] + state[8:12]

    def mix_columns(self, state):
        # 分割状态为两列
        s0 = state[0:4]
        s1 = state[4:8]
        s2 = state[8:12]
        s3 = state[12:16]

        a = int(s0, 2)
        b = int(s1, 2)
        c = int(s2, 2)
        d = int(s3, 2)

        # MixColumns 使用矩阵 [1 4; 4 1]
        c0 = multiply(a, 1) ^ multiply(c, 4)
        c1 = multiply(b, 1) ^ multiply(d, 4)
        c2 = multiply(a, 4) ^ multiply(c, 1)
        c3 = multiply(b, 4) ^ multiply(d, 1)

        # 保证每个值为4位
        c0_bin = f'{c0:04b}'
        c1_bin = f'{c1:04b}'
        c2_bin = f'{c2:04b}'
        c3_bin = f'{c3:04b}'

        mixed = c0_bin + c1_bin + c2_bin + c3_bin
        return mixed

    def inverse_mix_columns(self, state):
        # 分割状态为两列
        s0 = state[0:4]
        s1 = state[4:8]
        s2 = state[8:12]
        s3 = state[12:16]

        a = int(s0, 2)
        b = int(s1, 2)
        c = int(s2, 2)
        d = int(s3, 2)

        # Inverse MixColumns 使用矩阵 [9 2; 2 9]
        c0 = multiply(a, 9) ^ multiply(c, 2)
        c1 = multiply(b, 9) ^ multiply(d, 2)
        c2 = multiply(a, 2) ^ multiply(c, 9)
        c3 = multiply(b, 2) ^ multiply(d, 9)

        # 保证每个值为4位
        c0_bin = f'{c0:04b}'
        c1_bin = f'{c1:04b}'
        c2_bin = f'{c2:04b}'
        c3_bin = f'{c3:04b}'

        mixed = c0_bin + c1_bin + c2_bin + c3_bin
        return mixed

    def encrypt(self, plaintext):
        if len(plaintext) != 16 or not all(c in '01' for c in plaintext):
            raise ValueError("明文必须是16位的二进制字符串")

        state = plaintext
        print(f'Initial state: {state}, length: {len(state)}')

        # Round 0
        state = self.add_round_key(state, self.keys[0])
        print(f'After add_round_key 0: {state}, length: {len(state)}')

        # Round 1
        state = self.substitute_nibbles(state)
        print(f'After substitute_nibbles: {state}, length: {len(state)}')

        state = self.shift_rows(state)
        print(f'After shift_rows: {state}, length: {len(state)}')

        state = self.mix_columns(state)
        print(f'After mix_columns: {state}, length: {len(state)}')

        state = self.add_round_key(state, self.keys[1])
        print(f'After add_round_key 1: {state}, length: {len(state)}')

        # Round 2
        state = self.substitute_nibbles(state)
        print(f'After substitute_nibbles: {state}, length: {len(state)}')

        state = self.shift_rows(state)
        print(f'After shift_rows: {state}, length: {len(state)}')

        state = self.add_round_key(state, self.keys[2])
        print(f'After add_round_key 2: {state}, length: {len(state)}')

        return state

    def decrypt(self, ciphertext):
        if len(ciphertext) != 16 or not all(c in '01' for c in ciphertext):
            raise ValueError("密文必须是16位的二进制字符串")

        state = ciphertext
        print(f'Cipher text: {state}, length: {len(state)}')

        # Round 2
        state = self.add_round_key(state, self.keys[2])
        print(f'After add_round_key 2: {state}, length: {len(state)}')

        state = self.inverse_shift_rows(state)
        print(f'After inverse_shift_rows: {state}, length: {len(state)}')

        state = self.inverse_substitute_nibbles(state)
        print(f'After inverse_substitute_nibbles: {state}, length: {len(state)}')

        # Round 1
        state = self.add_round_key(state, self.keys[1])
        print(f'After add_round_key 1: {state}, length: {len(state)}')

        state = self.inverse_mix_columns(state)
        print(f'After inverse_mix_columns: {state}, length: {len(state)}')

        state = self.inverse_shift_rows(state)
        print(f'After inverse_shift_rows: {state}, length: {len(state)}')

        state = self.inverse_substitute_nibbles(state)
        print(f'After inverse_substitute_nibbles: {state}, length: {len(state)}')

        # Round 0
        state = self.add_round_key(state, self.keys[0])
        print(f'After add_round_key 0: {state}, length: {len(state)}')

        return state



def string_to_bin(s, bits=16):
    return bin(int.from_bytes(s.encode(), 'big'))[2:].zfill(bits)


def bin_to_string(b):
    try:
        return int(b, 2).to_bytes((len(b) + 7) // 8, 'big').decode('latin1')
    except Exception as e:
        print(f"解码错误: {e}")
        return b


def shift_left(s, n):
    return s[n:] + s[:n]


def generate_random_bin_key(bits=16):
    return ''.join(random.choice(['0', '1']) for _ in range(bits))


def generate_random_ascii_key(bits=16):
    # Convert bits to bytes
    n = bits // 8
    return ''.join([chr(random.randint(32, 126)) for _ in range(n)])



if __name__ == '__main__':
    # plain_text = '1000110101011100'
    # secret_key = '1000100111000100'
    # engine = SAES(secret_key)
    # cipher_text = engine.encrypt(plain_text)
    # print(f'Cipher text: {cipher_text}\n')
    #
    # new_plain_text = engine.decrypt(cipher_text)
    # print(f'New plain text: {new_plain_text}')

    print(bin_to_string('1111111111111111'))

