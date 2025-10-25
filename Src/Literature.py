import requests

def fetch_literature_summary(cid):
    """
    Fetches PubMed literature summary from PubChem for a given CID.

    Returns the 'AllURL' (general PubMed mesh term link) and all subheading-specific links
    as a structured list. Handles missing fields safely.

    Args:
        cid (int): PubChem Compound ID.

    Returns:
        List[Union[str, dict]]:
            The first element is a string with key "AllURL".
            The rest are dictionaries with:
              - "Heading": Subheading name
              - "URL": Corresponding PubMed search URL
            Returns empty list if no data found.
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/literature/compound/{cid}/JSON"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        literature = data.get("Literature", {})
        all_url = literature.get("AllURL", None)
        subheadings = literature.get("Subheadings", [])

        output = []
        if all_url:
            output.append({"AllURL": all_url})

        for item in subheadings:
            output.append({
                "Heading": item.get("Subheading"),
                "URL": item.get("SubheadingURL")
            })

        return output

    except Exception as e:
        print(f"❌ Error fetching literature summary for CID {cid}: {e}")
        return []
