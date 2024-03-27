from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get
import boto3
import logging
import wikipedia
import time

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")
aws_region = os.getenv("AWS_REGION")
aws_bucket_name = os.getenv("AWS_BUCKET_NAME")

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Loading environment variables")
# Check that all required environment variables are set
if not all([client_id, client_secret, aws_access_key, aws_secret_key, aws_region, aws_bucket_name]):
    logging.error("One or more required environment variables are not set")
    raise Exception("One or more required environment variables are not set")

def get_token():
    try:
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
    except Exception as e:
        logging.error(f"Failed to retrieve access token: {e}")
        raise

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# search for classical music
def search_for_classical_music(token, limit=50, max_results=1000):
    try:
        url = "https://api.spotify.com/v1/search?"
        headers = get_auth_header(token)
        
        classical_music_metadata = []
        offset = 0
        
        while offset < max_results:
            query = f"q=classical&type=playlist,album,track&limit={limit}&offset={offset}"
            query_url = url + query
            result = get(query_url, headers=headers)
            json_result = json.loads(result.content)
            
            classical_music_metadata.extend(json_result["tracks"]["items"])
            
            offset += limit
            if len(json_result["tracks"]["items"]) < limit:
                break
        
        return classical_music_metadata
    except Exception as e:
        logging.error(f"Failed to search for classical music: {e}")
        raise

composer_cache = {}

def get_composer_background(composer):
    if composer in composer_cache:
        return composer_cache[composer]
    else:
        try:
            composer_page = wikipedia.page(composer)
            background_info = composer_page.summary
            composer_cache[composer] = background_info
            return background_info
        except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
            return None

def get_background_from_musicbrainz(composer):
    # Make a request to the MusicBrainz API to retrieve background information for the composer
    # Implement the code to parse the response and extract relevant information
    # Return the background information if found, otherwise return None
    pass

def get_background_from_classical_archives(composer):
    # Make a request to the Classical Archives API or scrape the website to retrieve background information for the composer
    # Return the background information if found, otherwise return None
    pass

def preprocess_classical_music_metadata(classical_music_metadata):
    preprocessed_data = []
    
    for track in classical_music_metadata:
        track_data = {
            "id": track["id"],
            "name": track["name"],
            "composer": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "duration_ms": track["duration_ms"],
            "popularity": track["popularity"],
            "background_info": ""
        }
        
        background_info = get_composer_background(track_data["composer"])
        
        if background_info is None:
            # Fallback to MusicBrainz
            background_info = get_background_from_musicbrainz(track_data["composer"])
        
        if background_info is None:
            # Fallback to Classical Archives
            background_info = get_background_from_classical_archives(track_data["composer"])
        
        if background_info is not None:
            track_data["background_info"] = background_info
        else:
            logging.warning(f"Couldn't find background information for composer '{track_data['composer']}'")
        
        preprocessed_data.append(track_data)
        
        # Rate limiting: Add a small delay between API calls
        time.sleep(0.5)
    
    return preprocessed_data


def upload_to_s3(bucket_name, file_name, data):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=data)
        logging.info(f"Data uploaded to S3 bucket '{bucket_name}' with key '{file_name}'")
    except Exception as e:
        logging.error(f"Failed to upload data to S3: {e}")
        raise

token = get_token()
classical_music_metadata = search_for_classical_music(token, max_results=1000)
preprocessed_data = preprocess_classical_music_metadata(classical_music_metadata)
classical_music_metadata_str = json.dumps(preprocessed_data)
upload_to_s3(aws_bucket_name, "classical_music_metadata.json", classical_music_metadata_str)