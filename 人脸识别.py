import json
import requests
api1 = " "

api2 = "https://aip.baidubce.com/rest/2.0/face/v3/match?access_token="

# 1. 读取图片数据
def get_img(img1, img2):
    import base64
    with open(img1, "rb") as f:
        pic1 = f.read()
    with open(img2, "rb") as f:
        pic2 = f.read()

    params = json.dumps([
        {"image": str(base64.b64encode(pic1), "utf-8"), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},
        {"image": str(base64.b64encode(pic2), "utf-8"), "image_type": "BASE64", "face_type": "IDCARD","quality_control": "LOW"},
    ])
    return params

# 2. 获取token值 拼接API
def get_token():
    response = requests.get(api1)
    access_token = eval(response.text)['access_token']
    api_url = api2 + access_token
    return api_url

# 3. 请求API拿到最终结果
def than_img(img1, img2):
    api_url = get_token()
    params = get_img(img1, img2)

    content = requests.post(api_url, params).text
    score = eval(content)['result']['score']

    if score > 80:
        print("图片相似度：" + str(score) + ",同一个人")
    else:
        print("图片相似度：" + str(score) + ",不是同一个人")

than_img("马云1.png", "xx.png")