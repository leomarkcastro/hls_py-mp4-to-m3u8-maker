import json
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from .services.preprocess_stream import get_folder_total_size, preprocess_m3u8, video_id, delete_folder_contents
from .services.stream_create import create_hls_stream, bandwidth_resolution_map, create_master_playlist
from .services.s3_upload import upload_folder_using_client
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def create_view(request):
    if request.method == 'POST' and request.FILES['myfile']:

        # get qualities list from query params
        qualities = request.GET.getlist('qualities[]')

        # if no qualities are specified, use default
        if len(qualities) == 0:
            qualities = ["144p", "240p", "480p"]

        # get segment duration from query params
        segment_duration = request.GET.get('segment_duration', 10)

        myfile = request.FILES['myfile']

        # save received video to local
        fs = FileSystemStorage(
            location="./to_convert"
        )
        filename = fs.save(myfile.name, myfile)

        # get file location in the local fs
        file_location = fs.path(filename)

        # create output folder
        output_fs = FileSystemStorage(
            location="./converted"
        )
        # create folder if not exists
        if not os.path.exists(output_fs.location):
            os.makedirs(output_fs.location)

        # set variables 
        serv_url = os.getenv("S3_ENDPOINTURL", "")
        bucket_name = os.getenv("S3_BUCKETNAME", "")       
        quality_list = []

        for quality_tier in qualities:
            # generate video id
            vid_id = video_id()

            # change output file name from <original>.mp4 to converted.m3u8
            output_file_location = output_fs.path(f"{vid_id}.m3u8")

            # create ffmpeg stream
            create_hls_stream(file_location, output_file_location, quality_tier, segment_duration)

            # preprocess the m3u8 file
            preprocess_m3u8(output_file_location, vid_id, f"{serv_url}/{bucket_name}/{vid_id}")
            print(f"Done creating {quality_tier} stream for {filename}")

            # add to quality list
            quality_list.append([
                *bandwidth_resolution_map[quality_tier],
                f"{vid_id}.m3u8"
            ])
        
        # generate video id
        master_id = video_id()
        # create master playlist
        master_playlist_path = output_fs.path(f"master-{master_id}.m3u8")
        create_master_playlist(quality_list, f"{serv_url}/{bucket_name}/", master_playlist_path)

        # upload files to s3
        upload_folder_using_client(output_fs.location)

        # get file size
        input_file_size = get_folder_total_size(fs.location)
        total_size = get_folder_total_size(output_fs.location)

        # delete files in the local fs
        delete_folder_contents(fs.location)
        delete_folder_contents(output_fs.location)

        # send back json response
        json_response = {
            "status": "ok",
            "message": "file uploaded successfully",
            "input_file_size": input_file_size,
            "output_file_size": total_size,
            "master_playlist": f"{serv_url}/{bucket_name}/master-{master_id}.m3u8",
            "streams": list(
                map(
                    lambda x: f"{serv_url}/{bucket_name}/{x[2]}", 
                    quality_list
                )
            ),
        }
        json_string = json.dumps(json_response)
        json_stringb = json_string.encode("utf-8")
        return HttpResponse(json_stringb, content_type="application/json")

    return render(request, 'core/index.html')


@csrf_exempt
def test(request):
    return HttpResponse(b"hello world")
