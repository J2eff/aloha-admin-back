import uvicorn
import multiprocessing
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import api
from settings import settings
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range"],
)

app.include_router(api.user.router)
if settings.PROJECT_ENV == "production":
    app.add_middleware(SentryAsgiMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":

    try:
        import uvloop
        loop = "uvloop"
    except ImportError:
        loop = "asyncio"
    try:
        import httptools
        http_tool = "httptools"
    except ImportError:
        http_tool = "h11"
    print(
        f"Starting Server : loop={loop}, http_tool={http_tool}, workers={multiprocessing.cpu_count()}"
    )
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=4321,
        loop=loop,
        http=http_tool,
        workers=multiprocessing.cpu_count(),
    )