from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from reports import router as reports_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allow_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(reports_router)
    return app


app = create_app()
