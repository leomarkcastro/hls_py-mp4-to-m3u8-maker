import json
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from .services.stream_create import create
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os


# Create your views here.
@csrf_exempt
def test2(request):
    if request.method == 'POST' and request.FILES['myfile']:

        myfile = request.FILES['myfile']

        fs = FileSystemStorage(
            location="./converted_images"
        )
        filename = fs.save(myfile.name, myfile)

        # get file location in server
        file_location = fs.path(filename)
        jpg_to_png = file_location.replace(".jpg", ".png")
        create(file_location, jpg_to_png)

        # send file back to client via http response
        with open(jpg_to_png, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/png")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(jpg_to_png)
            return response

    return render(request, 'core/index.html')


@csrf_exempt
def create_view(request):
    if request.method == 'POST' and request.FILES['myfile']:

        myfile = request.FILES['myfile']

        # save received video to local
        fs = FileSystemStorage(
            location="./to_convert"
        )
        filename = fs.save(myfile.name, myfile)

        # get file location in server
        file_location = fs.path(filename)

        # create ffmpeg stream

        # upload files to s3

        # send back json response
        json_response = {
            "status": "ok",
            "message": "file uploaded successfully",
            "file_location": file_location
        }
        json_string = json.dumps(json_response)
        json_stringb = json_string.encode("utf-8")
        return HttpResponse(json_stringb, content_type="application/json")

    return render(request, 'core/index.html')


@csrf_exempt
def test(request):
    return HttpResponse(b"hello world")
