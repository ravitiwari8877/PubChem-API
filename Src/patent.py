import requests

def fetch_patents_for_cid(cid):
    """
    Fetches patents for a given PubChem CID using the PUG-View API.
    
    Parameters:
        cid (int): PubChem Compound ID
        
    Returns:
        list of dicts: Each dict contains 'Patent' and 'URL' keys.
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/?heading=Patents"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        sections = data.get("Record", {}).get("Section", [])

        for section in sections:
            if section.get("TOCHeading") == "Patents":
                result = []
                for info in section.get("Information", []):
                    for item in info.get("Value", {}).get("StringWithMarkup", []):
                        patent = item.get("String")
                        url = item.get("Markup", [{}])[0].get("URL", "")
                        if patent and url:
                            result.append({"Patent": patent, "URL": url})
                return result

        return []

    except Exception as e:
        print(f"❌ Error fetching patents for CID {cid}: {e}")
        return []

# # Example usage
if __name__ == "__main__":
    cid = 134611040  # Aspirin
    patents = fetch_patents_for_cid(cid)
    for entry in patents:
        print(entry)
