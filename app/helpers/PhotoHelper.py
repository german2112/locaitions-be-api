from app.utils.ImageUtils import upload_image_to_S3
from app.factories.AwsFactory import create_aws_session
from app.models.Photo import PhotoSchema
from typing import List
from fastapi import UploadFile
from datetime import datetime
from app.exceptions.InternalServerError import InternalServerError
import uuid
from zoneinfo import ZoneInfo

async def format_photos_to_insert(files: List[UploadFile], isProfile: bool):
    try:
        session = create_aws_session()
        photoUrl = ''
        formattedPhotosList: List[dict] = []
        for file in files:
            photoUUID = str(uuid.uuid4())
            photoUrl = await upload_image_to_S3(session, file, photoUUID)
            photo = PhotoSchema(id=photoUUID,
                                filename=file.filename, 
                                fileUrl=photoUrl, 
                                createdAt=str(datetime.now(ZoneInfo('UTC'))), 
                                isProfile=isProfile)
            formattedPhotosList.append(photo.to_dict())
        return formattedPhotosList
    except Exception as e:
        raise InternalServerError(f"Error formatting new event photos. Error: {str(e)}")