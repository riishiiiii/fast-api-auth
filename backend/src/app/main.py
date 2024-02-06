from fastapi import FastAPI
import uvicorn
import dotenv
import os
from api.auth import router

from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv(dotenv.find_dotenv(".env"))

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router, prefix="/auth", tags=["auth"])
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", default="0.0.0.0"),
        port=int(os.getenv("BACKEND_PORT", default=8000)),
        reload=os.getenv("RELOAD", default=False),
    )
