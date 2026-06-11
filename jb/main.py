from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jb.apps.branch.adapter.inbound.api import branch_router
from jb.apps.briefing.adapter.inbound.api import briefing_router
from jb.apps.chat.adapter.inbound.api import chat_router
from jb.apps.phishing.adapter.inbound.api import phishing_router
from jb.apps.report.adapter.inbound.api import report_router
from jb.apps.reservation.adapter.inbound.api import reservation_router
from jb.apps.savings.adapter.inbound.api import savings_router

app = FastAPI(title="JB Silver Connect API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_API_PREFIX = "/api/v1"
for _router in (
    briefing_router,
    reservation_router,
    savings_router,
    phishing_router,
    branch_router,
    report_router,
    chat_router,
):
    app.include_router(_router, prefix=_API_PREFIX)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "JB Silver Connect API", "docs": "/docs"}
