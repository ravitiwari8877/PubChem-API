from compound_extractor import PubChemCompoundExtractor
from vendor_extractor import fetch_vendors_for_cid
from pdb import fetch_pdb_for_cid
from bioassay import fetch_assay_summary
from patent import fetch_patents_for_cid
from Depositor_Supply_Patent import fetch_depositor_patent_list
from Literature import fetch_literature_summary
import pandas as pd
import os
import json

def main(compound_name):
    try:
        print(f"🔍 Extracting compound data for '{compound_name}'")
        extractor = PubChemCompoundExtractor(compound_name)
        extractor.fetch_compound()
        extractor.extract_details()
        compound_data = extractor.get_data()
        cid = compound_data.get('CID')

        print(f"🔍 Extracting vendor data for CID {cid}")
        vendors = fetch_vendors_for_cid(cid)
        
        print(f"🔍 Extracting PDB data for CID {cid}")
        pdb = fetch_pdb_for_cid(cid)
        
        print(f"🔍 Extracting BioAssay data for CID {cid}")
        assay = fetch_assay_summary(cid)
        
        print(f"🔍 Extracting Patent data for CID {cid}")
        patent = fetch_patents_for_cid(cid)
        
        print(f"🔍 Extracting Depositor-supplied patent data for CID {cid}")
        depositor_patent = fetch_depositor_patent_list(cid)
        
        print(f"🔍 Extracting Literature Summary data for CID {cid}")
        literature = fetch_literature_summary(cid)

        # Extract unique SourceName values and join
        vendor_names = sorted({v['SourceName'] for v in vendors if v.get('SourceName')})
        compound_data["Chemical Vendors"] = "; ".join(vendor_names) if vendor_names else None
        compound_data["Protein 3D Structures"] = json.dumps(pdb, indent=2)
        compound_data["BioAssay"] = json.dumps(assay[:8], indent=2)
        compound_data["Patent"] = json.dumps(patent, indent=2)
        compound_data["Depositor-Supplied Patent"] = depositor_patent
        compound_data["Literature"] = json.dumps(literature, indent=2)

        # Create DataFrame
        compound_df = pd.DataFrame([compound_data])

        # Ensure Output directory exists
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'Output')
        os.makedirs(output_dir, exist_ok=True)

        # Save the compound data
        output_path = os.path.join(output_dir, f'{cid}compound_details.csv')
        compound_df.to_csv(output_path, index=False)

        print(f"✅ Compound data saved to: {output_path}")
        print(compound_df.head())
        return compound_df

    except Exception as e:
        print(f"❌ Error in main workflow: {e}")
        return None

if __name__ == "__main__":
    compound = "Aspirin"
    main(compound)
