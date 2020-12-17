from django.urls import path
from .views import EquationHome,Detect,Blob,EquationImage,DetectI,FileUploadView,test

urlpatterns = [
    path('EqHome',EquationHome),
    path('EqI',EquationImage),
    path('detect',Detect),
    path('detectI',DetectI),
    path('<str:a>',Blob),
    path('ui', FileUploadView.as_view()),
    path('uij', test),
    
]