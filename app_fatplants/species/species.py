from fastapi import APIRouter, HTTPException
from db import crud
from db.helper import *
from blast import blastp

router = APIRouter(
    tags=["species"],
    # dependencies=[Depends(jwt.JWTBearer())],
    responses={404: {"description": "Error in calling species API"}},
)

@router.get('/api/get_species_records/')
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

@router.get('/api/details/')
async def get_Details_By_FPID(species: str, id: str):
    res=await crud.get_details_by_fpid(species, id)
    return res

@router.get('/api/uniprot/')
async def get_Base_By_Uniprot(species: str, uniprot: str):
    res=await crud.get_base_data_by_uniprot(species, uniprot)
    return res

@router.get('/api/tair/')
async def get_Base_Lmpd_By_Tair(species: str, tair: str):
    res=await crud.get_data_by_tair(species, tair)
    return res

@router.get('/api/sample/')
async def get_Sample_Data_By_Species(species: str):
    res=await crud.load_sample_data(species)
    return res

@router.get('/api/fatty_acid_search/')
async def search_Fatty_Acids(query: str):
    res=await crud.fatty_acid_search(query)
    return res

@router.get('/api/homolog/')
async def get_Homologs_For_Uniprot_ID(uniprot_id: str):
    res= await crud.get_homolog_uniprots(uniprot_id)
    return res

@router.get('/api/sequence_search/')
async def search_By_Sequence(species: str, sequence: str):
    res=await crud.sequence_search(species, sequence)
    return res

@router.get('/api/blast/')
async def blast(database: str, sequence: str, parameters: str):
    if database.isalpha() or sequence.isalpha():
        res=await blastp.getResult(database, sequence, parameters)
        return res
    else:
        return {"Error": "Invalid input values"}
   
@router.get('/api/PSI_blast/')
async def PSI_blast(database: str, sequence: str, parameters: str):
    if database.isalpha() or sequence.isalpha():
        res=await blastp.getPSIBlastResult(database, sequence, parameters)
        return res
    else:
        return {"Error": "Invalid input values"}
   
#by Sam, for phase out Firestore
@router.get('/api/species_mapper/')
async def get_species_mapper(speciesName: str, q: str):
    if speciesName != "arabidopsis" and speciesName != "camelina" and speciesName != "glymine_max":
        raise HTTPException(status_code=500, detail="Invalid speciesName")
    if is_sql_injection(speciesName) or is_sql_injection(q):
        raise HTTPException(status_code=500, detail="Invalid input values")
    res=await crud.get_species_mapper(speciesName, q)
    return res

@router.get('/api/customized_pathways/')
async def get_customized_pathways():
    res=await crud.get_customized_pathways()
    return res

@router.get('/api/pathway_areas/')
async def get_pathway_areas(pathway_id: int):
    res=await crud.get_pathway_areas(pathway_id)
    return res

@router.get('/api/pathway_img_path/')
async def get_pathway_img_path(pathway_id: int):
    res=await crud.get_pathway_img_path(pathway_id)
    return res

@router.get('/api/details_uniprotid/')
async def get_Details_By_UNIPROTID(species: str, id: str):
    if species != "soya" and species != "camelina" and species != "lmpd":
        raise HTTPException(status_code=500, detail="Invalid speciesName")
    if is_sql_injection(species) or is_sql_injection(id):
        raise HTTPException(status_code=500, detail="Invalid input values")
    res=await crud.get_details_by_uniprotid(species, id)
    return res

#counting visitors and log their IP address etc.
@router.get('/api/visit/')
async def count_and_log_visitor(info: str):
    if is_sql_injection(info):
        raise HTTPException(status_code=500, detail="Invalid input values")
    res=await crud.count_and_log_visitor(info)
    return res

@router.get('/enzyme_search/')
async def search_Enzyme(query: str):
    res=await crud.enzyme_search(query)
    return res
