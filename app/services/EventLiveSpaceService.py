from app.repositories import EventLiveSpaceRepository
from app.exceptions.InternalServerError import InternalServerError
from app.models.EventLiveSpace import EventLiveSpace
from app.dto.CreateLiveSpaceDTO import CreateLiveSpaceDTO
from app.services.ChatService import create_chatroom
from datetime import datetime
from zoneinfo import ZoneInfo


async def create_live_space(liveSpaceData: CreateLiveSpaceDTO):
    try:
        chatroomId = await create_chatroom(liveSpaceData.agoraChatUser)
        createdLiveStream = EventLiveSpace(createdBy=liveSpaceData.createdBy, eventId=liveSpaceData.eventId, channelId=liveSpaceData.username, createdAt=str(
            datetime.now(ZoneInfo('UTC'))), photoUrl=liveSpaceData.photoUrl, chatroomId=chatroomId)
        EventLiveSpaceRepository.insert_event_live_space(createdLiveStream)
        return createdLiveStream.to_dict()
    except Exception as e:
        raise InternalServerError(
            f"Error while creating live stream video. Error: {str(e)}")
