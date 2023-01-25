# Importing Python packages
import boto3
from environs import Env
from passlib.hash import pbkdf2_sha256
from typing import Tuple


# ---------------------------------------------------------------------------------------------------


env = Env()
env.read_env()
aws_access_key_id = env("AWS_ACCESS_KEY_ID")
aws_secret_access_key = env("AWS_SECRET_ACCESS_KEY")
region_name = env("REGION_NAME")


# AWS S3 Client Object
s3_client = boto3.client(
    's3',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key,
    region_name = region_name
)


def partial_update_query(record: Tuple):
    key, value = record
    if isinstance(value, int) or isinstance(value, float):
        return f"{key}={value},"
    elif isinstance(value, str):
        if key == "password":
            return f"{key}='{pbkdf2_sha256.hash(value)}',"
        return f"{key}='{value}',"
    else:
        return str()
