# coding: utf-8
import boto3
session = boto3.Session(profile_name="devuser")
session
s3 = session.resource('s3')
s3
for bucket in s3.buckets.all():
    print(bucket)
    
new_bucket = s3.create_bucket(Bucket='webhostcoder00907471')
get_ipython().run_line_magic('history', '')
new_bucket = s3.create_bucket(Bucket='webhostcoder00907471', CreateBucketConfiguration={'LocationConstraint': new_bucket.region})
new_bucket = s3.create_bucket(Bucket='webhostcoder00907471', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
new_bucket = s3.create_bucket(Bucket='webhostcoder009074712', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
for bucket in s3.buckets.all():
    print(bucket)
    
new_bucket
get_ipython().run_line_magic('save', 'ipythonsession.py 1-30')
