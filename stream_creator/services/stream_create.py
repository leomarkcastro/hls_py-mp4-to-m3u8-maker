
def run_on_cmd_and_wait(cmd):
    import subprocess as sp
    proc = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = proc.communicate()
    return out, err

def create(file_path, output_path):
    stream_cmd_command = f'ffmpeg -i "{file_path}" -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{output_path}"'
    return run_on_cmd_and_wait(stream_cmd_command)