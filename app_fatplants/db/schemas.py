from pydantic import BaseModel

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
