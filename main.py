import fastapi
import uvicorn
from app import routers
from fastapi.middleware import cors

app = fastapi.FastAPI()
app.add_middleware(cors.CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(routers.user_router)
app.include_router(routers.portfolio_router)
app.include_router(routers.orders_router)
app.include_router(routers.symbols_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    