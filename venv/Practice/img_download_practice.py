"""
이미지 다운로드 하기
"""

import requests
from io import BytesIO
from PIL import Image

img_url = 'https://dgalywyr863hv.cloudfront.net/pictures/athletes/51315032/14526524/2/large.jpg'

res = requests.get(img_url)

img = Image.open(BytesIO(res.content))
img.save("user.jpg", "JPEG")