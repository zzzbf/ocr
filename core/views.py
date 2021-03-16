from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from demo.settings import OCR as ocr
from demo.settings import UPLOAD_DIR
import cv2
import numpy
import os
import uuid


class IndexView(generics.GenericAPIView):
    @staticmethod
    def get(request):
        return render(request, "core/index.html")

    @staticmethod
    def post(request):
        file = request.FILES['file']
        image_path = os.path.join(UPLOAD_DIR, str(uuid.uuid4()).replace("-", "_"))

        with open(image_path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
        print(image_path)
        np_images = [cv2.imread(image_path)]
        results = ocr.recognize_text(
            images=np_images,
            use_gpu=False,
            visualization=False,
            box_thresh=0.5,
            text_thresh=0.5)
        response = {"result": []}
        for result in results:
            data = result['data']
            for infomation in data:
                response['result'].append(infomation)
        return Response(response)
