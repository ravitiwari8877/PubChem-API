import requests

def fetch_pdb_for_cid(cid):
    """
    Fetches Protein Bound 3D Structure information for a given PubChem Compound ID (CID).

    This function queries the PubChem PUG-View API to retrieve a list of PDB structures
    associated with the compound, such as cryo-EM or X-ray crystal structures. Each entry
    includes identifiers, descriptions, taxonomy information, and relevant URLs.

    API used:
        https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/structure/compound/{cid}/JSON

    Args:
        cid (int): The PubChem Compound ID for which protein structure data is to be retrieved.

    Returns:
        List[dict]: A list of dictionaries. Each dictionary contains:
            - PDB_ID (str): Protein Data Bank identifier
            - MMDB_ID (int): NCBI MMDB identifier
            - Description (str): Description of the protein-compound complex
            - Taxonomy_Name (str): Organism name (e.g., "Homo sapiens")
            - URL (str): NCBI URL to the structure entry

        Returns an empty list if no structures are found or if an error occurs.
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/structure/compound/{cid}/JSON"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        structures = data.get("Structure", {}).get("Structures", [])
        result = []

        for entry in structures:
            result.append({
                "PDB_ID": entry.get("PDB_ID"),
                "MMDB_ID": entry.get("MMDB_ID"),
                "Description": entry.get("Description"),
                "Taxonomy_Name": entry.get("Taxonomy", {}).get("Name"),
                "URL": entry.get("URL")
            })
        return result

    except Exception as e:
        print(f"❌ Error retrieving protein structures for CID {cid}: {e}")
        return []
