import os, sys, boto3
s3 = boto3.client("s3", endpoint_url=os.getenv("S3_URL", "http://localhost:5000"), region_name="us-east-1",
                  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),

aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"))
bucket, path = "pipeline-artifacts", sys.argv[1]
try:
    s3.create_bucket(Bucket=bucket)
except s3.exceptions.BucketAlreadyOwnedByYou:
    pass
s3.upload_file(path, bucket, os.path.basename(path))
print("uploaded", path, "to", bucket)
