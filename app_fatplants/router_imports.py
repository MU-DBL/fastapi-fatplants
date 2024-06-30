from species import species
from kegg_pathway import kegg
from chatgpt import chat
from contactus import send_email

routers=[
    species,
    kegg,
    chat,
    send_email
]