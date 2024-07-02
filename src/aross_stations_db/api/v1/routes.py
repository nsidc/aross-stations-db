from fastapi import APIRouter

from aross_stations_db.api.v1.stations import router as stations_router

router = APIRouter()
router.include_router(stations_router, prefix="/stations")
