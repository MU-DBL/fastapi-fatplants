from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
import csv

router = APIRouter(
    tags=["networks"],
    responses={404: {"description": "Error in calling networks API"}},
)

csv_entity_table_file_path = '/app/fatplants_volume/fileCyt/GO_AllLists.csv'
csv_file_path1 = '/app/fatplants_volume/fileCyt/network.csv'

@router.get("/api/godata")
async def godata(request: Request):
    identifier = request.query_params.get('identifier')
    ifsearch = identifier is not None
    node_array = []
    node_id_count = {}

    # Read the csv entity table file
    with open(csv_entity_table_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            node_id_count[row[0]] = {
                'hitCount': int(row[1]),
                'groupId': row[2]
            }
            if identifier and identifier in row:
                node_array.append(row[0])

    elements = []
    genes = []
    group_num = 1

    # Read the csv file
    with open(csv_file_path1, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if group_num > 11:
                group_num = 1

            if ifsearch:
                node1 = row['Gene_A']
                node2 = row['Gene_B']
                if not node1 or not node2:
                    continue
                if node1 not in node_array and node2 not in node_array:
                    continue

            # Process Gene_A
            if row['Gene_A'] not in genes:
                genes.append(row['Gene_A'])
                data = {
                    "id": row['Gene_A'],
                    "name": row['Gene_A'],
                    "score": 0,
                    "gene": True,
                    "hitCount": node_id_count[row['Gene_A']]['hitCount'],
                    "groupId": node_id_count[row['Gene_A']]['groupId']
                }
                node_model = {"data": data, "group": "nodes"}
                elements.append(node_model)

            # Process Gene_B
            if row['Gene_B'] not in genes:
                genes.append(row['Gene_B'])
                data = {
                    "id": row['Gene_B'],
                    "name": row['Gene_B'],
                    "score": 0,
                    "gene": True,
                    "hitCount": node_id_count[row['Gene_B']]['hitCount'],
                    "groupId": node_id_count[row['Gene_B']]['groupId']
                }
                node_model = {"data": data, "group": "nodes"}
                elements.append(node_model)

            # Update scores for nodes
            for element in elements:
                if element["group"] == "nodes" and element["data"]["name"] in [row['Gene_A'], row['Gene_B']]:
                    element["data"]["score"] += 0.0004

            # Process edge
            data = {
                "source": row['Gene_A'],
                "target": row['Gene_B'],
                "weight": float(row['SCORE']) / 1.2,
                "group": str(group_num)
            }
            node_model = {"data": data, "group": "edges"}
            elements.append(node_model)

            group_num += 1

    return JSONResponse(content=elements)