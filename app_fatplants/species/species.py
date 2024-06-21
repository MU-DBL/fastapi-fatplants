from fastapi import APIRouter
from db import crud
from db.helper import *
from blast import blastp

router = APIRouter(
    tags=["species"],
    # dependencies=[Depends(jwt.JWTBearer())],
    responses={404: {"description": "Error in calling species API"}},
)

@router.get('/get_species_records/')
async def get_Species_Records(species: str,expression: str):
    if is_sql_injection(expression) or is_sql_injection(species):
        return {"Error": "Invalid input values"}
    
    if species=='cuphea' or species=='pennycress':
        result= await crud.get_species_details_records(species, expression)
        return result

    fpid_list= await crud.get_fpids_index(species,expression)
    
    if len(fpid_list) > 0:
        result= await crud.get_species_records_identifier(species,fpid_list)
        return result
    return []

@router.get('/details/')
async def get_Details_By_FPID(species: str, id: str):
    res=await crud.get_details_by_fpid(species, id)
    return res

@router.get('/uniprot/')
async def get_Base_By_Uniprot(species: str, uniprot: str):
    res=await crud.get_base_data_by_uniprot(species, uniprot)
    return res

@router.get('/tair/')
async def get_Base_Lmpd_By_Tair(species: str, tair: str):
    res=await crud.get_data_by_tair(species, tair)
    return res

@router.get('/sample/')
async def get_Sample_Data_By_Species(species: str):
    res=await crud.load_sample_data(species)
    return res

@router.get('/fatty_acid_search/')
async def search_Fatty_Acids(query: str):
    res=await crud.fatty_acid_search(query)
    return res

@router.get('/homolog/')
async def get_Homologs_For_Uniprot_ID(uniprot_id: str):
    res= await crud.get_homolog_uniprots(uniprot_id)
    return res

@router.get('/sequence_search/')
async def search_By_Sequence(species: str, sequence: str):
    res=await crud.sequence_search(species, sequence)
    return res

@router.get('/blast/')
async def blast(database: str, sequence: str, parameters: str):
    if database.isalpha() or sequence.isalpha():
        res=await blastp.getResult(database, sequence, parameters)
        return res
    else:
        return {"Error": "Invalid input values"}
   
@router.get('/PSI_blast/')
async def PSI_blast(database: str, sequence: str, parameters: str):
    if database.isalpha() or sequence.isalpha():
        res=await blastp.getPSIBlastResult(database, sequence, parameters)
        return res
    else:
        return {"Error": "Invalid input values"}
   
#by Sam, for phase out Firestore
@router.get('/species_mapper/')
async def get_species_mapper(speciesName: str, q: str):
    if speciesName != "arabidopsis" and speciesName != "camelina" and speciesName != "soya":
        raise HTTPException(status_code=500, detail="Invalid speciesName")
    if is_sql_injection(speciesName) or is_sql_injection(q):
        raise HTTPException(status_code=500, detail="Invalid input values")
    res=await crud.get_species_mapper(speciesName, q)
    return res
   
