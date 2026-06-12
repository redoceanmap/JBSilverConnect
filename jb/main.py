from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jb.apps.branch.adapter.inbound.api import branch_router
from jb.apps.chat.adapter.inbound.api import chat_router
from jb.apps.corporate.adapter.inbound.api import corporate_router
from jb.apps.queue.adapter.inbound.api import queue_router
from jb.apps.reservation.adapter.inbound.api import reservation_router

app = FastAPI(title="JB AI Connect API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", 
    "http://localhost:3001", "http://127.0.0.1:3001", 
    "http://localhost:3002","http://127.0.0.1:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_API_PREFIX = "/api/v1"
for _router in (
    reservation_router,
    branch_router,
    chat_router,
    queue_router,
    corporate_router,
):
    app.include_router(_router, prefix=_API_PREFIX)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "JB AI Connect API", "docs": "/docs"}
