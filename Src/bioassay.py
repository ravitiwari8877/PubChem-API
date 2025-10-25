import requests

def fetch_assay_summary(cid):
    """
    Fetches assay summary data for a given PubChem CID and returns
    a list of dictionaries with selected fields.

    Parameters:
        cid (int): PubChem Compound ID

    Returns:
        list of dicts with keys:
            - AID
            - SID
            - Activity Outcome
            - Assay Type
            - Activity Value [uM]
            - Assay Name
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/assaysummary/JSON"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        columns = data['Table']['Columns']['Column']
        rows = data['Table']['Row']

        # Identify indexes of required columns
        col_indices = {
            'AID': columns.index('AID'),
            'SID': columns.index('SID'),
            'Activity Outcome': columns.index('Activity Outcome'),
            'Assay Type': columns.index('Assay Type'),
            'Activity Value [uM]': columns.index('Activity Value [uM]'),
            'Assay Name': columns.index('Assay Name')
        }

        results = []
        for row in rows:
            cells = row['Cell']
            result = {
                'AID': cells[col_indices['AID']],
                'SID': cells[col_indices['SID']],
                'Activity Outcome': cells[col_indices['Activity Outcome']],
                'Assay Type': cells[col_indices['Assay Type']],
                'Activity Value [uM]': cells[col_indices['Activity Value [uM]']],
                'Assay Name': cells[col_indices['Assay Name']]
            }
            results.append(result)

        return results

    except Exception as e:
        print(f"❌ Error fetching assay summary for CID {cid}: {e}")
        return []

# # Example usage
# if __name__ == "__main__":
#     cid = 2244  # Aspirin
#     assay_data = fetch_assay_summary(cid)
#     for record in assay_data[:3]:  # Print first 3 records
#         print(record)
