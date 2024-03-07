from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get
import boto3

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")
aws_region = os.getenv("AWS_REGION")
aws_bucket_name = os.getenv("AWS_BUCKET_NAME")

# Check that all required environment variables are set
if not all([client_id, client_secret, aws_access_key, aws_secret_key, aws_region, aws_bucket_name]):
    raise Exception("One or more required environment variables are not set")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# search for classical music
def search_for_classical_music(token):
    url = "https://api.spotify.com/v1/search?"
    headers = get_auth_header(token)
    query = f"q=classical&type=playlist,album,track&limit=50"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def upload_to_s3(bucket_name, file_name, data):
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
        )
    try:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=data)
    except Exception as e:
        print(f"Failed to upload data to S3: {e}")
        raise

token = get_token()
classical_music_metadata = search_for_classical_music(token)
classical_music_metadata_str = json.dumps(classical_music_metadata)

upload_to_s3(aws_bucket_name, "classical_music_metadata.json", classical_music_metadata_str)