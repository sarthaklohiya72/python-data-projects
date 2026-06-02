import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
    region_name='ap-south-1'
)

bucket_name = 'sarthak-business-data'

# Upload your CSV files
files = ['orders.csv', 'inventory.csv', 'products.csv']

for file in files:
    if os.path.exists(file):
        s3.upload_file(file, bucket_name, f'data/{file}')
        print(f"✅ Uploaded: {file}")

# List files in bucket
print("\nFiles in S3 bucket:")
response = s3.list_objects_v2(Bucket=bucket_name)
for obj in response.get('Contents', []):
    print(f"  → {obj['Key']} ({obj['Size']} bytes)")