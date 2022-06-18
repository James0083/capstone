import os

from django.db import models
from django.conf import settings

# Create your models here.


class Document(models.Model):
    # title = models.CharField(max_length = 100)      #파일의 사용자 지정 제목
    title = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')
    uploadedFile = models.FileField(upload_to="Uploaded Files/")  # 모든 종류의 파일, #upload_to:저장경로지정
    dateTimeOfUpload = models.DateTimeField(auto_now=True)  # 파일 업로드 날짜 저장

    def delete(self, *args, **kwargs):
        super(Document, self).delete(*args, **kwargs)
        os.remove(os.path.join(settings.MEDIA_ROOT, self.field_name.path))


# class Notice(models.Model):
#
#     def delete(self, *args, **kargs):
#         if self.upload_files:
#             os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_files.path))
#         super(Notice, self).delete(*args, **kargs)


class RightWrong(models.Model):
    presentWord = models.CharField(max_length=20, null=True, verbose_name='제시단어')
    LipNetAnswer = models.CharField(max_length=20, null=True, verbose_name='독순결과')
    sttAnswer = models.CharField(max_length=20, null=True, verbose_name='stt결과')
    LipNetResult = models.CharField(max_length=20, null=True, verbose_name='독순비교결과')
    sttResult = models.CharField(max_length=20, null=True, verbose_name='stt비교결과')


class WordList(models.Model):
    word = models.CharField(max_length=20, null=True, verbose_name='제시단어목록')

    def __str__(self):
        return self.word