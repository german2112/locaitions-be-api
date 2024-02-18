from app.repositories import PhotoRepository as photoRepository
from dotenv import load_dotenv
from app.common import constants
import os
import boto3

load_dotenv()

session = boto3.Session(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                        region_name=os.getenv("AWS_REGION")
                      )

def find_photos_by_user_uid(uid: str):
    photos = photoRepository.find_by_user_uid(uid)
    photos_modified = list(photos)
    for photo in photos_modified:
        photo['_id'] = str(photo['_id'])
    return {"message": "ok", "body": photos_modified}

def find_photo_and_delete(id: str):
    """ bucketName = constants.AWS_BUCKET_NAME
    client = session.resource("s3")
    bucket = client.Bucket(bucketName)
    
    bucket.delete_objects() """
    photoRepository.delete_by_id(id)
    return {"message": "ok"}
    