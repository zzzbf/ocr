from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from demo.settings import OCR as ocr
from demo.settings import UPLOAD_DIR
import cv2
import numpy
import os
import uuid
import base64

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

        img = cv2.imread(image_path)
        results = ocr.recognize_text(
            images=[img],
            use_gpu=False,
            visualization=False,
            box_thresh=0.5,
            text_thresh=0.5)
        response = {"result": []}

        for result in results:
            data = result['data']
            for information in data:
                response['result'].append(information)
                text_box_position = information['text_box_position']
                text_box_position = [tuple(i) for i in text_box_position]
                for i in range(4):
                    cv2.line(img, text_box_position[i], text_box_position[(i + 1) % 4], (0, 0, 255))
        response['base64'] = "data:image/jpeg;base64," + base64.b64encode(cv2.imencode(".jpeg", img)[1]).decode("utf-8")
        return Response(response)
