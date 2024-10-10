
from fastapi import APIRouter, HTTPException
from db.schemas import *
from db.crud import *

router = APIRouter(
    tags=["aralipform"],
    responses={404: {"description": "Error in calling aralipform API"}},
)

router = APIRouter()

@router.post("/api/submitform/") 
async def submit_record_api(record: ArabidopsisRecord):
    try:
        await submit_record(record)
        return {"message": "Record inserted successfully"}
    except Exception as e:
        return {"message": str(e)}

# Since it does not need to be live right now, commenting out api
#@router.get("/api/fetchformrecords/")
async def fetch_records_api():
    try:
        records = await fetch_records()
        return records
    except Exception as e:
        return {"message": str(e)}
