# 广州理工教务系统逆向脚本 🚀

> 自动化解放双手！验证码识别+登录脚本，助你畅享教务管理生活~

## ⭐ 如果觉得有用请顺手 Star 鼓励作者吧！Thanks! ⭐

## 项目简介

本项目通过逆向分析广州理工教务管理系统，实现验证码自动识别与自动化登录功能，后续你们可以自行开发更多功能，
如课表查询、成绩查询、课表导出、课表导入、一键式抢课等等。

## 使用方法 ✨

1. **安装依赖** (python 版本 3.12)

```shell
pip install -r requirements.txt
```

2. **配置参数**（在 `main.py` 中填入账号和密码）

3. **运行脚本**

```shell
python main.py
```

## 核心代码逻辑 🧩

- 登录页面自动抓取公钥，RSA加密密码
- 利用 [ddddocr](https://github.com/sml2h3/ddddocr) 自动解验证码，无需人工输入 🤖
- requests 实现多步表单交互，为你自动获取个人信息!

### 主要代码片段：

```python:/Users/kcicat/project/python/广州理工教务系统/v1 快速原型/main.py
mm = rsa_encrypt_base64(modulus, exponent, pwd)
ocr_client = ddddocr.DdddOcr()
ocr = ocr_client.classification(img)
payload = { ... "yzm": ocr.lower(), ... }
```

## 依赖库 📦

- requests
- pycryptodome（用于RSA加密）
- Pillow（验证码图片处理）
- matplotlib（可视化与调试）
- ddddocr（纯Python验证码OCR，0配置开箱即用）

详情见 `requirements.txt`

## 免责声明 💡

本项目仅供学习和研究使用，禁止用于任何非法用途。