from pydantic import BaseModel
from typing import Optional

class lmpd_index(BaseModel):
    identifier:str
    fatplant_id:str
    type:str

    # class Config:
    #     orm_mode = True

class camelina_index(BaseModel):
    identifier:str
    fatplant_id:str
    type:str

    # class Config:
    #     orm_mode = True

class soya_index(BaseModel):
    identifier:str
    fatplant_id:str
    type:str

    # class Config:
    #     orm_mode = True

class lmpd_identifier(BaseModel):
    fatplant_id:str
    gene_names:str
    protein_name:str
    refseq_id:str
    tair_id:str
    uniprot_id:str

    # class Config:
    #     orm_mode = True

class camelina_identifier(BaseModel):
    fatplant_id:str
    cs_id:str
    protein_name:str
    refseq_id:str
    tair_id:str
    uniprot_id:str

    # class Config:
    #     orm_mode = True

class soya_identifier(BaseModel):
    fatplant_id:str
    gene_names:str
    protein_name:str
    refseq_id:str
    glyma_id:str
    uniprot_id:str

    # class Config:
    #     orm_mode = True

class ArabidopsisRecord(BaseModel):
    name: str
    affiliation: str
    email_address: str
    record_type: str
    record_url: Optional[str] = None
    figure_url: Optional[str] = None
    pathway: Optional[str] = None
    protein_family_name_common: Optional[str] = None
    protein_family_abbreviation_common: Optional[str] = None
    isoform_gene_name: Optional[str] = None
    isoform_gene_abbreviation: Optional[str] = None
    gene_locus: Optional[str] = None
    ec_number: Optional[str] = None
    subcellular_location_listed: Optional[str] = None
    subcellular_location_filled: Optional[str] = None
    mutant_name: Optional[str] = None
    evidence_for_function_listed: Optional[str] = None
    evidence_for_function_filled: Optional[str] = None
    specific_comments_on_locus: Optional[str] = None
    other_comments: Optional[str] = None
    reference_1: Optional[str] = None
    pubmed_link_1: Optional[str] = None
    reference_2: Optional[str] = None
    pubmed_link_2: Optional[str] = None
    reference_3: Optional[str] = None
    pubmed_link_3: Optional[str] = None