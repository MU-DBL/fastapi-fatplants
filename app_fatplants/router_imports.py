from species import species
from kegg_pathway import kegg
from chatgpt import chat
from networks import goenrichment
from contact_us import send_email

routers=[
    species,
    kegg,
    chat,
    goenrichment,
    send_email
]