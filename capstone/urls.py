from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from .views import FileDownloadView

app_name = "capstone"

urlpatterns = [
    # path("", views.uploadFile, name="uploadFile"),
    path("", views.capstoneMain, name='capstoneMain'),
    # path('capstone/', views.index),
    path("upload/<ran_word>/", views.uploadAnalyze, name="uploadAnalyze"),
    # path("download/", views.downloadFile, name="downloadFile"),
    # path('document/<int:document_id>/', FileDownloadView.as_view(), name="download"),
    path("deleteFile/", views.deleteFile, name="deleteFile"),

    # path('answer/delete/', views.pytest, name='pytest1'),
    # path("capstoneMain/", views.capstoneMain, name='capstoneMain'),
    path("dostt/", views.stt, name='stt'),

    # path("doSomething/", views.pytest, name="pytest"),
    # path("", views.pytest, name="pytest"),

    path("show/result/<ran_word>/", views.show_result, name='show_result'),
    path("capstoneHome/", views.index, name="index"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
