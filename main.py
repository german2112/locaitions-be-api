import fastapi
from app.routers import UserRouter as userRouter

app = fastapi.FastAPI()

#Register routes to the context
app.include_router(userRouter.userRouter)



