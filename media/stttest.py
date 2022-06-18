import json
import requests
from django.core.files.storage import FileSystemStorage
import os

# data = open("tiger.wav", "rb")
file_path = os.path.abspath("media/Uploaded Files/")
file_name = os.path.basename("media/Uploaded Files/자동차5.mp4")
fs = FileSystemStorage(file_path)
data = open(file_name, "rb")  # 장고 DB에서 가져오기

Lang = "Kor" 
URL = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + Lang
    
ID = "q353uq6jzs" 
Secret = "NnY8otVFlK87HCjOYYAyo5imnrldbsKHALGWrfa1"
    
headers = {
    "Content-Type": "application/octet-stream", 
    "X-NCP-APIGW-API-KEY-ID": ID,
    "X-NCP-APIGW-API-KEY": Secret,
}
response = requests.post(URL,  data=data, headers=headers)
rescode = response.status_code

if(rescode == 200):
    print (response.text)
    print (type(response.text))
    print(response.text.split('"')[3].split(' ')[0])
else:
    print("Error : " + response.text)
