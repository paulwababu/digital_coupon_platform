from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from tutorials import views

urlpatterns = [
    #path('tutorials/upload/', views.uploadTutorial, name='upload_tutorial'),
    path('scanner/', views.scanner, name="scanner"),
    path('tutorials/', views.tutorialList, name='tutorial_list'),
    path('tutorials/<int:pk>', views.deleteTutorial, name='tutorial'),
    ##
    path('', views.phone, name="login"),
    path('otp/', views.otp, name="otp"),
    path('ocr/', views.ocr, name="ocr"),
    path('success/', views.success, name = 'success'),
]

if settings.DEBUG:  # remember to set 'DEBUG = True' in settings.py
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
