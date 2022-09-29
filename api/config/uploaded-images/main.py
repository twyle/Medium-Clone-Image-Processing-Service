import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
   aws_secret_access_key=os.environ['AWS_ACCESS_SECRET']
)

S3_BUCKET = os.environ['S3_BUCKET']
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
image = 'aws-credit.png'

def upload_file_to_s3(file_path, bucket_name):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    with open(file_path, 'rb') as file:
        try:
            s3.upload_fileobj(
                file,
                bucket_name,
                os.path.basename(file.name)
            )
        except Exception as e: 
            raise e
        else:
            data = "{}{}".format(S3_LOCATION, os.path.basename(file.name))
            return data
        
upload_file_to_s3(image, S3_BUCKET)