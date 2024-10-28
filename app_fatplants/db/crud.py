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

#Aralip datas
async def enzyme_search(query: str):
    query='SELECT pathways.path, pathways.id AS path_id, pathways.name AS path_name, enzymes.id , enzymes.name, enzymes.abbreviation, enzymecomments.comments FROM enzymes LEFT JOIN enzymeenzymecomments ON enzymes.id = enzymeenzymecomments.enzyme_id LEFT JOIN enzymecomments ON enzymeenzymecomments.enzymecomment_id = enzymecomments.id JOIN enzymes_pathways ON enzymes.id = enzymes_pathways.enzyme_id LEFT JOIN pathways ON enzymes_pathways.pathway_id = pathways.id where pathways.name like \'%'+query+'%\' or enzymes.name like \'%'+query+'%\' or enzymes.abbreviation like \'%'+query+'%\' or enzymecomments.comments like \'%'+query+'%\';'
    res = await database_conn_obj.fetch_all(query)
    return res 
    
async def enzyme_pathway(id: str):
    query='SELECT name,path,legend,abbreviation,tabLink,tabTitle,GROUP_CONCAT(CONCAT(firstName, " ", lastName) SEPARATOR ", ") AS contributor FROM pathways LEFT JOIN contributors_pathways ON pathways.id = contributors_pathways.pathway_id LEFT JOIN contributors ON contributors_pathways.contributor_id = contributors.id WHERE pathways.id= \''+id+'\' GROUP BY name, path,legend,abbreviation,tabLink,tabTitle;'
    res = await database_conn_obj.fetch_all(query)
    return res 

async def enzyme_search_by_locus(locus_id: int):
    query='select enzyme_id from enzymes_locations where location_id =\''+str(locus_id)+'\';'
    res = await database_conn_obj.fetch_all(query)
    return res 

async def get_location_summary():
    query = """
        SELECT DISTINCT 
            l.id as location_id,
            l.name as location_name,
            e.id AS enzyme_id,
            e.name AS enzyme_name,
            i.abbreviation,
            p.id as pathway_id,
            p.nameabbreviation,
            p.path,
            p.name as pathway_name
        FROM locations l
        JOIN enzymes_locations el ON l.id = el.location_id
        JOIN enzymes e ON e.id = el.enzyme_id
        JOIN enzymes_pathways ep ON e.id = ep.enzyme_id
        JOIN pathways p ON p.id = ep.pathway_id
        LEFT OUTER JOIN locusisoformabbs lia ON lia.location_id = l.id
        LEFT OUTER JOIN isoformabbs i ON i.id = lia.isoformabb_id
    """
    result = await database_conn_obj.fetch_all(query)
    return result

async def get_enzyme_name(enzyme_id: str):
    query='SELECT * FROM enzymes WHERE id = \''+enzyme_id+'\';'
    res = await database_conn_obj.fetch_all(query)
    return res

async def get_enzyme_reactions(enzyme_id: str):
    query='SELECT reactions.id, enzymes_reactions.enzyme_id, reactiontype, enzymetype, hehos.name AS heho_name, hehos.id AS heho_id, s1, s2, p1, p2, comment, domain, enzymes.name AS enzyme_name FROM enzymes_reactions LEFT JOIN reactions ON enzymes_reactions.reaction_id = reactions.id LEFT JOIN hehoenzymes ON enzymes_reactions.enzyme_id = hehoenzymes.enzyme_id LEFT JOIN hehos ON hehoenzymes.heho_id = hehos.id LEFT JOIN reactionreactiontypes ON reactions.id = reactionreactiontypes.reaction_id LEFT JOIN reactiontypes ON reactionreactiontypes.reactiontype_id = reactiontypes.id LEFT JOIN hehodomains ON reactions.id = hehodomains.reaction_id LEFT JOIN enzymes ON enzymes_reactions.enzyme_id = enzymes.id WHERE enzymes_reactions.enzyme_id=\''+enzyme_id+'\';'
    res = await database_conn_obj.fetch_all(query)
    json_data = []
    row_headers=['id','enzyme_id','reactiontype','enzymetype','heho_name','heho_id','s1','s2','p1','p2','comment','domain','enzyme_name','ecnumber']
    for r in res:
        query2="SELECT ecnumber FROM ecnumbers_reactions LEFT JOIN ecnumbers ON ecnumbers.id = ecnumbers_reactions.ecnumber_id WHERE reaction_id=\'"+str(r.id)+"\';"
        res2=await database_conn_obj.fetch_all(query2)
        json_data.append(dict(zip(row_headers,[r.id, r.enzyme_id, r.reactiontype, r.enzymetype, r.heho_name, r.heho_id, r.s1, r.s2, r.p1, r.p2, r.comment, r.domain, r.enzyme_name, res2])))
    return json_data

async def get_enzyme_pathways(enzyme_id: str):
    query='SELECT pathway_id, name, nameabbreviation FROM enzymes_pathways LEFT JOIN pathways ON enzymes_pathways.pathway_id = pathways.id WHERE enzyme_id = \''+enzyme_id+'\';'
    res = await database_conn_obj.fetch_all(query)
    return res

async def get_enzyme_locus(enzyme_id:str):
    query="SELECT locations.id AS location_id, locations.name AS locus_id, isoformabbs.abbreviation AS abbrev, mutants.name AS mutant, gene_identification_method, description_mutant_phenotype, isoformnames.name AS gene, organelles.subcellularlocation AS subcelles, GROUP_CONCAT(evidenceforfunctions.evidenceforfunction SEPARATOR '  ') AS evidence, locuscomments.comments AS comments, brem1, brem2, brem3, brem4, caen1, caen2, caen3, caen4, caem, euen1, euen2, euen3, euen4, euem, naem1, naem2, naem3, naem4 FROM enzymes_locations LEFT JOIN locations ON enzymes_locations.location_id = locations.id LEFT JOIN locusisoformabbs ON locusisoformabbs.location_id = locations.id LEFT JOIN isoformabbs ON isoformabbs.id = locusisoformabbs.isoformabb_id LEFT JOIN mutants ON mutants.location_id = locations.id LEFT JOIN isoformnames_locations ON isoformnames_locations.location_id = locations.id LEFT JOIN isoformnames ON isoformnames.id = isoformnames_locations.isoformname_id LEFT JOIN locusorganelles ON locusorganelles.location_id = locations.id LEFT JOIN organelles ON organelles.id = locusorganelles.organelle_id LEFT JOIN locusevidenceforfunctions ON locusevidenceforfunctions.location_id = locations.id LEFT JOIN evidenceforfunctions ON locusevidenceforfunctions.evidenceforfunction_id = evidenceforfunctions.id LEFT JOIN locationlocuscomments ON locationlocuscomments.location_id = locations.id LEFT JOIN locuscomments ON locuscomments.id = locationlocuscomments.locuscomment_id LEFT JOIN brassicas ON locations.id = brassicas.location_id LEFT JOIN castors ON locations.id = castors.location_id LEFT JOIN euonymus ON locations.id = euonymus.location_id LEFT JOIN nasturtia ON locations.id = nasturtia.location_id WHERE enzymes_locations.enzyme_id = \'"+enzyme_id+"\' GROUP BY location_id, locus_id, abbrev, mutant, gene_identification_method, description_mutant_phenotype, gene, subcelles, comments, brem1, brem2, brem3, brem4, caen1, caen2, caen3, caen4, caem, euen1, euen2, euen3, euen4, euem, naem1, naem2, naem3, naem4;"
    res=await database_conn_obj.fetch_all(query)
    json_data = []
    row_headers=['locus_id','abbrev','mutant', 'gene_identification_method', 'description_mutant_phenotype','gene','subcelles','evidence','comments', 'brem1', 'brem2', 'brem3', 'brem4', 'caen1', 'caen2', 'caen3', 'caen4', 'caem', 'euen1', 'euen2', 'euen3', 'euen4', 'euem', 'naem1', 'naem2', 'naem3', 'naem4','pathways','references']
    for r in res:
        query2="SELECT name, pathway_id, nameabbreviation FROM locations_pathways LEFT JOIN pathways ON locations_pathways.pathway_id = pathways.id WHERE locations_pathways.location_id = \'"+str(r.location_id)+"\';"
        res2=await database_conn_obj.fetch_all(query2)
        query3="SELECT alias, ref FROM locations_refs LEFT JOIN refs ON refs.id = locations_refs.ref_id WHERE locations_refs.location_id = \'"+str(r.location_id)+"\' ORDER BY Sort DESC;"
        res3=await database_conn_obj.fetch_all(query3)
        json_data.append(dict(zip(row_headers, [r.locus_id, r.abbrev, r.mutant, r.gene_identification_method, r.description_mutant_phenotype, r.gene, r.subcelles, r.evidence,r.comments, r.brem1, r.brem2, r.brem3, r.brem4, r.caen1, r.caen2, r.caen3, r.caen4, r.caem, r.euen1, r.euen2, r.euen3, r.euen4, r.euem, r.naem1, r.naem2, r.naem3, r.naem4 ,res2, res3])))
    return json_data

async def get_heho_name(heho_id: str):
    query='SELECT CONCAT(name, " ( ", enzymetype, " )") AS name FROM hehos WHERE id = \''+heho_id+'\';'
    res = await database_conn_obj.fetch_all(query)
    return res

async def get_heho_reactions(heho_id: str):
    query='SELECT reactions.id, s1, s2, p1, p2, enzymes.name AS name, comment FROM hehos LEFT JOIN hehos_reactions ON hehos.id = hehos_reactions.heho_id LEFT JOIN reactions ON hehos_reactions.reaction_id = reactions.id LEFT JOIN reactionreactiontypes ON reactions.id = reactionreactiontypes.reaction_id LEFT JOIN reactiontypes ON reactionreactiontypes.reactiontype_id = reactiontypes.id LEFT JOIN enzymes_reactions ON reactions.id = enzymes_reactions.reaction_id LEFT JOIN enzymes ON enzymes_reactions.enzyme_id = enzymes.id LEFT JOIN hehodomains ON reactions.id = hehodomains.reaction_id LEFT JOIN hehoenzymes ON hehoenzymes.heho_id = hehos_reactions.heho_id WHERE reactiontype_id!=1 AND hehoenzymes.enzyme_id = enzymes.id AND hehos_reactions.heho_id=\''+heho_id+'\';'
    res = await database_conn_obj.fetch_all(query)
    json_data = []
    row_headers=['s1','s2','p1','p2','name','comment','ecnumber']
    for r in res:
        query2="SELECT ecnumber FROM ecnumbers_reactions LEFT JOIN ecnumbers ON ecnumbers.id = ecnumbers_reactions.ecnumber_id WHERE reaction_id=\'"+str(r.id)+"\';"
        res2=await database_conn_obj.fetch_all(query2)
        json_data.append(dict(zip(row_headers,[r.s1, r.s2, r.p1, r.p2, r.name, r.comment, res2])))
    return json_data

async def get_heho_pathways(heho_id: str):
    query='SELECT pathway_id, name, nameabbreviation FROM hehoenzymes LEFT JOIN enzymes_pathways ON enzymes_pathways.enzyme_id = hehoenzymes.enzyme_id LEFT JOIN pathways ON enzymes_pathways.pathway_id = pathways.id WHERE hehoenzymes.heho_id = \''+heho_id+'\' GROUP BY pathway_id, name, nameabbreviation;'
    res = await database_conn_obj.fetch_all(query)
    return res

async def get_heho_locus(heho_id:str):
    query="SELECT locations.id AS location_id, locations.name AS locus_id, isoformabbs.abbreviation AS abbrev, mutants.name AS mutant, gene_identification_method, description_mutant_phenotype, isoformnames.name AS gene, organelles.subcellularlocation AS subcelles, GROUP_CONCAT(evidenceforfunctions.evidenceforfunction SEPARATOR '  ') AS evidence, locuscomments.comments AS comments, brem1, brem2, brem3, brem4, caen1, caen2, caen3, caen4, caem, euen1, euen2, euen3, euen4, euem, naem1, naem2, naem3, naem4 FROM locushehos LEFT JOIN locations ON locushehos.location_id = locations.id LEFT JOIN locusisoformabbs ON locusisoformabbs.location_id = locations.id LEFT JOIN isoformabbs ON isoformabbs.id = locusisoformabbs.isoformabb_id LEFT JOIN mutants ON mutants.location_id = locations.id LEFT JOIN isoformnames_locations ON isoformnames_locations.location_id = locations.id LEFT JOIN isoformnames ON isoformnames.id = isoformnames_locations.isoformname_id LEFT JOIN locusorganelles ON locusorganelles.location_id = locations.id LEFT JOIN organelles ON organelles.id = locusorganelles.organelle_id LEFT JOIN locusevidenceforfunctions ON locusevidenceforfunctions.location_id = locations.id LEFT JOIN evidenceforfunctions ON locusevidenceforfunctions.evidenceforfunction_id = evidenceforfunctions.id LEFT JOIN locationlocuscomments ON locationlocuscomments.location_id = locations.id LEFT JOIN locuscomments ON locuscomments.id = locationlocuscomments.locuscomment_id LEFT JOIN brassicas ON locations.id = brassicas.location_id LEFT JOIN castors ON locations.id = castors.location_id LEFT JOIN euonymus ON locations.id = euonymus.location_id LEFT JOIN nasturtia ON locations.id = nasturtia.location_id WHERE locushehos.heho_id = \'"+heho_id+"\' GROUP BY location_id, locus_id, abbrev, mutant, gene_identification_method, description_mutant_phenotype, gene, subcelles, comments, brem1, brem2, brem3, brem4, caen1, caen2, caen3, caen4, caem, euen1, euen2, euen3, euen4, euem, naem1, naem2, naem3, naem4;"
    res=await database_conn_obj.fetch_all(query)
    json_data = []
    row_headers=['locus_id','abbrev','mutant', 'gene_identification_method', 'description_mutant_phenotype','gene','subcelles','evidence','comments', 'brem1', 'brem2', 'brem3', 'brem4', 'caen1', 'caen2', 'caen3', 'caen4', 'caem', 'euen1', 'euen2', 'euen3', 'euen4', 'euem', 'naem1', 'naem2', 'naem3', 'naem4','pathways','references']
    for r in res:
        query2="SELECT name, pathway_id, nameabbreviation FROM locations_pathways LEFT JOIN pathways ON locations_pathways.pathway_id = pathways.id WHERE locations_pathways.location_id = \'"+str(r.location_id)+"\';"
        res2=await database_conn_obj.fetch_all(query2)
        query3="SELECT alias, ref FROM locations_refs LEFT JOIN refs ON refs.id = locations_refs.ref_id WHERE locations_refs.location_id = \'"+str(r.location_id)+"\' ORDER BY Sort DESC;"
        res3=await database_conn_obj.fetch_all(query3)
        json_data.append(dict(zip(row_headers, [r.locus_id, r.abbrev, r.mutant, r.gene_identification_method, r.description_mutant_phenotype, r.gene, r.subcelles, r.evidence,r.comments, r.brem1, r.brem2, r.brem3, r.brem4, r.caen1, r.caen2, r.caen3, r.caen4, r.caem, r.euen1, r.euen2, r.euen3, r.euen4, r.euem, r.naem1, r.naem2, r.naem3, r.naem4 ,res2, res3])))
    return json_data
