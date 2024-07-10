import fastapi
from app.routers import UserRouter as userRouter
from app.routers import PlaceRouter as placerRouter
from app.routers import MusicGenreRouter as musicGenreRouter
from app.routers import AgoraRouter as agoraRouter
from app.routers import EventRouter as eventRouter
from app.routers import ChatRouter as chatRouter
from app.routers import LiveVideoRouter as liveStreamRouter
from app.routers import EventLiveSpaceRouter as eventLiveSpaceRouter
from app.routers import TagsRouter as tagsRouter
from app.routers import FavoriteEventRouter as favoriteEventRouter
from app.routers import JoinEventRequestRouter as joinEventRequestRouter
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('./service-key-firebase.json')
firebase_admin.initialize_app(cred)

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],  # Or specify just the methods your API uses
    allow_headers=["*"],
)

#Register routes to the context
app.include_router(userRouter.userRouter)
app.include_router(placerRouter.placeRouter)
app.include_router(musicGenreRouter.userRouter)
app.include_router(agoraRouter.agoraRouter)
app.include_router(liveStreamRouter.liveVideoRouter)
app.include_router(eventRouter.eventRouter)
app.include_router(tagsRouter.tagsRouter)
app.include_router(favoriteEventRouter.favoriteEventRouter)
app.include_router(joinEventRequestRouter.joinEventRequestRouter)
app.include_router(chatRouter.chatRouter)
app.include_router(eventLiveSpaceRouter.eventLiveSpaceRouter)

add_pagination(app)



