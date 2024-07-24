# BLAST API Reference
This document outlines the available APIs within the blast module for performing sequence analysis using BLAST tools.

## APIs

### 1. Get PSI-BLAST Result
- Path: /api/psiblast
- Method: POST
- Input Parameters:
   - `database` (string): The target database for the BLAST search.
   - `sequence` (string): The amino acid sequence for the BLAST search.
   - `parameters` (string): Additional command-line parameters for the PSI-BLAST execution.
- Description: Executes a PSI-BLAST search against a specified database using provided sequence and parameters. Returns the search results or an error message.

### 2. Get BLASTP Result
- Path: /api/blastp
- Method: POST
- Input Parameters:
   - `database` (string): The target database for the BLAST search.
   - `sequence` (string): The amino acid sequence for the BLAST search.
   - `parameters` (string): Additional command-line parameters for the BLASTP execution.
- Description: Performs a BLASTP search against a specified database using provided sequence and parameters. Returns the search results or an error message.
<br/><br/>

# ChatGPT API reference
This document provides details for the API within the chatgpt module that facilitates interactions with the OpenAI GPT models.

## APIs
### 1. Get GPT Chat Completion
- Path: /chatgpt/
- Method: GET
- Input Parameters:
   - `content` (string): The input text to send to the GPT model.
   - `role` (string, optional, default="user"): The role of the message sender.   
    This influences how the model interprets the input.
- Description: This endpoint generates responses from the GPT model based on the provided text. It utilizes OpenAI's GPT-3.5 Turbo model to generate conversational completions.
- Tags: kegg_pathway
<br></br>

# Database CRUD API Reference
This document details the APIs provided in the crud module for interacting with database records related to various biological species and their genetic data.

## APIs
### 1. Get Species Details Records
- Path: /species/details
- Method: GET
- Input Parameters:
   - `species`: (string)
   - `expression`: (string)
- Description: Fetches detailed records from the species-specific tables based on a description search pattern.
### 2. Get Identifiers Index
- Path: /species/index
- Method: GET
- Input Parameters:
   - `species` (string)
   - `expression` (string)
- Description: Retrieves identifiers from the species index tables based on a provided search pattern.
### 3. Get Records by Identifier
- Path: /species/identifiers
- Method: GET
- Input Parameters:
   - `species` (string)
   - `fp_list` (list of strings): List of fatplant IDs.
- Description: Fetches records from species-specific identifier tables using a list of fatplant IDs.
### 4. Get Details by FatPlant ID
- Path: /details/by_fpid
- Method: GET
- Input Parameters:
   - `species` (string)
   - `fp_id` (string)
- Description: Retrieves details for a specific fatplant ID from species-specific details tables.
### 5. Get Base Data by UniProt ID
- Path: /base_data/uniprot
- Method: GET
- Input Parameters:
   - `species` (string)
   - `uniprot_id` (string)
- Description: Fetches base genetic data by UniProt ID from species-specific identifier tables.
### 6. Sequence Search
- Path: /sequence/search
- Method: GET
- Input Parameters:
   - `species` (string)
   - `sequence` (string)
- Description: Searches for sequences in species-specific details tables.
### 7. Fatty Acid Search
- Path: /fatty_acid/search
- Method: GET
- Input Parameters:
    - `query` (string)
- Description: Performs a search for fatty acids based on a query string.
### 8. Get KEGG ID by UniProt/FatPlant ID
- Path: /keggid
- Method: GET
- Input Parameters:
    - `species` (string)
    - `uniprot_id` (string)
- Description: Retrieves KEGG ID mapping based on UniProt ID.
### 9. Customized Pathways
- Path: /pathways/customized
- Method: GET
- Description: Retrieves customized pathway data from the database.
### 10. Pathway Areas
- Path: /pathways/areas
- Method: GET
- Input Parameters:
    - `pathway_id` (int)
- Description: Fetches pathway area details for a given pathway ID.
### 11. Get Pathway Image Path
- Path: /pathways/img_path
- Method: GET
- Input Parameters:
    - `pathway_id` (int)
- Description: Retrieves the image path for a specified pathway from the database.
<br></br>


# KEGG Pathway API Reference
This document details the APIs provided in the kegg.py module for interacting with the KEGG (Kyoto Encyclopedia of Genes and Genomes) pathway database.

## APIs
### 1. Get Pathway IDs
- Path: /pathways/
- Method: GET
- Input Parameters:
    - `species` (string)
    - `uniprot_id` (string)
- Description: Retrieves KEGG pathway IDs related to a given UniProt ID within a specified species. It checks for mappings in the database and returns the relevant pathway IDs.
### 2. Get Highlighted Pathway Image
- Path: /highlighted_image/
- Method: GET
- Input Parameters:
    - `pathway_id` (string)
    - `uniprot_id` (string)
    - `species` (string)
- Description: Generates and returns a highlighted image of a specific pathway. It identifies genes related to the given UniProt ID, highlights them in the pathway image, and returns the modified image as a PNG file.
### 3. Get Coordinates
- Path: /getcoordinates/
- Method: GET
- Input Parameters:
    - `pathway_id` (string)
- Description: Fetches coordinates for elements within a specified KEGG pathway. This API could be used to understand the layout or annotations within a pathway map.
<br></br>

# Gene Ontology Enrichment API Reference
This document details the API provided in the goenrichment.py module for handling network data interactions based on Gene Ontology (GO) information.

## APIs
### 1. Get Gene Ontology Data
- Path: /godata
- Method: GET
- Input Parameters:
    - `identifier` (string, optional): A query parameter that filters the network data based on specific identifiers.
- Description: Retrieves and processes Gene Ontology network data from CSV files, constructing a JSON response that includes nodes and edges representing gene interactions. This response is used to visualize networks in a web application.