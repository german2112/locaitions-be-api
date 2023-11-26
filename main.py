import fastapi
from app.routers import UserRouter as userRouter
from app.routers import PlaceRouter as placerRouter
from app.routers import MusicGenreRouter as musicGenreRouter

app = fastapi.FastAPI()

#Register routes to the context
app.include_router(userRouter.userRouter)
app.include_router(placerRouter.placeRouter)
app.include_router(musicGenreRouter.userRouter)



