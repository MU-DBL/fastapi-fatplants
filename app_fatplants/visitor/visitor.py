from fastapi import APIRouter, HTTPException
from db import crud

router = APIRouter(
    tags=["visitor"],
    responses={404: {"description": "Error in calling visitor API"}},
)

@router.get('/api/monthly-hits')
async def get_monthly_hits():
    try:
        res = await crud.get_monthly_hits()
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/api/location-hits')
async def get_location_hits():
    try:
        res = await crud.get_location_hits()
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 