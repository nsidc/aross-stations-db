from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aross_stations_db.api.v1.routes import router as v1_router

api = FastAPI(
    title=(
        "Rain on snow events detected by"
        " Automated Surface Observing System (ASOS) stations"
    ),
    openapi_url="/api/aross-stations/openapi.json"
)
api.include_router(v1_router, prefix="/v1", tags=["v1"])
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/")
def get_root() -> dict[str, str]:
    return {
        "Hello": "The root of this API doesn't do anything. Please check out '/docs' or something!"
    }
