from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework import status
from .serializer import FileSerializer
import cv2 
#from keras.models import model_from_json
import numpy as np
import urllib
import string 
import random 
import os
from skimage import io
from Latex.Latex import Latex
import tensorflow as tf
from pylatexenc.latex2text import LatexNodes2Text
import tensorflow.contrib.legacy_seq2seq as seq2seq
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 



"""json_file = open('model1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model1.h5")
"""

mean_train = np.load("train_images_mean.npy")
std_train = np.load("train_images_std.npy")

model2 = Latex("model", mean_train, std_train, plotting=False)
labels = ['!', '(', ')', '+', ',', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', 'A', 'alpha', 'ascii_124', 'b', 'beta', 'C', 'cos', 'd', 'Delta', 'div', 'e', 'exists', 'f', 'forall', 'forward_slash', 'G', 'gamma', 'geq', 'gt', 'H', 'i', 'in', 'infty', 'int', 'j', 'k', 'l', 'lambda', 'ldots', 'leq', 'lim', 'log', 'lt', 'M', 'mu', 'N', 'neq', 'o', 'p', 'phi', 'pi', 'pm', 'prime', 'q', 'R', 'rightarrow', 'S', 'sigma', 'sin', 'sqrt', 'sum', 'T', 'tan', 'theta', 'times', 'u', 'v', 'w', 'X', 'y', 'z', '[', ']', '{', '}']


def EquationHome(request):
    return render(request,'index.html')

def EquationImage(request):
    return render(request,'index2.html')

@api_view(['POST'])
def test(request):
    print("hello")
    return Response({""})


class FileUploadView(APIView):
    authentication_classes = []
    parser_class = (FileUploadParser,)


    def get(self, request, *args, **kwargs):
        print("vj")

        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['POST'])
def DetectI(request):
    if request.method == 'POST':
        return handle_uploaded_file(request.FILES['file'])

def handle_uploaded_file(f):
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 6)) 

    with open(res+'.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    formula = io.imread(res+'.jpg')
    latex = model2.predict(formula)

    eqn = latex['equation'].replace("#frac{","").replace("}{","/").replace("}","").replace(" #leq ","lt")
    print(eqn)
    
    
    return Response({
        "eqn":eqn,  
    })
    


@api_view(['POST'])
def Detect(request):

    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 6)) 
   
    if 'img' in request.POST:
        imgURL = "data:image/png;"+request.POST['img'].replace("$","+").replace(" ","+")
        resp = urllib.request.urlretrieve(imgURL)

        img = cv2.imread(resp[0])
        img = ~img
        img = cv2.resize(img, (720,200), interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("image.png",gray)


        formula = io.imread("image.png")
        latex = model2.predict(formula)
        print(latex['equation'])

        eqn = latex['equation'].replace("#frac{","").replace("}{","/").replace("}","").replace(" #leq ","lt")
        print(eqn)

        return Response({
            "char":eqn
        })

    return Response({
            "char":"No Character found"
        })

def Blob(request,a):
    return CustomSchemeRedirect("blob:127.0.0.1:8000/"+a)

class CustomSchemeRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ['blob']



