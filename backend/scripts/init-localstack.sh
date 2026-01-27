#!/bin/bash
awslocal s3 mb s3://atlasnap-media
awslocal s3api put-bucket-cors --bucket atlasnap-media --cors-configuration '{
  "CORSRules": [{
    "AllowedOrigins": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
    "AllowedHeaders": ["*"],
    "ExposeHeaders": ["ETag"]
  }]
}'
echo "LocalStack S3 bucket created!"