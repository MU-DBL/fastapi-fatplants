from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from db import crud

import requests
import xml.etree.ElementTree as ET
import cv2
from PIL import Image
from io import BytesIO


router = APIRouter(
    tags=["kegg_pathway"],
    # dependencies=[Depends(jwt.JWTBearer())],
    responses={404: {"description": "Error in calling kegg pathway API"}},
)

@router.get('/pathways/')
async def get_pathway_ids(species:str, uniprot_id:str):
    mapping_res= await crud.get_keggid(species,uniprot_id)
    if len(mapping_res)<1:
        #return "No Uniprot ID in database table for this species"
        raise HTTPException(status_code=400, detail="No Uniprot ID in database table for this species")
    kegg_ids=[]
    for r in mapping_res:
        if r['kegg_id'] is not None:
            kegg_ids.append(r['kegg_id'])  
        else:
            #return "Null kegg_id is mapped for given uniprot_id"
            raise HTTPException(status_code=400, detail="Null kegg_id is mapped for given uniprot_id")
    if len(kegg_ids)>1:
        #return "More than 1 kegg_ids found for given uniprot id. Give functionality to select specific keggid"
        raise HTTPException(status_code=400, detail="More than 1 kegg_ids found for given uniprot id")

    kegg_id=kegg_ids[0]

    pathway_url=f"http://rest.kegg.jp/link/pathway/{kegg_id}"
    pathway_content = requests.get(pathway_url).text
    #If rest.kegg.jp returns no result, "pathway_content" will only contain a '\n' and cause error. Sam
    if len(pathway_content)<=1:
        raise HTTPException(status_code=400, detail="No pathway found in rest.kegg.jp")
    p=pathway_content.split('\n')[:-1]
    res=[]
    for x in p:
        res.append(x.split('\t')[1])
    output={'pathway_ids':res}
    return output

@router.get('/highlighted_image/')
async def get_highlighted_pathwayimage(pathway_id: str, uniprot_id: str, species:str):
    mapping_res= await crud.get_keggid(species,uniprot_id)
    if len(mapping_res)<1:
        return "No Uniprot ID in database table for this species"
    kegg_ids=[]
    for r in mapping_res:
        if r['kegg_id'] is not None:
            kegg_ids.append(r['kegg_id'])  
        else: 
            return "Null kegg_id is mapped for given uniprot_id"
    if len(kegg_ids)>1:
        return "More than 1 kegg_ids found for given uniprot id. Give functionality to select specific keggid"

    kegg_id=kegg_ids[0]
    # highlight=kegg_id.split(':')[-1]'
    highlight=kegg_id
    print(highlight)
    # highlight='GGPS6'

    kgml_url = f"http://rest.kegg.jp/get/{pathway_id}/kgml"
    kgml_content = requests.get(kgml_url).text
    img_url=f"http://rest.kegg.jp/get/{pathway_id}/image"
    img_content = requests.get(img_url).content

    img1 = Image.open(BytesIO(img_content))
    owidth, oheight = img1.size

    with open(f'/tmp/{pathway_id}.png','wb') as f:
        f.write(img_content)
        f.close()
    # Load the image
    img = cv2.imread(f'/tmp/{pathway_id}.png')
    img=cv2.resize(img, (owidth, oheight))


    root = ET.fromstring(kgml_content)
    tree=ET.ElementTree(root)
    root=tree.getroot()

    for x in root.findall('entry'):
        if x.get('type')=='gene':
            gr=x.find('graphics')
            # names_list=gr.get('name').split(',')
            names_list=x.get('name').split(',')
            ns=names_list[0].split(' ')
            print(ns)
            if highlight in ns:
                print("in if")
                if gr.get('type')=='rectangle':
                    print(" is rectangle")
                    gr.set('bgcolor','#FF0000')
                    xc=int(gr.get('x'))
                    yc=int(gr.get('y'))
                    w=int(gr.get('width'))
                    h=int(gr.get('height'))
                    cv2.rectangle(img, (xc-(w//2), yc-(h//2)), (xc+(w//2) , yc+(h//2) ), (0, 0, 255), 2)
                if gr.get('type')=='line':
                    coords=gr.get('coords').split(',')
                    x1=int(coords[0])
                    y1=int(coords[1])
                    x2=int(coords[2])
                    y2=int(coords[3])
                    cv2.line(img, (x1,y1),(x2,y2),(0,0,255),2)

    tree.write('/tmp/new.xml')
    img2=cv2.resize(img, (owidth, oheight))
    cv2.imwrite(f'/tmp/output_{pathway_id}.png', img2)
    with open(f'/tmp/output_{pathway_id}.png','rb') as r:
        img_byte_result=r.read()
    return Response(content=img_byte_result, media_type="image/png")

@router.get('/getcoordinates/')
async def get_coordinates(pathway_id:str):
    conf_url=f"http://rest.kegg.jp/get/{pathway_id}/conf"
    conf_content=requests.get(conf_url).text
    x=conf_content.replace("\\t", '\t').replace("\\n", '\n')
    # print(x)
    # print(conf_content)
    # u="https://fatplantsmu.ddns.net:5000/getcoordinates/?pathway_id=ath00510"
    # r=requests.get(u).text
    # r2=r.replace("\\t",'\t').replace("\\n",'\n')
    # with open("new.txt",'w') as f:
    #     f.write(r2)
    return x







