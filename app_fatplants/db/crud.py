# from sqlalchemy.orm import Session
from typing import List
from db.schemas import *
from db.database import database_conn_obj

# def get_fpids_index(db:Session, species, expression):
#     exp='%{e}%'.format(e=expression)
#     species=species.lower()
#     if species=='lmpd':
#         return db.query(models.Lmpd_Index).filter(models.Lmpd_Index.identifier.like(exp)).all()
#     elif species=='camelina':
#         return db.query(models.Camelina_Index).filter(models.Camelina_Index.identifier.like(exp)).all()
#     elif species=='soya':
#         return db.query(models.Soya_Index).filter(models.Soya_Index.identifier.like(exp)).all()

async def get_fpids_index(species: str, expression: str):
    expression=expression.lower()
    exp='%{e}%'.format(e=expression)
    species=species.lower()
    query1='select fatplant_id from '+species+'_index where identifier like \''+exp+'\';'
    res1= await database_conn_obj.fetch_all(query1)
    res=[i[0] for i in res1]
    row_headers=['identifier','fatplant_id','type']

    return res
async def get_species_records_identifier(species: str,fp_list: List[str]):
    species=species.lower()
    query1 = 'select * from '+species+'_identifier where fatplant_id in ({fpl});'
    fps = ["\"" + fp + "\"" for fp in fp_list]
    fps_list = ",".join(fps)
    query1 = query1.format(fpl=fps_list)
    res1= await database_conn_obj.fetch_all(query1)
    if species=='lmpd':
        row_headers=['fatplants_id','gene_names','protein_name','refseq_id','tair_id','uniprot_id','fp_id']
    elif species=='camelina':
        row_headers=['fatplants_id','cs_id','protein_name','refseq_id','tair_id','uniprot_id','fp_id']
    elif species=='soya':
        row_headers=['fatplants_id','gene_names','protein_name','refseq_id','glyma_id','uniprot_id','fp_id']

    json_data = []
    for result in res1:
        json_data.append(dict(zip(row_headers, result)))

    return json_data

async def get_details_by_fpid(species: str, fp_id: str):
    species=species.lower()
    query='select * from '+species+'_details where fp_id = \''+fp_id+'\';'
    res = await database_conn_obj.fetch_all(query)
    return res

async def get_base_data_by_uniprot(species: str, uniprot_id: str):
    species=species.lower()
    uniprot_id=uniprot_id.upper()
    query='select * from '+species+'_identifier where uniprot_id = \''+uniprot_id+'\';'
    res = await database_conn_obj.fetch_all(query)
    return res

async def get_data_by_tair(species: str, tair: str):
    species=species.lower()
    tair=tair.upper()
    if species == 'lmpd' or species == 'camelina':
        query='select * from '+species+'_identifier where tair_id = \''+tair+'\';'
        res = await database_conn_obj.fetch_all(query)

    else:
        res = []

    return res

async def load_sample_data(species: str):
    species=species.lower()
    if species != 'fatty_acid':
        query='select * from '+species+'_identifier order by fp_id limit 30;'
    else:
        query='select * from fatty_acid order by fp_id limit 30;'
    
    res = await database_conn_obj.fetch_all(query)
    return res

async def get_homolog_uniprots(uniprot_id: str):
    uniprot_id=uniprot_id.upper()
    query='select * from homolog_mapper where uniprot_id = \''+uniprot_id+'\' limit 1;'
    res = await database_conn_obj.fetch_all(query)
    return res

async def sequence_search(species: str, sequence: str):
    species=species.lower()
    sequence=sequence.upper()

    query='select uniprot_id, fp_id from '+species+'_details where sequence=\''+sequence+'\' limit 1;'
    res = await database_conn_obj.fetch_all(query)

# implemented separately from lmpd/camelina/soya
async def fatty_acid_search(query: str):
    query='select * from fatty_acid where SOFAID like \'%'+query+'%\' or delta_notation like \'%'+query+'%\' or Name like \'%'+query+'%\' or other_names like \'%'+query+'%\' or formula like \'%'+query+'%\' limit 30;'
    res = await database_conn_obj.fetch_all(query)
    return res 

#get kegg id from uniprot/fp id using keggid_mapping table
async def get_keggid(species:str, uniprot_id:str):
    query="select * from "+species+"_keggid_mapping where uniprot_id=\'"+uniprot_id+"\';"
    res=await database_conn_obj.fetch_all(query)
    json_data = []
    row_headers=['uniprot_id','fp_id','kegg_id']
    for result in res:
        json_data.append(dict(zip(row_headers, result)))
    return json_data











# def get_species_records_identifier(db:Session,species,expression,fp_list):
#     exp='%{e}%'.format(e=expression)
#     if species=='lmpd':
#         return db.query(models.Lmpd_Identifier).filter(models.Lmpd_Identifier.fatplant_id.in(fp_list)).all()
#     elif species=='camelina':
#         return db.query(models.Camelina_Identifier).filter(models.Camelina_Identifier.fatplant_id.in(fp_list)).all()
#     elif species=='soya':
#         return db.query(models.Soya_Identifier).filter(models.Soya_Identifier.fatplant_id.in(fp_list)).all()
