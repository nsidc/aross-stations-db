from fastapi import APIRouter

from aross_stations_db.api.v1.climatology import router as climatology_router
from aross_stations_db.api.v1.stations import router as stations_router
from aross_stations_db.api.v1.timeseries import router as timeseries_router
from aross_stations_db.api.v1.totals import router as totals_router

router = APIRouter()
router.include_router(stations_router, prefix="/stations")
router.include_router(timeseries_router, prefix="/events/timeseries")
router.include_router(climatology_router, prefix="/events/climatology")
router.include_router(totals_router, prefix="/events/totals")