# from sqlalchemy.orm import Session
from typing import List
from db.schemas import *
from db.database import database_conn_obj
from datetime import datetime
import os

# def get_fpids_index(db:Session, species, expression):
#     exp='%{e}%'.format(e=expression)
#     species=species.lower()
#     if species=='lmpd':
#         return db.query(models.Lmpd_Index).filter(models.Lmpd_Index.identifier.like(exp)).all()
#     elif species=='camelina':
#         return db.query(models.Camelina_Index).filter(models.Camelina_Index.identifier.like(exp)).all()
#     elif species=='soya':
#         return db.query(models.Soya_Index).filter(models.Soya_Index.identifier.like(exp)).all()

async def get_species_details_records(species: str, expression: str):
    species=species.lower()
    exp = f'%{expression}%'
    query1 = 'select fp_id, description, is_longest, sequence from '+species+'_details where description like :exp;'
    res1= await database_conn_obj.fetch_all(query1, values={"exp": exp})

    row_headers=['fp_id','description','is_longest','sequence']

    json_data = []
    for result in res1:
        json_data.append(dict(zip(row_headers, result)))

    return json_data

async def get_fpids_index(species: str, expression: str):
    expression=expression.lower()
    exp = f'%{expression}%'
    species = f'{species.lower()}_index'
    query1 = f'select fatplant_id from {species} where identifier like :exp;'
    res1= await database_conn_obj.fetch_all(query1, values={"exp": exp})
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
    if species=='cuphea' or species=='pennycress':
        query='select * from '+species+'_details order by fp_id limit 30;'
    
    elif species=='lmpd' or species=='camelina'or species=='soya':
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
    query='select * from fatty_acid where SOFAID like \'%'+query+'%\' or delta_notation like \'%'+query+'%\' or Name like \'%'+query+'%\' or other_names like \'%'+query+'%\' or formula like \'%'+query+'%\';'
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

#by Sam, for phase out Firestore
async def get_species_mapper(speciesName: str, q: str):
    speciesName=speciesName.lower()
    q=q.upper()
    query='select * from species_mapper where '+speciesName+' = \''+q+'\';'
    res = await database_conn_obj.fetch_all(query)
    return res

async def get_customized_pathways():
    query='SELECT * FROM customized_pathways;'
    res = await database_conn_obj.fetch_all(query)
    return res

async def get_pathway_areas(pathway_id: int):
    query='SELECT * FROM pathway_areas WHERE pathway_id = '+str(pathway_id)+';'
    res = await database_conn_obj.fetch_all(query)
    return res

async def get_pathway_img_path(pathway_id: int):
    query='SELECT img_path FROM customized_pathways WHERE pathway_id = '+str(pathway_id)+';'
    res = await database_conn_obj.fetch_all(query)
    return res

async def get_details_by_uniprotid(species: str, uniprot_id: str):
    species=species.lower()
    query='select * from '+species+'_details where uniprot_id = \''+uniprot_id+'\';'
    res = await database_conn_obj.fetch_all(query)
    return res

#for logging IP and counting visitors
async def count_and_log_visitor(info: str):
    query='SELECT count FROM visitor WHERE id = 0;'
    res = await database_conn_obj.fetch_all(query)
    result=str(res[0][0]+1)
    query2='UPDATE visitor SET count = \''+result+'\' WHERE id = \'0\';'
    await database_conn_obj.execute(query2)

    year_month_str = f"{datetime.now().month:02d}{datetime.now().year % 100:02d}"
    with open('fatplants_volume//counter_log//record_'+os.getenv('APP_ENV')+'_'+year_month_str+'.txt', 'a') as file:
        file.write(result+' '+info + '\n')
    
    return result

async def submit_record(record: ArabidopsisRecord):
    subcellular_location = record.subcellular_location_listed or record.subcellular_location_filled
    evidence_for_function = record.evidence_for_function_listed or record.evidence_for_function_filled

    query = """
    INSERT INTO ArabidopsisFormRecords (
        submitter_name, submitter_affiliation, submitter_email_address,
        record_type, record_url, figure_url, pathway,
        protein_family_name_common, protein_family_abbreviation_common,
        isoform_gene_name, isoform_gene_abbreviation, gene_locus, ec_number,
        subcellular_location, mutant_name, evidence_for_function,
        specific_comments_on_locus, other_comments,
        reference_1, pubmed_link_1, reference_2, pubmed_link_2,
        reference_3, pubmed_link_3
    )  VALUES (
        :submitter_name, :submitter_affiliation, :submitter_email_address,
        :record_type, :record_url, :figure_url, :pathway,
        :protein_family_name_common, :protein_family_abbreviation_common,
        :isoform_gene_name, :isoform_gene_abbreviation, :gene_locus, :ec_number,
        :subcellular_location, :mutant_name, :evidence_for_function,
        :specific_comments_on_locus, :other_comments,
        :reference_1, :pubmed_link_1, :reference_2, :pubmed_link_2,
        :reference_3, :pubmed_link_3
    )
    """

    values = {
        "submitter_name": record.name,
        "submitter_affiliation": record.affiliation,
        "submitter_email_address": record.email_address,
        "record_type": record.record_type,
        "record_url": record.record_url,
        "figure_url": record.figure_url,
        "pathway": record.pathway,
        "protein_family_name_common": record.protein_family_name_common,
        "protein_family_abbreviation_common": record.protein_family_abbreviation_common,
        "isoform_gene_name": record.isoform_gene_name,
        "isoform_gene_abbreviation": record.isoform_gene_abbreviation,
        "gene_locus": record.gene_locus,
        "ec_number": record.ec_number,
        "subcellular_location": subcellular_location,
        "mutant_name": record.mutant_name,
        "evidence_for_function": evidence_for_function,
        "specific_comments_on_locus": record.specific_comments_on_locus,
        "other_comments": record.other_comments,
        "reference_1": record.reference_1,
        "pubmed_link_1": record.pubmed_link_1,
        "reference_2": record.reference_2,
        "pubmed_link_2": record.pubmed_link_2,
        "reference_3": record.reference_3,
        "pubmed_link_3": record.pubmed_link_3
    }
    
    await database_conn_obj.execute(query=query, values=values)

async def fetch_records():
    query = "SELECT * FROM ArabidopsisFormRecords"
    records = await database_conn_obj.fetch_all(query)
    
    return records


# def get_species_records_identifier(db:Session,species,expression,fp_list):
#     exp='%{e}%'.format(e=expression)
#     if species=='lmpd':
#         return db.query(models.Lmpd_Identifier).filter(models.Lmpd_Identifier.fatplant_id.in(fp_list)).all()
#     elif species=='camelina':
#         return db.query(models.Camelina_Identifier).filter(models.Camelina_Identifier.fatplant_id.in(fp_list)).all()
#     elif species=='soya':
#         return db.query(models.Soya_Identifier).filter(models.Soya_Identifier.fatplant_id.in(fp_list)).all()
