from fastapi import FastAPI

from aross_stations_db.api.v1.routes import router as v1_router

api = FastAPI(
    title=(
        "Rain on snow events detected by"
        " Automated Surface Observing System (ASOS) stations"
    ),
)
api.include_router(v1_router, prefix="/v1", tags=["v1"])


@api.get("/")
def get():
    return {
        "Hello": "The root of this API doesn't do anything. Please check out '/docs'!"
    }
