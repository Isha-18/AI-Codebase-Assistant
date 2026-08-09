import logging

from fastapi import FastAPI


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

from api.routes import router


app = FastAPI(
    title="AI Codebase Assistant",
    version="1.0.0",
)

app.include_router(router)