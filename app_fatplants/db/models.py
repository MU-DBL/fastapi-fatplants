# from sqlalchemy import Column, String

# from .database import Base


# class Lmpd_Index(Base):
#     __tablename__ = "lmpd_index"

#     identifier=Column(String)
#     fatplant_id=Column(String)
#     type=Column(String)

# class Camelina_Index(Base):
#     __tablename__ = "camelina_index"

#     identifier=Column(String)
#     fatplant_id=Column(String)
#     type=Column(String)

# class Soya_Index(Base):
#     __tablename__ = "soya_index"

#     identifier=Column(String)
#     fatplant_id=Column(String)
#     type=Column(String)


# class Lmpd_Identifier(Base):
#     __tablename__ = "lmpd_identifier"

#     fatplant_id=Column(String)
#     gene_names=Column(String)
#     protein_name=Column(String)
#     refseq_id=Column(String)
#     tair_id=Column(String)
#     uniprot_id=Column(String)

# class Camelina_Identifier(Base):
#     __tablename__ = "camelina_identifier"

#     fatplant_id=Column(String)
#     cs_id=Column(String)
#     protein_name=Column(String)
#     refseq_id=Column(String)
#     tair_id=Column(String)
#     uniprot_id=Column(String)

# class Soya_Identifier(Base):
#     __tablename__ = "soya_identifier"

#     fatplant_id=Column(String)
#     gene_names=Column(String)
#     protein_name=Column(String)
#     refseq_id=Column(String)
#     glyma_id=Column(String)
#     uniprot_id=Column(String)