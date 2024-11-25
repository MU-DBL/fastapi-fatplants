from fastapi import APIRouter, HTTPException
from db.schemas import ArabidopsisRecord
from db.crud import submit_record, fetch_records
import re
from db.helper import *

router = APIRouter(
    tags=["aralipform"],
    responses={404: {"description": "Error in calling aralipform API"}},
)

def is_sql_injection_http(input_value):
    safe_input_pattern = re.compile(
        r'^\s*$'  # Matches empty string or string with only whitespace
        r'|'  # OR
        r'^[a-zA-Z0-9\s]+$'  # Matches alphanumeric characters and spaces
        r'|'  # OR
        r'^(https?:\/\/)?'  # HTTP or HTTPS protocols (optional)
        r'([\da-z\.-]+)\.'  # Domain name
        r'([a-z\.]{2,6})'  # Domain extension
        r'(\/[\w\.-]*)*'  # Path
        r'\/?$'  # Optional trailing slash
    )

    # Return False if the input matches the safe pattern (indicating it's safe), True otherwise
    return not safe_input_pattern.match(input_value)

def validate_input(record: ArabidopsisRecord) -> None:
    fields = record.dict()
    for key, value in fields.items():
        if isinstance(value, str) and value != None :
            # Check URL fields with a specific pattern allowing more characters
            if key in ['record_url', 'figure_url', 'pubmed_link_1', 'pubmed_link_2', 'pubmed_link_3']:
                if is_sql_injection_http(value):
                    raise HTTPException(status_code=400, detail=f"Potential SQL injection detected in URL field: {key}")
            if key not in ['record_type', 'pathway', 'subcellular_location_listed', 'evidence_for_function_listed']:
                if is_sql_injection(value):
                    raise HTTPException(status_code=400, detail=f"Potential SQL injection detected in field: {key}")

@router.post("/api/submitform/")
async def submit_record_api(record: ArabidopsisRecord):
    validate_input(record)  # Perform SQL injection checks before processing
    try:
        await submit_record(record)
        return {"message": "Record inserted successfully"}
    except Exception as e:
        return {"message": str(e)}

@router.get("/api/fetchformrecords/")
async def fetch_records_api():
    try:
        records = await fetch_records()
        return records
    except Exception as e:
        return {"message": str(e)}
