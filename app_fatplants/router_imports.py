from species import species
from kegg_pathway import kegg
from chatgpt import chat
from networks import goenrichment
from contact_us import send_email
from aralipform import form

routers=[
    species,
    kegg,
    chat,
    goenrichment,
    send_email,
    form
]