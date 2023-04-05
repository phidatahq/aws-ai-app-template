from phidata.aws.resource.s3.bucket import S3Bucket

from workflows.env import RUNTIME_ENV
from workspace.dev.aws_config import dev_data_s3_bucket
from workspace.prd.aws_config import prd_data_s3_bucket

# -*- S3 Buckets

# S3 bucket for storing data
DATA_S3_BUCKET: S3Bucket
if RUNTIME_ENV == "prd":
    DATA_S3_BUCKET = prd_data_s3_bucket
else:
    DATA_S3_BUCKET = dev_data_s3_bucket
