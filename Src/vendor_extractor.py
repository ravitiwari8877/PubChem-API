import requests

def fetch_vendors_for_cid(cid):
    """
    Fetches chemical vendor information for a given PubChem Compound ID (CID).

    This function calls the PUG-View Categories API to retrieve the list of
    commercial sources (vendors) that provide the specified compound. Each vendor's
    information includes supplier ID, name, URLs, and registry data.

    API used:
        https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/categories/compound/{cid}/JSON/?heading=Chemical+Vendors

    Args:
        cid (int): The PubChem Compound ID for which vendor information is to be retrieved.

    Returns:
        List[dict]: A list of dictionaries containing vendor details. Each dictionary contains:
            - CID (int): The input compound CID
            - SID (str): Substance ID
            - SourceName (str): Vendor name
            - SourceURL (str): Vendor homepage
            - RegistryID (str): Vendor registry identifier
            - SourceRecordURL (str): Link to the vendor's record for this compound

        Returns an empty list if no vendor data is found or an error occurs.
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/categories/compound/{cid}/JSON/?heading=Chemical+Vendors&response_type=display"
    vendors = []

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        sources = data["SourceCategories"]["Categories"][0]["Sources"]
        for source in sources:
            vendors.append({
                "CID": cid,
                "SID": source.get("SID", ""),
                "SourceName": source.get("SourceName", ""),
                "SourceURL": source.get("SourceURL", ""),
                "RegistryID": source.get("RegistryID", ""),
                "SourceRecordURL": source.get("SourceRecordURL", "")
            })
    except Exception as e:
        print(f"⚠️ Failed to fetch vendors for CID {cid}: {e}")

    return vendors
