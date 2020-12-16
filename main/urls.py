from django.urls import path
from .views import EquationHome,Detect,Blob,EquationImage,DetectI

urlpatterns = [
    path('EqHome',EquationHome),
    path('EqI',EquationImage),
    path('detect',Detect),
    path('detectI',DetectI),
    path('<str:a>',Blob)
]