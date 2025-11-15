import base64
import json
import re
from io import BytesIO

import ddddocr
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from PIL import Image

session = requests.session()

# 加密盐值
url = "http://jw.gzist.edu.cn/jwglxt/xtgl/login_getPublicKey.html"
res = session.get(url)
res_json = json.loads(res.text)
modulus = res_json["modulus"]
exponent = res_json["exponent"]


# 密码加密
def rsa_encrypt_base64(modulus_b64: str, exponent_b64: str, plaintext: str) -> str:
    """
    输入:
      - modulus_b64: 从后端拿到的 modulus（Base64 编码字符串）
      - exponent_b64: 从后端拿到的 exponent（Base64 编码字符串，常见为 "AQAB"）
      - plaintext: 明文密码
    返回:
      - 与前端等价的 Base64(RSA_PKCS1_v1_5_encrypt(plaintext)) 字符串
    """
    # 把 base64 -> bytes -> 整数
    mod_bytes = base64.b64decode(modulus_b64)
    exp_bytes = base64.b64decode(exponent_b64)

    mod_int = int.from_bytes(mod_bytes, byteorder="big")
    exp_int = int.from_bytes(exp_bytes, byteorder="big")

    # 构造 RSA 公钥并加密（PKCS#1 v1.5，与大多数前端 RSA.js 实现一致）
    rsa_key = RSA.construct((mod_int, exp_int))
    cipher = PKCS1_v1_5.new(rsa_key)
    cipher_bytes = cipher.encrypt(plaintext.encode("utf-8"))

    # 返回 Base64 字符串（前端通常是 hex->base64，但效果等价：这是原始密文 bytes 的 base64）
    return base64.b64encode(cipher_bytes).decode("ascii")


def main(pwd, un):
    mm = rsa_encrypt_base64(modulus, exponent, pwd)

    # 验证码
    url = "http://jw.gzist.edu.cn/jwglxt/kaptcha"
    res = session.get(url)
    img_data = BytesIO(res.content)
    img = Image.open(img_data)
    ocr_client = ddddocr.DdddOcr()
    ocr = ocr_client.classification(img)

    # token
    url = "http://jw.gzist.edu.cn/jwglxt/xtgl/login_slogin.html"
    res = session.get(url)
    pattern = r'id="csrftoken".*?name="csrftoken".*?value="(.*?)"'
    match = re.search(pattern, res.text)

    # 发送登录请求
    payload_dict = {
        "csrftoken": match.group(1),
        "language": "zh_CN",
        "ydType": "1",
        "yhm": un,
        "mm": mm,
        "yzm": ocr.lower(),
    }
    res = session.post(url, data=payload_dict)
    print(res.url)

    # 测试获取个人信息
    url = "http://jw.gzist.edu.cn/jwglxt/xsxxxggl/xsgrxxwhMobile_cxXsgrxxApp.html"
    res = session.post(url, data={"doType": "app"})
    return json.loads(res.text)


if __name__ == "__main__":
    print(main("你的密码", "你的账号"))
