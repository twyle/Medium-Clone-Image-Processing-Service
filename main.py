import boto3

S3_BUCKET='flask-image-service'
AWS_ACCESS_KEY='AKIATSBC6QTDG7STZG4Q'
AWS_ACCESS_SECRET='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'

s3 = boto3.client(
   "s3",
   aws_access_key_id=AWS_ACCESS_KEY,
   aws_secret_access_key=AWS_ACCESS_SECRET
)

# buckets = s3.list_buckets()
# for b in buckets['Buckets']:
#     print(b)

# List all objects in a bucket
# response = s3.list_objects_v2(Bucket=S3_BUCKET)
# for obj in response["Contents"]:
#     print(obj)
    
# Upload file to bucket [Show with public-read, and without it too]
# with open("api/config/uploaded-images/aws-credit.png", "rb") as f:
#     print(f.name)
#     s3.upload_fileobj(f, S3_BUCKET, "aws-credit.png")

# Presigned URL to give limited access to an unauthorized user
url = s3.generate_presigned_url(
    "get_object", Params={"Bucket": S3_BUCKET, "Key": "aws-credit.png"}, ExpiresIn=30
)
print(url)