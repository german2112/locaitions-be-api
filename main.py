import fastapi
from app.routers import UserRouter as userRouter
from app.routers import PlaceRouter as placerRouter

app = fastapi.FastAPI()

#Register routes to the context
app.include_router(userRouter.userRouter)
app.include_router(placerRouter.placeRouter)


