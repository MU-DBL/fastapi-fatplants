from species import species
from kegg_pathway import kegg
from chatgpt import chat
from networks import goenrichment

routers=[
    species,
    kegg,
    chat,
    goenrichment
]