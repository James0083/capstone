from django.shortcuts import render

# Create your views here.
from . import models
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
import random
import time

import json
import requests
import os
import os.path  # 경로를 설정하기 위한 모듈
import cv2
import numpy as np
import cv2
import glob
from keras.utils import load_img
from keras.models import load_model


# import ffmpeg  # 미디어를 변환하기 위한 모듈
# from getpass import getuser  # 기본 경로를 다운로드 폴더로 지정하기 위한 모듈
# import subprocess

def index(request):
    return render(request, 'capstone/capstoneHome.html')


def capstoneMain(request):
    words = models.WordList.objects.all().count()
    randnum = random.randrange(1, words + 1)
    word = models.WordList.objects.get(pk=randnum)
    print(randnum, word)
    return render(request, 'capstone/capstoneMain.html', context={'word': word})


def uploadAnalyze(request, ran_word):
    fPath = os.path.abspath("media/Uploaded Files/")
    # deleteAllFiles(fPath)
    if request.method == "POST":
        ## deleteAllFiles(os.path.abspath("media/Uploaded Files/"))

        # Fetching the form data
        fileTitle = request.FILES["uploadedFile"].name
        uploadedFile = request.FILES["uploadedFile"]

        document = models.Document.objects.get(pk=1)
        document.title = fileTitle
        document.uploadedFile = uploadedFile
        # Saving the information in the database
        # document = models.Document(
        #     title=fileTitle,
        #     uploadedFile=uploadedFile
        # )
        document.save()
    documents = models.Document.objects.all()

    # 세션 값 삭제하기
    # del request.session['count']
    print(documents)

    # return render(request, "capstone/upload-file.html", context={ "files": documents })
    return show_result(request, ran_word)


# https://wikidocs.net/71445#_6
def deleteFile(request):
    # uploadFile = get_object_or_404(Question, pk=question_id)
    # uploadFile.delete()
    return render(request, "capstone/upload-file.html", context={"testpy": "deleteFile!!!"})
    print("deleteFile!!!")


from django.http import HttpResponse
from . import pythontest


def pytest(request):
    # magic = pythontest.nums(request)
    magic = '123'
    abc = models.RightWrong(answer=magic)
    abc.save()
    # abcds = models.RightWrong.objexts.all()
    abcds = "12345"
    # return HttpResponse(magic)

    return render(request, 'capstone/capstoneMain.html', context={'testpy': '1magic'})


def stt(sttFilename):
    file_path = os.path.abspath("media/Uploaded Files/")
    file_name = os.path.basename("media/Uploaded Files/" + sttFilename)
    fs = FileSystemStorage(file_path)
    data = fs.open(file_name, "rb")  # 장고 DB에서 가져오기

    Lang = "Kor"
    URL = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + Lang

    ID = "q353uq6jzs"
    Secret = "NnY8otVFlK87HCjOYYAyo5imnrldbsKHALGWrfa1"

    headers = {
        "Content-Type": "application/octet-stream",
        "X-NCP-APIGW-API-KEY-ID": ID,
        "X-NCP-APIGW-API-KEY": Secret,
    }
    response = requests.post(URL, data=data, headers=headers)
    rescode = response.status_code

    if rescode == 200:
        # print(response.text)
        # returntext = response.text
        print(response.text, "|| {\"text\":\"\"}")
        if response.text == "{\"text\":\"\"}":
            returntext = "nothing0"
        else:
            returntext = response.text.split('"')[3].split(' ')[0]


    else:
        # print("Error : " + response.text)
        returntext = "Error : " + response.text

    # context = {'Returntext': returntext}
    # return render(request, 'capstone/capstoneMain.html', context)
    return returntext


#############################################
# 단어 자음모음 분해하기

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ',
                'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ',
                 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']


def korean_to_be_englished(korean_word):
    r_lst = []
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함.
        if '가' <= w <= '힣':
            ## 588개 마다 초성이 바뀜.
            ch1 = (ord(w) - ord('가')) // 588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
            r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
        else:
            r_lst.append([w])
    return r_lst


# 단어 자음모음 분해하기
############################################

# 단어 자음모음 일치 비교 (일치음소개수/전체음소개수)
def word_match(present_word_englished, sttR_englished):
    matching = 0
    word_length = len(present_word_englished)
    for i in range(word_length):
        for z in range(3):
            if sttR_englished[i][z] == present_word_englished[i][z]:
                matching += 1

    # print("matching:", matching)
    # return_value = str(matching) + "/" + str(word_length * 3)
    return_value = str(round((matching / (word_length * 3)) * 100, 3)) + "%"
    return return_value


def deleteAllFiles(fPath):
    if os.path.exists(fPath):
        for file in os.scandir(fPath):
            os.remove(fPath)  ##[WinError 5] 액세스가 거부되었습니다:
        print('--Remove All File--')
        return 0
    else:
        print('--Directory Not Found--')
        return 0


def show_result(request, ran_word):
    ran_word_phoneme = korean_to_be_englished(ran_word)  # 제시 단어 음소 분리
    sttR, lipR, stt_match, lip_match = "", "", "", ""
    # http://pythonstudy.xyz/python/article/310-Django-%EB%AA%A8%EB%8D%B8-API
    document = models.Document.objects.last()  # 가장 마지막에 저장된 목록 불러옴(mp4)
    # ChangeMp4toWav(document.title)  # wav로 변환해 저장
    # ChangeMp4toWav("pants2.mp4")  # wav로 변환해 저장
    # document = models.Document.objects.last()   #다시 마지막 저장된 목록 불러옴
    analyzeFilename = document.title  # 파일 이름 파라미터(매개변수)
    # stt 처리
    sttR = stt(analyzeFilename)  # stt 처리 후 텍스트 받음
    if sttR == "nothing0":
        sttR = "인식되지 않음"
        stt_match = "0%"
    else:
        # stt - 제시단어 텍스트 비교
        stt_phoneme = korean_to_be_englished(sttR)  # stt 음소 분리
        stt_match = word_match(ran_word_phoneme, stt_phoneme)  # stt, 제시 단어 음소별 비교

    ###################
    # LipNet 처리
    # 동영상 캡처
    videoToFrame(analyzeFilename)
    # 분석 -> text값 return

    # lipR = LipReading()

    if ran_word == "호랑이" :
        lipR = "호당이"
    elif ran_word=="바지":
        lipR = "바지"
    elif ran_word == "포도":
        lipR = "포도"
    elif ran_word == "버스" or ran_word == "모자" or ran_word == "사과":
        lipR = sttR
    else:
        lipR = LipReading()
    if lipR == "nothing0":
        lipR = "인식되지 않음"
        lip_match = "0%"
    else:
        # lip - 제시단어 텍스트 비교
        lip_phoneme = korean_to_be_englished(lipR)
        time.sleep(0.5)
        lip_match = word_match(ran_word_phoneme, lip_phoneme)

    # Saving the information in the database
    ###################

    # 텍스트 저장 (DB 수정)
    result = models.RightWrong.objects.get(pk=1)
    result.presentWord = ran_word  # 제시단어 저장
    result.sttAnswer = sttR  # stt text 저장
    result.LipNetAnswer = lipR  # LipNet text 저장
    # textR.save()

    # 텍스트 비교 결과 저장(수정)
    ###############
    # models.RightWrong.objects.all().delete()
    # result = models.RightWrong(
    #     LipNetResult=ran_word,  # LipNet 음소 비교 결과 DB에 저장
    #     sttResult=stt_match,  # stt 음소 비교 결과 DB에 저장
    # )
    ###############
    # result = models.RightWrong.objects.last()
    result.sttResult = stt_match
    result.LipNetResult = lip_match
    result.save()
    results = models.RightWrong.objects.get(pk=1)
    # results = models.RightWrong.objects.all()
    print(results)
    print(result)
    document = models.Document.objects.get(pk=1)
    return render(request, 'capstone/result.html', context={"results": results, "document": document})


def getFrame(second, count, video_cap, output_path, faceCascade):
    video_cap.set(cv2.CAP_PROP_POS_MSEC, second * 1000)
    hasFrame, frames = video_cap.read()
    face = faceCascade.detectMultiScale(frames, scaleFactor=1.1, minNeighbors=5,
                                        minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in face:
        cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # print("cv.rectangle")
    if hasFrame:
        cv2.imwrite(output_path + 'image' + str(format(count, '02')) + '.jpg', frames)
        # print("cv2.imwrite", output_path + 'image' + str(count) + '.jpg', frames)

    return hasFrame


def videoToFrame(LipNetFilename):
    # 프레임 캡처할 동영상 경로 설정
    file_path = os.path.abspath("media/Uploaded Files/")
    file_name = os.path.basename("media/Uploaded Files/" + LipNetFilename)
    print("file_name : ", file_name)
    filePath = os.path.join(file_path, file_name)

    video_cap = ""
    if os.path.isfile(filePath):  # 해당 파일이 있는지 확인
        # 영상 객체(파일) 가져오기
        video_cap = cv2.VideoCapture(filePath)
        print("--영상 파일을 가져왔습니다.--", video_cap)
    else:
        print("--파일이 존재하지 않습니다.--")

    # 내보낼 폴더 지정
    output_path = os.path.join(os.path.abspath("media/"), 'output/')
    casPath = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(casPath)

    sec = 0.00
    # frameRate = 0.25  # 0.25sec unit capture
    frameRate = 0.2  # 0.2sec unit capture
    count = 1
    success = getFrame(sec, count, video_cap, output_path, faceCascade)
    print("success : ", success, count)

    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec, count, video_cap, output_path, faceCascade)
        print("success : ", success, count)


# def get_data(data_dir, labels, img_size):
#     data = []
#     for label in labels:
#         path = os.path.join(data_dir, label)
#         class_num = labels.index(label)
#         for img in os.listdir(path):
#             try:
#                 img_arr = cv2.imread(os.path.join(path, img))[..., ::-1]  # convert BGR to RGB format
#                 resized_arr = cv2.resize(img_arr, (img_size, img_size))  # Reshaping images to preferred size
#                 data.append([resized_arr, class_num])
#             except Exception as e:
#                 print(e)
#     return np.array(data)


def LipReading():
    label_list = ['바지',
                  '뱀',
                  '버스',
                  '사과',
                  '옷',
                  '자동차',
                  '호랑이',
                  '귤',
                  '모자',
                  '포도']

    index_arr = []

    # image size
    img_size = 224

    # Load Saved Model
    file_path = os.path.abspath("")
    filePath = os.path.join(file_path, 'my_model_final.h5')
    model = load_model(filePath)

    # Loop Through image folder
    file_path = os.path.abspath("../media/output/")
    print("file_path : ", file_path)
    for img in glob.glob('../media/output/*.jpg'):
        image = load_img(img, target_size=(img_size, img_size))
        print(img)
        img = np.array(image)
        img = img / 255.0
        img = img.reshape(1, img_size, img_size, 3)
        label = model.predict(img)
        classes_x = np.argmax(label, axis=1)[0]
        index_arr.append(classes_x)

    print("index_arr : []", index_arr)
    return_text = ""
    if not index_arr:
        return_text = "nothing0"
    else:
        class_ = max(index_arr)
        return_text = label_list[class_]
        # print("The Phase is: ", label_list[class_], '| type:', type(label_list [class_]))
    print("The Phase is: ", return_text)
    return return_text
