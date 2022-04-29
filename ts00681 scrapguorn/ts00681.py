
# 百度图片识别
# https://cloud.baidu.com/doc/OCR/s/Ek3h7yeiq

from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '22529677'
API_KEY = 'miUrjSWNGr0O8YGffYqCsZG4'
SECRET_KEY = 'bNA0qXyTNBwD160dpMSs8GPWji4IKBS8'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

options = {}
options["language_type"] = "ENG"

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('c:\\4.png')

# print(client.basicGeneral(image))
print(client.basicGeneral(image, options))


# print(client.basicAccurate(image))