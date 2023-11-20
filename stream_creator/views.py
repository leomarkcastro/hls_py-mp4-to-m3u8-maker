import json
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from .services.preprocess_stream import preprocess_m3u8, video_id, delete_folder_contents
from .services.stream_create import create
from .services.s3_upload import upload_folder_using_client
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def create_view(request):
    if request.method == 'POST' and request.FILES['myfile']:

        myfile = request.FILES['myfile']

        # save received video to local
        fs = FileSystemStorage(
            location="./to_convert"
        )
        filename = fs.save(myfile.name, myfile)

        # get file location in the local fs
        file_location = fs.path(filename)

        # generate video id
        vid_id = video_id()

        # change output file name from <original>.mp4 to converted.m3u8
        output_fs = FileSystemStorage(
            location="./converted"
        )
        # create folder if not exists
        if not os.path.exists(output_fs.location):
            os.makedirs(output_fs.location)
        output_fs_folderloc = output_fs.location
        output_file_location = output_fs.path(f"{vid_id}.m3u8")

        # create ffmpeg stream
        create(file_location, output_file_location)

        # preprocess the m3u8 file
        serv_url = os.getenv("S3_ENDPOINTURL", "")
        bucket_name = os.getenv("S3_BUCKETNAME", "")
        preprocess_m3u8(output_file_location, vid_id, f"{serv_url}/{bucket_name}/{vid_id}")

        # upload files to s3
        upload_folder_using_client(output_fs_folderloc)

        # delete files in the local fs
        delete_folder_contents(fs.location)
        delete_folder_contents(output_fs.location)

        # send back json response
        json_response = {
            "status": "ok",
            "message": "file uploaded successfully",
            "m3u8": f"{serv_url}/{bucket_name}/{vid_id}.m3u8"
        }
        json_string = json.dumps(json_response)
        json_stringb = json_string.encode("utf-8")
        return HttpResponse(json_stringb, content_type="application/json")

    return render(request, 'core/index.html')


@csrf_exempt
def test(request):
    return HttpResponse(b"hello world")
