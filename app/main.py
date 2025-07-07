from fastapi import FastAPI
from app.api import router
from app.utils import log_message

app = FastAPI(title="Product Price Fetcher")

log_message("info", "Starting FastAPI app...")

app.include_router(router)
