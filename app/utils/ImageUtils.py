from fastapi import UploadFile
from app.common import constants
from app.exceptions.InternalServerError import InternalServerError
import os


def is_image_explicit(content: bytes, session):
    client = session.client('rekognition')

    response = client.detect_moderation_labels(Image={'Bytes': content})

    # TODO Migrate to enum class
    explictyDefinition = {"Explicit Nudity": "Explicit Nudity",
                          "Suggestive": "Suggestive",
                          "Violence": "Violence",
                          "Visual Disturbing": "Visual Disturbing",
                          "Rude Gestures": "Rude Gestures",
                          "Drugs": "Drugs",
                          "Tobacco": "Tobacco",
                          "Alcohol": "Alcohol",
                          "Gambling": "Gambling",
                          "Hate Symbols": "Symbols"}

    for label in response['ModerationLabels']:
        if explictyDefinition.get(label.get("ParentName")):
            return True

    return False


async def upload_image_to_S3(session, file: UploadFile):
    if not is_image_explicit(file.file.read(), session):
        await file.seek(0)
        client = session.resource("s3")
        bucket = client.Bucket(constants.AWS_BUCKET_NAME)
        formatted_name = os.path.basename(file.filename)
        bucket.upload_fileobj(file.file, formatted_name)
        return f"https://{constants.AWS_BUCKET_NAME}.s3.amazonaws.com/{formatted_name}"
    else:
        raise InternalServerError(
            f"File: {formatted_name} cannot be uploaded to S3 as it contains explicit content.")
