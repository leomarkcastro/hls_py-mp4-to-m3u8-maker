import os 
import shutil

def preprocess_m3u8(file_location, file_id, object_point):
  # sample: test.m3u8 => https://file-asia-se-01-api.db.srv01.xyzapps.xyz/streams/test.m3u8
  
  # read the m3u8 file as a text
  with open(file_location, 'r') as file:
    data = file.read()

    # replace the content of the m3u8 file where each instance of <file_id> is replaced with <object_point>
    data = data.replace(file_id, object_point)

    # overwrite the m3u8 file with the new content
    with open(file_location, 'w') as file:
      file.write(data)
    
    return file_location

def delete_folder_contents(folder_loc):
  # delete all files in the folder
  for filename in os.listdir(folder_loc):
    file_path = os.path.join(folder_loc, filename)
    try:
      if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
      elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
    except Exception as e:
      print('Failed to delete %s. Reason: %s' % (file_path, e))

def video_id():
  # generate hash (8 chars)
  import uuid
  return str(uuid.uuid4())[:8]

def get_folder_total_size(folder_loc):
  # get total size of the folder
  total_size = 0
  for dirpath, dirnames, filenames in os.walk(folder_loc):
    for f in filenames:
      fp = os.path.join(dirpath, f)
      total_size += os.path.getsize(fp)
  # split total_size from 123456 to 123_456
  total_size = f"{total_size:,}"
  return total_size