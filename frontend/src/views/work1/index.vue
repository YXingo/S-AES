<template>
  <el-container class="container">
    <el-header class="header">
      <h2>S-AES加解密系统</h2>
    </el-header>
    <el-main class="main">

      <div class="leftSide">
        <br><br>
        <el-card class="leftCardStyle" shadow="never" :class="{ selectedCard: cardID == 0 }"
                 @click="changeID(0)">二进制加密
        </el-card>
        <el-card class="leftCardStyle" shadow="never" :class="{ selectedCard: cardID == 1 }"
                 @click="changeID(1)">ASCII加密
        </el-card>
        <el-card class="leftCardStyle" shadow="never" :class="{ selectedCard: cardID == 2 }"
                 @click="changeID(2)">双重加密
        </el-card>
        <el-card class="leftCardStyle" shadow="never" :class="{ selectedCard: cardID == 3 }"
                 @click="changeID(3)">三重加密
        </el-card>
        <el-card class="leftCardStyle" shadow="never" :class="{ selectedCard: cardID == 4 }"
                 @click="changeID(4)">中间相遇攻击
        </el-card>
        <el-card class="leftCardStyle" shadow="never" :class="{ selectedCard: cardID == 5 }"
                 @click="changeID(5)">工作模式
        </el-card>
        <el-card class="redLeftCardStyle" shadow="never" style="color: red;" @click="exitSystem">退出系统</el-card>
      </div>

      <div class="divider"></div>
      <div class="rightSide">

        <div class="rightTitle">
          <h2 v-if="cardID == 0" class="title">二进制加密</h2>
          <h2 v-if="cardID == 1" class="title">ASCII加密</h2>
          <h2 v-if="cardID == 2" class="title">双重加密</h2>
          <h2 v-if="cardID == 3" class="title">三重加密</h2>
          <h2 v-if="cardID == 4" class="title">中间相遇攻击</h2>
          <h2 v-if="cardID == 5" class="title">工作模式</h2>
        </div>

        <div class="rightContent">
          <div class="centerInfo">

            <div v-if="cardID == 0" class="input">
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>明文</h3>
                <el-input v-model="binEnPlainText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入明文"/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥</h3>
                <el-input v-model="binEnSecretKey" style="width: 500px; margin-left: 20px;" placeholder="请输入密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getBinKey(binEnSecretKey)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                <el-button style="font-weight: 600;" @click="binEncryption">开始加密</el-button>
                <el-input v-model="binEnCipherText" style="width: 450px; margin-left: 20px;" placeholder=""/>
              </div>

              <br><br>

              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密文</h3>
                <el-input v-model="binDePlainText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入明文"/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥</h3>
                <el-input v-model="binDeSecretKey" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;"
                           @click="getBinKey(binDeSecretKey)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                <el-button style="font-weight: 600;" @click="binDecryption">开始解密</el-button>
                <el-input v-model="binDeCipherText" style="width: 450px; margin-left: 20px;" placeholder=""/>
              </div>
            </div>
            <div v-if="cardID == 1" class="input">
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>明文</h3>
                <el-input v-model="asciiEnPlainText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入明文"/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥</h3>
                <el-input v-model="asciiEnSecretKey" style="width: 500px; margin-left: 20px;" placeholder="请输入密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getKey(asciiEnSecretKey)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                <el-button style="font-weight: 600;" @click="asciiEncryption">开始加密</el-button>
                <el-input v-model="asciiEnCipherText" style="width: 450px; margin-left: 20px;" placeholder=""/>
              </div>

              <br><br>

              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密文</h3>
                <el-input v-model="asciiDePlainText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入明文"/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥</h3>
                <el-input v-model="asciiDeSecretKey" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;"
                           @click="getKey(asciiDeSecretKey)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                <el-button style="font-weight: 600;" @click="asciiDecryption">开始解密</el-button>
                <el-input v-model="asciiDeCipherText" style="width: 450px; margin-left: 20px;" placeholder=""/>
              </div>
            </div>
            <div v-if="cardID == 2" class="input">
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>明文</h3>
                <el-input v-model="doubleEnPlainText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入明文"/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥1</h3>
                <el-input v-model="doubleEnSecretKey1" style="width: 490px; margin-left: 20px;"
                          placeholder="请输入第一把密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getKey(doubleEnSecretKey1)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥2</h3>
                <el-input v-model="doubleEnSecretKey2" style="width: 490px; margin-left: 20px;"
                          placeholder="请输入第二把密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getKey(doubleEnSecretKey2)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                <el-button style="font-weight: 600;" @click="doubleEncryption">开始加密</el-button>
                <el-input v-model="doubleEnCipherText" style="width: 450px; margin-left: 20px;" placeholder=""/>
              </div>

              <br><br>

              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密文</h3>
                <el-input v-model="doubleDeCipherText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入密文"/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥1</h3>
                <el-input v-model="doubleDeSecretKey1" style="width: 490px; margin-left: 20px;"
                          placeholder="请输入第一把密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getKey(doubleDeSecretKey1)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥2</h3>
                <el-input v-model="doubleDeSecretKey2" style="width: 490px; margin-left: 20px;"
                          placeholder="请输入第二把密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getKey(doubleDeSecretKey2)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                <el-button style="font-weight: 600;" @click="doubleDecryption">开始解密</el-button>
                <el-input v-model="doubleDePlainText" style="width: 450px; margin-left: 20px;" placeholder=""/>
              </div>
            </div>
            <div v-if="cardID == 3" class="input">
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>明文</h3>
                <el-input v-model="tripleEnPlainText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入明文"/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥1</h3>
                <el-input v-model="tripleEnSecretKey1" style="width: 490px; margin-left: 20px;"
                          placeholder="请输入第一把密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getKey(tripleEnSecretKey1)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥2</h3>
                <el-input v-model="tripleEnSecretKey2" style="width: 490px; margin-left: 20px;"
                          placeholder="请输入第二把密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getKey(tripleEnSecretKey2)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥3</h3>
                <el-input v-model="tripleEnSecretKey3" style="width: 490px; margin-left: 20px;"
                          placeholder="请输入第三把密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getKey(tripleEnSecretKey3)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                <el-button style="font-weight: 600;" @click="doubleEncryption">开始加密</el-button>
                <el-input v-model="tripleEnCipherText" style="width: 450px; margin-left: 20px;" placeholder=""/>
              </div>

              <br><br>

              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密文</h3>
                <el-input v-model="tripleDeCipherText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入密文"/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥1</h3>
                <el-input v-model="tripleDeSecretKey1" style="width: 490px; margin-left: 20px;"
                          placeholder="请输入第一把密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getKey(tripleDeSecretKey1)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥2</h3>
                <el-input v-model="tripleDeSecretKey2" style="width: 490px; margin-left: 20px;"
                          placeholder="请输入第二把密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getKey(tripleDeSecretKey2)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥3</h3>
                <el-input v-model="tripleDeSecretKey3" style="width: 490px; margin-left: 20px;"
                          placeholder="请输入第三把密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="getKey(tripleDeSecretKey3)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                <el-button style="font-weight: 600;" @click="doubleDecryption">开始解密</el-button>
                <el-input v-model="tripleDePlainText" style="width: 450px; margin-left: 20px;" placeholder=""/>
              </div>
            </div>
            <div v-if="cardID == 4" class="input">
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>明文</h3>
                <el-input v-model="attackPlainText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入明文"/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密文</h3>
                <el-input v-model="attackCipherText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入密文"/>
                <el-button style="font-weight: 600; margin-left: 20px;" @click="attack">开始攻击
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 20px">
                <h2>破解结果</h2>
              </div>
              <!--              <el-divider>-->
              <!--                  破解结果-->
              <!--              </el-divider>-->
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥1</h3>
                <el-input v-model="attackSecretKey1" style="width: 490px; margin-left: 20px;" placeholder=""/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥2</h3>
                <el-input v-model="attackSecretKey2" style="width: 490px; margin-left: 20px;" placeholder=""/>
              </div>
            </div>
            <div v-if="cardID == 5" class="input">
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>明文</h3>
                <el-input v-model="workEnPlainText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入明文"/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥</h3>
                <el-input v-model="workEnSecretKey" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;"
                           @click="getKey(workEnSecretKey)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>初始向量</h3>
                <el-input v-model="workEnVector" style="width: 460px; margin-left: 20px;"
                          placeholder="请输入初始向量"/>
                <el-button style="font-weight: 600; margin-left: 20px;"
                           @click="getVector(workEnVector)">获取随机初始向量
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                <el-button style="font-weight: 600;" @click="workEncryption">开始加密</el-button>
                <el-input v-model="workEnCipherText" style="width: 450px; margin-left: 20px;" placeholder=""/>
              </div>

              <br><br>

              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密文</h3>
                <el-input v-model="workDeCipherText" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入密文"/>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>密钥</h3>
                <el-input v-model="workDeSecretKey" style="width: 500px; margin-left: 20px;"
                          placeholder="请输入密钥"/>
                <el-button style="font-weight: 600; margin-left: 20px;"
                           @click="getKey(workDeSecretKey)">获取随机密钥
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                <h3>初始向量</h3>
                <el-input v-model="workDeVector" style="width: 460px; margin-left: 20px;"
                          placeholder="请输入初始向量"/>
                <el-button style="font-weight: 600; margin-left: 20px;"
                           @click="getVector(workDeVector)">获取随机初始向量
                </el-button>
              </div>
              <div
                  style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                <el-button style="font-weight: 600;" @click="encryption">开始解密</el-button>
                <el-input v-model="workDePlainText" style="width: 450px; margin-left: 20px;" placeholder=""/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue';
import axios from 'axios'

const cardID = ref(0);

const binEnPlainText = ref(""); // 二进制加密的明文
const binEnCipherText = ref(""); // 二进制加密的密文
const binEnSecretKey = ref(""); // 二进制加密的密钥

const binDePlainText = ref(""); // 二进制解密的明文
const binDeCipherText = ref(""); // 二进制解密的密文
const binDeSecretKey = ref(""); // 二进制解密的密钥

const asciiEnPlainText = ref(""); // ASCII加密的明文
const asciiEnCipherText = ref(""); // ASCII加密的密文
const asciiEnSecretKey = ref(""); // ASCII加密的密钥

const asciiDePlainText = ref(""); // ASCII解密的明文
const asciiDeCipherText = ref(""); // ASCII解密的密文
const asciiDeSecretKey = ref(""); // ASCII解密的密钥

const doubleEnPlainText = ref(""); // 双重加密的明文
const doubleEnCipherText = ref(""); // 双重加密的密文
const doubleEnSecretKey1 = ref(""); // 双重加密的密钥1
const doubleEnSecretKey2 = ref(""); // 双重加密的密钥2

const doubleDePlainText = ref(""); // 双重解密的明文
const doubleDeCipherText = ref(""); // 双重解密的密文
const doubleDeSecretKey1 = ref(""); // 双重解密的密钥1
const doubleDeSecretKey2 = ref(""); // 双重解密的密钥2

const attackPlainText = ref(""); // 中间相遇攻击的明文
const attackCipherText = ref(""); // 中间相遇攻击的密文
const attackSecretKey1 = ref(""); // 中间相遇攻击的密钥1
const attackSecretKey2 = ref(""); // 中间相遇攻击的密钥2

const tripleEnPlainText = ref(""); // 三重加密的明文
const tripleEnCipherText = ref(""); // 三重加密的密文
const tripleEnSecretKey1 = ref(""); // 三重加密的密钥1
const tripleEnSecretKey2 = ref(""); // 三重加密的密钥2
const tripleEnSecretKey3 = ref(""); // 三重加密的密钥3

const tripleDePlainText = ref(""); // 三重解密的明文
const tripleDeCipherText = ref(""); // 三重解密的密文
const tripleDeSecretKey1 = ref(""); // 三重解密的密钥1
const tripleDeSecretKey2 = ref(""); // 三重解密的密钥2
const tripleDeSecretKey3 = ref(""); // 三重解密的密钥3

const workEnPlainText = ref(""); // 工作模式加密的明文
const workEnCipherText = ref(""); // 工作模式加密的密文
const workEnSecretKey = ref(""); // 工作模式加密的密钥
const workEnVector = ref(""); // 工作模式加密的初始向量

const workDePlainText = ref(""); // 工作模式解密的明文
const workDeCipherText = ref(""); // 工作模式解密的密文
const workDeSecretKey = ref(""); // 工作模式解密的密钥
const workDeVector = ref(""); // 工作模式解密的初始向量

const timeTaken = ref("");


function changeID(id) {
  cardID.value = id;
}


async function binEncryption() {
  try {
    // 检查输入是否为空
    if (!binEnPlainText.value || !binEnSecretKey.value) {
      alert('请输入明文和密钥')
      return
    }

    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/binEncryption', {
      binEnPlainText: binEnPlainText.value,
      binEnSecretKey: binEnSecretKey.value
    })

    binEnCipherText.value = response.data.binEnCipherText
    console.log('加密成功:', binEnCipherText.value)
  } catch (error) {
    console.error('加密失败:', error)
    alert('加密失败，请稍后再试')
  }
}


async function binDecryption() {
  try {
    // 检查输入是否为空
    if (!binDeCipherText.value || !binDeSecretKey.value) {
      alert('请输入密文和密钥')
      return
    }

    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/binDecryption', {
      binDeCipherText: binDeCipherText.value,
      binDeSecretKey: binDeSecretKey.value
    })

    binDePlainText.value = response.data.binDePlainText
    console.log('加密成功:', binDePlainText.value)
  } catch (error) {
    console.error('加密失败:', error)
    alert('加密失败，请稍后再试')
  }
}

async function asciiEncryption() {
  try {
    // 检查输入是否为空
    if (!asciiEnPlainText.value || !asciiEnSecretKey.value) {
      alert('请输入明文和密钥')
      return
    }

    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/asciiEncryption', {
      asciiEnPlainText: asciiEnPlainText.value,
      asciiEnSecretKey: asciiEnSecretKey.value
    })

    asciiEnCipherText.value = response.data.asciiEnCipherText
    console.log('加密成功:', asciiEnCipherText.value)
  } catch (error) {
    console.error('加密失败:', error)
    alert('加密失败，请稍后再试')
  }
}


async function asciiDecryption() {
  try {
    // 检查输入是否为空
    if (!asciiDeCipherText.value || !asciiDeSecretKey.value) {
      alert('请输入密文和密钥')
      return
    }

    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/asciiDecryption', {
      asciiDeCipherText: asciiDeCipherText.value,
      asciiDeSecretKey: asciiDeSecretKey.value
    })

    asciiDePlainText.value = response.data.asciiDePlainText
    console.log('加密成功:', asciiDePlainText.value)
  } catch (error) {
    console.error('加密失败:', error)
    alert('加密失败，请稍后再试')
  }
}

async function doubleEncryption() {
  try {
    // 检查输入是否为空
    if (!doubleEnPlainText.value || !doubleEnSecretKey1.value || !doubleEnSecretKey2.value) {
      alert('请输入明文和密钥')
      return
    }

    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/doubleEncryption', {
      doubleEnPlainText: doubleEnPlainText.value,
      doubleEnSecretKey1: doubleEnSecretKey1.value,
      doubleEnSecretKey2: doubleEnSecretKey2.value
    })

    doubleEnCipherText.value = response.data.doubleEnCipherText
    console.log('加密成功:', doubleEnCipherText.value)
  } catch (error) {
    console.error('加密失败:', error)
    alert('加密失败，请稍后再试')
  }
}


async function doubleDecryption() {
  try {
    // 检查输入是否为空
    if (!doubleDeCipherText.value || !doubleDeSecretKey1.value || !doubleDeSecretKey2.value) {
      alert('请输入密文和密钥')
      return
    }

    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/doubleDecryption', {
      doubleDeCipherText: doubleDeCipherText.value,
      doubleDeSecretKey1: doubleDeSecretKey1.value,
      doubleDeSecretKey2: doubleDeSecretKey2.value
    })

    doubleDePlainText.value = response.data.doubleDePlainText
    console.log('加密成功:', doubleDePlainText.value)
  } catch (error) {
    console.error('加密失败:', error)
    alert('加密失败，请稍后再试')
  }
}

async function tripleEncryption() {
  try {
    // 检查输入是否为空
    if (!tripleEnPlainText.value || !tripleEnSecretKey1.value || !tripleEnSecretKey2.value || !tripleEnSecretKey3.value) {
      alert('请输入明文和密钥')
      return
    }

    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/tripleEncryption', {
      tripleEnPlainText: tripleEnPlainText.value,
      tripleEnSecretKey1: tripleEnSecretKey1.value,
      tripleEnSecretKey2: tripleEnSecretKey2.value,
      tripleEnSecretKey3: tripleEnSecretKey3.value
    })

    tripleEnCipherText.value = response.data.tripleEnCipherText
    console.log('加密成功:', tripleEnCipherText.value)
  } catch (error) {
    console.error('加密失败:', error)
    alert('加密失败，请稍后再试')
  }
}


async function tripleDecryption() {
  try {
    // 检查输入是否为空
    if (!tripleDeCipherText.value || !tripleDeSecretKey1.value || !tripleDeSecretKey2.value || !tripleDeSecretKey3.value) {
      alert('请输入密文和密钥')
      return
    }

    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/tripleDecryption', {
      tripleDeCipherText: tripleDeCipherText.value,
      tripleDeSecretKey1: tripleDeSecretKey1.value,
      tripleDeSecretKey2: tripleDeSecretKey2.value,
      tripleDeSecretKey3: tripleDeSecretKey3.value
    })

    tripleDePlainText.value = response.data.tripleDePlainText
    console.log('加密成功:', tripleDePlainText.value)
  } catch (error) {
    console.error('加密失败:', error)
    alert('加密失败，请稍后再试')
  }
}

async function attack() {
  try {
    // 检查输入是否为空
    if (!attackCipherText.value || !attackPlainText.value) {
      alert('请输入密文和密钥')
      return
    }

    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/attack', {
      attackCipherText: attackCipherText.value,
      attackPlainText: attackPlainText.value
    })

    attackSecretKey1.value = response.data.attackSecretKey1
    attackSecretKey2.value = response.data.attackSecretKey2
    console.log('攻击成功：', attackSecretKey1.value, attackSecretKey2.value)
  } catch (error) {
    console.error('攻击失败:', error)
    alert('攻击失败，请稍后再试')
  }
}

async function workEncryption() {
  try {
    // 检查输入是否为空
    if (!workEnPlainText.value || !workEnSecretKey.value || !workEnVector.value) {
      alert('请输入明文和密钥')
      return
    }

    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/workEncryption', {
      workEnPlainText: workEnPlainText.value,
      workEnSecretKey: workEnSecretKey.value,
      workEnVector: workEnVector.value
    })

    workEnCipherText.value = response.data.workEnCipherText
    console.log('加密成功:', workEnCipherText.value)
  } catch (error) {
    console.error('加密失败:', error)
    alert('加密失败，请稍后再试')
  }
}


async function workDecryption() {
  try {
    // 检查输入是否为空
    if (!workDeCipherText.value || !workDeSecretKey.value || !workDeVector.value) {
      alert('请输入密文和密钥')
      return
    }

    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/workDecryption', {
      workDeCipherText: workDeCipherText.value,
      workDeSecretKey: workDeSecretKey.value,
      workDeVector: workDeVector.value
    })

    workDePlainText.value = response.data.workDePlainText
    console.log('加密成功:', workDePlainText.value)
  } catch (error) {
    console.error('加密失败:', error)
    alert('加密失败，请稍后再试')
  }
}

// 随机生成密钥
async function getBinKey(target) {
  try {
    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/getBinKey', {})

    target.value = response.data.secretKey

    console.log('获取密钥成功:', secretKey.value)
  } catch (error) {
    console.error('获取密钥失败:', error)
    alert('获取密钥失败，请稍后再试')
  }
}


// 随机生成密钥
async function getKey(target) {
  try {
    // 发送请求到后端
    const response = await axios.post('http://localhost:5000/getKey', {})

    target.value = response.data.secretKey

    console.log('获取密钥成功:', secretKey.value)
  } catch (error) {
    console.error('获取密钥失败:', error)
    alert('获取密钥失败，请稍后再试')
  }
}

function exitSystem() {
  alert('您已退出系统！')
}
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
  background: rgb(247, 249, 253);
}

.header {
  background-color: rgb(255, 255, 255);
  display: flex;
  justify-content: center;
  align-items: center;
}

.main {
  display: flex;
  padding: 0;
}

.centerInfo {
  background: linear-gradient(to bottom right, #b4daff, #fff);
  width: 95%;
  height: 95%;
  border-radius: 40px;
  display: flex;
  /* align-items: ; */
  justify-content: left;
}

.leftSide {
  width: 15%;
  display: flex;
  align-items: center;
  flex-direction: column;
}

.rightSide {
  width: 85%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.leftCardStyle {
  width: 150px;
  height: 60px;
  /* height: 20%; */
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: auto;
  background-color: rgb(247, 249, 254);
  border: none;
  cursor: pointer;
  margin-top: 5px;
  /* margin-bottom: 20px; */
  margin-right: 0px;
}

.leftCardStyle:hover {
  background-color: rgb(220, 235, 255);
  color: rgb(115, 163, 231);
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
  margin-right: 20px;
}

.redLeftCardStyle {
  width: 150px;
  height: 60px;
  margin-left: auto;
  background-color: rgb(247, 249, 254);
  border: none;
  cursor: pointer;
  margin-right: 0px;
  margin-top: 5px;
}

.redLeftCardStyle:hover {
  background-color: rgba(255, 0, 0, 0.1);
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
  margin-right: 20px;
}


.selectedCard {
  background-color: rgb(220, 235, 255);
  color: rgba(90, 156, 248, 1);
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
  margin-right: 20px;
}

.divider {
  width: 1px;
  background-color: #ccc;
}

.rightTitle {
  display: flex;
  width: 100%;
  height: 10%;
}

.rightContent {
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.title {
  margin-left: 20px;
}

.input {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  margin-top: 20px;
  /* align-items: center; */
  justify-content: left;
}

:deep .el-divider__text {
  background-color: transparent;
  color: var(--el-text-color-primary);
  font-size: 20px;
  font-weight: 1000;
  padding: 0 20px;
  position: absolute;
}
</style>