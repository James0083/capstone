# pip install dlib opencv-python

import dlib
import cv2 as cv
import numpy as np
from google.colab.patches import cv2_imshow

# !wget   http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 # DOWNLOAD LINK

# !bunzip2 /content/shape_predictor_68_face_landmarks.dat.bz2

datFile =  "/shape_predictor_68_face_landmarks.dat"



detector = dlib.get_frontal_face_detector()
 
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#웹캠 불러옴
cap = cv.VideoCapture(0)



# range는 끝값이 포함안됨   
ALL = list(range(0, 68)) 

MOUTH_OUTLINE = list(range(48, 61))  
MOUTH_INNER = list(range(61, 68)) 

index = ALL




while True:

    ret, img_frame = cap.read()

    # resize the video
    image = cv.resize(img_frame, dsize=(640, 480), interpolation=cv.INTER_AREA)
    img_gray = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY)


    dets = detector(img_gray, 1)
    # the number of face detected
    print("The number of faces detected : {}".format(len(dets)))


    for face in dets:

        shape = predictor(img_frame, face) #얼굴에서 68개 점 찾기

        list_points = []
        for p in shape.parts():
            list_points.append([p.x, p.y])

        list_points = np.array(list_points)


        for i,pt in enumerate(list_points[index]):

            pt_pos = (pt[0], pt[1])
            cv.circle(img_frame, pt_pos, 2, (0, 255, 0), -1)

        
        cv.rectangle(img_frame, (face.left(), face.top()), (face.right(), face.bottom()),
            (0, 0, 255), 3)


    cv2_imshow( img_frame)
    



    
    key = cv.waitKey(1)

    if key == 27:
        break

    elif key == ord('5'):
        index = MOUTH_OUTLINE+MOUTH_INNER


cap.release()







while True:
    # read : 프레임 읽기
    # [return]
    # 1) 읽은 결과(True / False)
    # 2) 읽은 프레임
    retval, frame = cap.read()

    img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    dets = detector(img_gray, 1)
    # the number of face detected
    print("The number of faces detected : {}".format(len(dets)))

    # 읽은 프레임이 없는 경우 종료
    if not retval:
        break

    # resize : 이미지 크기 변환
    # 1) 변환할 이미지
    # 2) 변환할 이미지 크기(가로, 세로)
    # - interpolation : 보간법 지정
    #   - 보간법 : 알려진 데이터 지점 내에서 새로운 데이터 지점을 구성하는 방식
    #   - cv2.INTER_NEAREST : 최근방 이웃 보간법
    #   - cv2.INTER_LINEAR(default) : 양선형 보간법(2x2 이웃 픽셀 참조)
    #   - cv2.INTER_CUBIC : 3차 회선 보간법(4x4 이웃 픽셀 참조)
    #   - cv2.INTER_LANCZOS4 : Lanczos 보간법(8x8 이웃 픽셀 참조)
    #   - cv2.INTER_AREA : 픽셀 영역 관계를 이용한 resampling 방법으로 이미지 축소시 효과적
    resize_frame = cv.resize(frame, (532, 720), interpolation=cv.INTER_CUBIC)

    for face in dets:

        shape = predictor(frame, face) #얼굴에서 68개 점 찾기

        list_points = []
        for p in shape.parts():
            list_points.append([p.x, p.y])

        list_points = np.array(list_points)


        for i,pt in enumerate(list_points[index]):

            pt_pos = (pt[0], pt[1])
            cv.circle(frame, pt_pos, 2, (0, 255, 0), -1)

        
        cv.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()),
            (0, 0, 255), 3)


    
    # 프레임 출력
    cv_imshow( resize_frame)
    #recognition
    cv_imshow(frame)
    # 'q' 를 입력하면 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 동영상 파일 또는 카메라를 닫고 메모리를 해제
cap.release()

# 모든 창 닫기
cv.destroyAllWindows()
