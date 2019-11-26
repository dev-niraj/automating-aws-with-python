# -*- Coding: utf-8 -*-

from botocore.exceptions import ClientError
import mimetypes
from pathlib import Path

"""Classes for S3 Buckets."""


class BucketManager:
    """Manage an S3 Bucket."""

    def __init__(self, session):
        """Create a BucketManager Object."""
        self.session = session
        self.s3 = session.resource('s3')

    def all_buckets(self):
        """Get an iterator for all S3 Buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket):
        """Get an iterator for all objects in bucket."""
        return self.s3.Bucket(bucket).objects.all()

    def init_bucket(self, bucket_name):
        """Create new abucket, or return existing one by name."""
        bucket = None

        try:
            bucket = self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                'LocationConstraint': self.session.region_name})
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                bucket = self.s3.Bucket(bucket_name)
            else:
                raise e

        return bucket

    def ste_policy(self, bucket):
        """Set bucket policy to be readable. by everyone"""
        policy = """
            {
            "Version":"2012-10-17",
                "Statement":[
                    {
                    "Sid":"PublicRead",
                    "Effect":"Allow",
                    "Principal": "*",
                    "Action":["s3:GetObject"],
                    "Resource":["arn:aws:s3:::%s/*"]
                    }
                ]
            }
        """ % bucket.name

        policy = policy .strip()

        pol = bucket.Policy()
        pol.put(Policy=policy)

    def configure_website(self, bucket):
        """Configure S3 Website hosting for bucket."""
        bucket.Website().put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        })

    @staticmethod
    def upload_file(bucket, path, key):
        """Upload Files to the bucket."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            }
        )

    def sync(self, pathname, bucket_name):
        """Sync Contents to S3."""
        bucket = self.s3.Bucket(bucket_name)

        root = Path(pathname).expanduser().resolve()

        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    self.upload_file(bucket, str(p), str(p.relative_to(root)))

        handle_directory(root)