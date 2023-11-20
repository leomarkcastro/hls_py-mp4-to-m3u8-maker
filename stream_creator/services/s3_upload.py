import boto3
import os

def upload_file_using_client(file_name, object_name):
    """
    Uploads file to S3 bucket using S3 client object
    :return: None
    """
    s3 = boto3.client("s3", 
        aws_access_key_id=os.getenv('S3_ACCESSKEY'),
        aws_secret_access_key=os.getenv('S3_SECRETKEY'),
        endpoint_url=os.getenv('S3_ENDPOINTURL')
    )
    bucket_name = os.getenv('S3_BUCKETNAME')
    s3.upload_file(file_name, bucket_name, object_name)
    return

def upload_folder_using_client(folder_location):
    s3 = boto3.client("s3", 
        aws_access_key_id=os.getenv('S3_ACCESSKEY'),
        aws_secret_access_key=os.getenv('S3_SECRETKEY'),
        endpoint_url=os.getenv('S3_ENDPOINTURL')
    )
    bucket_name = os.getenv('S3_BUCKETNAME')

    # get all files in the folder
    files = os.listdir(folder_location)

    # upload each file to s3
    for file in files:
        s3.upload_file(folder_location + "/" + file, bucket_name, file)
    return