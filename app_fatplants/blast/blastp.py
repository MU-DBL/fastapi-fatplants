import subprocess
from datetime import datetime
import os

def getDatabasePath(database: str):
    soybean_path = "/app/fatplants_volume/blast_db/soybean.fasta"
    arabidopsis_path = "/app/fatplants_volume/blast_db/arabidopsis.fasta"
    camelina_path = "/app/fatplants_volume/blast_db/camelina.fasta"
    if database:
        switcher = {
            "soybean": soybean_path,
            "arabidopsis": arabidopsis_path,
            "camelina": camelina_path
        }
        return switcher.get(database, arabidopsis_path)
    else:
        return 'Error: database is null'
    
async def getPSIBlastResult(database: str, sequence: str, parameters: str):
    file_path = '/app/'

    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    input_file = f"{file_path}input_{time_str}.faa"
    output_file = f"{file_path}output_{time_str}.txt"

    with open(input_file, 'w') as file:
        file.write(sequence)

    result = "";

    try:
        database_path = getDatabasePath(database)
        command_line = f"psiblast -query {input_file} -db {database_path} -out {output_file} -evalue 0.001 -num_iterations 3 {parameters}"
        print(command_line)
        subprocess.check_output(command_line, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        with open(output_file, 'r') as file:
            result = file.read()

        os.remove(input_file)
        os.remove(output_file)   
        return result   
    except subprocess.CalledProcessError as e:
        os.remove(input_file)
        os.remove(output_file)
        return f'Error: {e.output}', 500

async def getResult(database: str, sequence: str, parameters: str):
    file_path = '/app/'

    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    input_file = f"{file_path}input_{time_str}.faa"
    output_file = f"{file_path}output_{time_str}.txt"

    with open(input_file, 'w') as file:
        file.write(sequence)

    result = "";

    try:
        database_path = getDatabasePath(database)
        command_line = f"blastp -query {input_file} -db {database_path} -out {output_file} {parameters}"
        # print(command_line)
        subprocess.check_output(command_line, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        with open(output_file, 'r') as file:
            result = file.read()

        os.remove(input_file)
        os.remove(output_file)   
        return result   
    except subprocess.CalledProcessError as e:
        os.remove(input_file)
        os.remove(output_file)
        return f'Error: {e.output}', 500
    
