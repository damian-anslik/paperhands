import fastapi
from app import routers

app = fastapi.FastAPI()
app.include_router(routers.user_router)
app.include_router(routers.portfolio_router)
app.include_router(routers.orders_router)