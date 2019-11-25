#!/usr/bin/python3
import boto3
import click

session = boto3.Session(profile_name="devuser")
s3 = session.resource('s3')


@click.group()
def cli():
    """ Script deployes websites to AWS """
    pass


@cli.command('list-buckets')
def list_buckets():
    """ List all S3 bucket """
    for bucket in s3.buckets.all():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """ List Objects in an S3 bucket """
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)


if __name__ == "__main__":
    cli()
