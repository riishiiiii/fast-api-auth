from fastapi import FastAPI
import uvicorn
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv(".env"))

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", default="0.0.0.0"),
        port=int(os.getenv("BACKEND_PORT", default=8000)),
        reload=os.getenv("RELOAD", default=False),
    )
