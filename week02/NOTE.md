学习笔记

异常只会被捕获一次，多个异常不会同时捕获。

```
try:
    1/0
except Exception as e:
    try:
        1/0
    except Exception as f:
        pass
    print(e)    # 输出异常信息
```

自建异常应该继承 `Exception` ：

```
class UserInputError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo + '。正确输入应该是数字！'

userinput = 'a'

try:
    if (not userinput.isdigit()):
        raise UserInputError('用户输入错误')
except UserInputError as ue:
    print(ue)
finally:
    del userinput
```

`pretty_errors` 可以美化异常的输出


with 语句用于包装带有使用上下文管理器 (参见 with 语句上下文管理器 一节) 定义的方法的代码块的执行。 这允许对普通的 try...except...finally 使用模式进行封装以方便地重用。

```
class Open:
    def __enter__(self):
        print("open")

    def __exit__(self, type, value, trace):
        print("close")
 
    def __call__(self):
        pass

with Open() as f:
    pass
```


反爬策略：

Headers:

1. User-Agent

```
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)

print(f'Chrome浏览器: {ua.chrome}')
# print(ua.safari)
# print(ua.ie)
print(f'随机浏览器: {ua.random}')
```

2. Referer
3. Host

4. Cookies

```
import time
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
headers = {
'User-Agent' : ua.random,
'Referer' : 'https://accounts.douban.com/passport/login_popup?login_source=anony'
}

s = requests.Session()
# 会话对象：在同一个 Session 实例发出的所有请求之间保持 cookie， 
# 期间使用 urllib3 的 connection pooling 功能。
# 向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。
login_url = 'https://accounts.douban.com/j/mobile/login/basic'
form_data = {
'ck':'',
'name':'15055495@qq.com',
'password':'',
'remember':'false',
'ticket':''
}

# post数据前获取cookie
pre_login = 'https://accounts.douban.com/passport/login'
pre_resp = s.get(pre_login, headers=headers)

response = s.post(login_url, data=form_data, headers=headers, cookies=s.cookies)


# 登陆后可以进行后续的请求
# url2 = 'https://accounts.douban.com/passport/setting'

# response2 = s.get(url2,headers = headers)
# response3 = newsession.get(url3, headers = headers, cookies = s.cookies)

# with open('profile.html','w+') as f:
    # f.write(response2.text)
```

5. 模拟浏览器行为

```
from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    # 需要安装chrome driver, 和浏览器版本保持一致
    # http://chromedriver.storage.googleapis.com/index.html
    
    browser.get('https://www.douban.com')
    time.sleep(1)

    browser.switch_to_frame(browser.find_elements_by_tag_name('iframe')[0])
    btm1 = browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    btm1.click()

    browser.find_element_by_xpath('//*[@id="username"]').send_keys('15055495@qq.com')
    browser.find_element_by_id('password').send_keys('test123test456')
    time.sleep(1)
    browser.find_element_by_xpath('//a[contains(@class,"btn-account")]').click()

    cookies = browser.get_cookies() # 获取cookies
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)
finally:    
    browser.close()
```



大文件下载

```
import requests
file_url = "http://python.xxx.yyy.pdf"
r = requests.get(file_url, stream=True)
with open("python.pdf", "wb") as pdf:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            pdf.write(chunk)
```

6. 验证码识别


```

# 先安装依赖库libpng, jpeg, libtiff, leptonica
# brew install leptonica
# 安装tesseract
# brew install  tesseract
# 与python对接需要安装的包
# pip3 install Pillow
# pip3 install pytesseract



import requests
import os
from PIL import Image
import pytesseract

# 下载图片
# session = requests.session()
# img_url = 'https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1320441599,4127074888&fm=26&gp=0.jpg'
# agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# headers = {'User-Agent': agent}
# r = session.get(img_url, headers=headers)

# with open('cap.jpg', 'wb') as f:
#     f.write(r.content)

# 打开并显示文件
im = Image.open('cap.jpg')
im.show()

# 灰度图片
gray = im.convert('L')
gray.save('c_gray2.jpg')
im.close()

# 二值化
threshold = 100
table = []

for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

out = gray.point(table, '1')
out.save('c_th.jpg')

th = Image.open('c_th.jpg')
print(pytesseract.image_to_string(th,lang='chi_sim+eng'))

# 各种语言识别库 https://github.com/tesseract-ocr/tessdata
# 放到 /usr/local/Cellar/tesseract/版本/share/tessdata

```