import requests

def fetch_depositor_patent_list(cid):
    """
    Fetches depositor-supplied patent IDs from PubChem for a given Compound ID (CID).

    This function uses the PUG-REST API endpoint:
    https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/xrefs/PatentID/TXT

    The response is a plain-text list of patent identifiers (one per line),
    representing patents submitted by data depositors.

    Args:
        cid (int): The PubChem Compound ID for which to fetch patent references.

    Returns:
        List[str]: A list of patent ID strings, e.g., ['AU-2017374860-A1', 'AU-2017374860-B2', ...].
                   Returns an empty list if none found or on error.
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/xrefs/PatentID/TXT"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Return plain list of patent IDs
        return response.text.strip().splitlines()

    except Exception as e:
        print(f"❌ Error fetching patents for CID {cid}: {e}")
        return []

# # Example usage
# if __name__ == "__main__":
#     cid = 134611040
#     patent_list = fetch_depositor_patent_list(cid)
#     print(patent_list)
