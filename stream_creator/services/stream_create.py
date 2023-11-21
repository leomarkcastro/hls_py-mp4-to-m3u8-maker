
def run_on_cmd_and_wait(cmd):
    import subprocess as sp
    proc = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = proc.communicate()
    return out, err

bandwidth_resolution_map = {
    "144p": ["200000", "256x144"],
    "240p": ["400000", "426x240"],
    "480p": ["800000", "854x480"],
    "720p": ["1500000", "1280x720"],
    "1080p": ["3000000", "1920x1080"],
}

video_quality_templates = {
    "144p": lambda: ([
        "-vf", "scale=-2:144",
        "-b:v", "200k",
        "-c:a", "aac",
        "-ar", "48000",
        "-c:v", "h264",
    ]),
    "240p": lambda: ([
        "-vf", "scale=-2:240",
        "-b:v", "400k",
        "-c:a", "aac",
        "-ar", "48000",
        "-c:v", "h264",
    ]),
    "480p": lambda: ([
        "-vf", "scale=-2:480",
        "-b:v", "800k",
        "-c:a", "aac",
        "-ar", "48000",
        "-c:v", "h264",
    ]),
    "720p": lambda: ([
        "-vf", "scale=-2:720",
        "-b:v", "1500k",
        "-c:a", "aac",
        "-ar", "48000",
        "-c:v", "h264",
    ]),
    "1080p": lambda: ([
        "-vf", "scale=-2:1080",
        "-b:v", "3000k",
        "-c:a", "aac",
        "-ar", "48000",
        "-c:v", "h264",
    ]),
}

def create_hls_stream(file_path, output_path, quality="480p", segment_duration=10):
    # stream_cmd_command = f'ffmpeg -i "{file_path}" -hls_time 10 -hls_list_size 0 -f hls "{output_path}"'
    # run_on_cmd_and_wait(stream_cmd_command)

    # create a video with lower bitrate and smaller video width and height
    stream_cmd_command = [
        'ffmpeg',
        '-i', f'"{file_path}"',
        *video_quality_templates[quality](),
        '-hls_time', f'{segment_duration}', # 10 seconds segment duration
        '-hls_list_size', '0', # no limit on the number of playlist entries
        '-f', 'hls',
        f'"{output_path}"'
    ]
    stream_cmd_command = " ".join(stream_cmd_command)
    print(f" > {stream_cmd_command}")
    return run_on_cmd_and_wait(stream_cmd_command)

def create_master_playlist(quality_defs, server_loc, output_path):
    definitions = ["#EXTM3U"]
    # print(quality_defs)
    for quality_def in quality_defs:
        bandwidth = quality_def[0]
        resolution = quality_def[1]
        path = quality_def[2]
        definitions.append(f'#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={resolution}\n{server_loc}{path}')
    
    with open(output_path, "w") as f:
        f.write("\n".join(definitions))
