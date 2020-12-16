from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
import cv2 
import matplotlib.pyplot as plt
from keras.models import model_from_json
import numpy as np
import urllib
import string 
import random 
import os
from Latex.Latex import Latex
import tensorflow as tf
import tensorflow.contrib.legacy_seq2seq as seq2seq



json_file = open('model1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model1.h5")
labels = ['!', '(', ')', '+', ',', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', 'A', 'alpha', 'ascii_124', 'b', 'beta', 'C', 'cos', 'd', 'Delta', 'div', 'e', 'exists', 'f', 'forall', 'forward_slash', 'G', 'gamma', 'geq', 'gt', 'H', 'i', 'in', 'infty', 'int', 'j', 'k', 'l', 'lambda', 'ldots', 'leq', 'lim', 'log', 'lt', 'M', 'mu', 'N', 'neq', 'o', 'p', 'phi', 'pi', 'pm', 'prime', 'q', 'R', 'rightarrow', 'S', 'sigma', 'sin', 'sqrt', 'sum', 'T', 'tan', 'theta', 'times', 'u', 'v', 'w', 'X', 'y', 'z', '[', ']', '{', '}']


def EquationHome(request):
    return render(request,'index.html')

def EquationImage(request):
    return render(request,'index2.html')

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
    latex = model.predict(formula)

   
    return Response({
        "eqn":latex
    })
    


@api_view(['POST'])
def Detect(request):

    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 6)) 
   
    if 'img' in request.POST:
        imgURL = "data:image/png;"+request.POST['img'].replace("$","+").replace(" ","+")
        f = open(res+'.txt','w')
        f.write(imgURL)
        f.close()
        resp = urllib.request.urlretrieve(imgURL)
        image = cv2.imread(resp[0])
        image = ~image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8)) 
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_KCOS) 

        im2 = image.copy()
        contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
        
        charList = []

        for cnt in contours: 
            x, y, w, h = cv2.boundingRect(cnt) 
            
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2) 
            cropped = image[y:y + h, x:x + w]
            image1 = cropped.copy()
            image1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
            image1 = cv2.threshold(image1,127,255,cv2.THRESH_BINARY_INV)[1]
            
            imgHeight = len(image1)
            imgWidth = len(image1[0])
            
            pleft = 0
            ptop = 0
            if imgHeight>imgWidth:
                pleft = int((imgHeight - imgWidth)/2)
            else:
                ptop = int((imgWidth-imgHeight)/2)
                
            
            image1 = cv2.copyMakeBorder(image1, ptop, ptop, pleft, pleft, cv2.BORDER_CONSTANT)

            image1 = cv2.resize(image1,(45,45))
            image1 = image1.reshape(-1, 45, 45, 1)
            image1 = image1.astype('float32')
            image1 /= 255.0

            
            
            charList.append(labels[np.argmax(loaded_model.predict(image1))])
        print("\n\nCharacter List :"+str(charList))


        for ii in range(len(charList)-1):
            if  charList[ii] == '-' and charList[ii+1] == '-':
                charList[ii] = '='
                charList[ii+1] = ''

        if '' in charList:
            charList.remove('')

        os.remove(res+".txt") 

        return Response({
            "char":str(charList)
        })

    return Response({
            "char":"No Character found"
        })

def Blob(request,a):
    return CustomSchemeRedirect("blob:127.0.0.1:8000/"+a)

class CustomSchemeRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ['blob']