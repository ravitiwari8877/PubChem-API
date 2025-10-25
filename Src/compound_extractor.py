import pubchempy as pcp
import requests
import pandas as pd
import logging
from time import sleep
from typing import List, Optional

# ---------------------------
# Setup Logging
# ---------------------------
logging.basicConfig(
    filename="pubchem_extractor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------
# Compound Extractor Class
# ---------------------------
class PubChemCompoundExtractor:
    def __init__(self, query):
        self.query = query
        self.compound = None
        self.data = {}

    def fetch_compound(self):
        compounds = pcp.get_compounds(self.query, namespace='name')
        if not compounds:
            raise ValueError(f"No compound found for '{self.query}'")
        self.compound = compounds[0]
        logging.info(f"Compound found: CID {self.compound.cid}")

    def extract_details(self):
        c = self.compound
        chembl_values = [v for v in c.synonyms if v.startswith('CHEMBL')] if c.synonyms else []
        self.data = {
            'CID': c.cid,
            'Compound Name': self.query,
            'IUPAC Name': c.iupac_name,
            'Molecular Formula': c.molecular_formula,
            'Molecular Weight': c.molecular_weight,
            'Canonical SMILES': c.canonical_smiles,
            'Isomeric SMILES': c.isomeric_smiles,
            'InChI': c.inchi,
            'InChIKey': c.inchikey,
            'XLogP': c.xlogp,
            'TPSA': c.tpsa,
            'Exact Mass': c.exact_mass,
            'Complexity': c.complexity,
            'Rotatable Bonds': c.rotatable_bond_count,
            'H-Bond Donors': c.h_bond_donor_count,
            'H-Bond Acceptors': c.h_bond_acceptor_count,
            'Charge': c.charge,
            'Heavy Atom Count': c.heavy_atom_count,
            'Defined Atom Stereo Count': c.defined_atom_stereo_count,
            'Undefined Atom Stereo Count': c.undefined_atom_stereo_count,
            'Defined Bond Stereo Count': c.defined_bond_stereo_count,
            'Undefined Bond Stereo Count': c.undefined_bond_stereo_count,
            'Covalent Unit Count': c.covalent_unit_count,
            'Coordinate Type': c.coordinate_type,
            'Synonyms': '; '.join(c.synonyms) if c.synonyms else None,
            "ChEMBL ID": chembl_values[0] if chembl_values else None
        }

    def get_data(self):
        return self.data
    
    # def to_dataframe(self):
    #     try:
    #         return pd.DataFrame([self.data])
    #     except Exception as e:
    #         logging.error(f"Error converting to DataFrame: {e}")
    #         raise

    # def save_to_csv(self, df, filename="compound_details.csv"):
    #     try:
    #         df.to_csv(filename, index=False)
    #         logging.info(f"Saved to {filename}")
    #     except Exception as e:
    #         logging.error(f"Error saving to CSV: {e}")
    #         raise

# ---------------------------
# Runner Function
# ---------------------------
# def run_extraction(query):
#     try:
#         extractor = PubChemCompoundExtractor(query)
#         extractor.fetch_compound()
#         extractor.extract_details()
#         df = extractor.to_dataframe()
#         extractor.save_to_csv(df)
#         print(f"✅ Data for '{query}' saved to compound_details.csv")
#         print(df.head())
#     except Exception as e:
#         print(f"❌ Error: {e}")

# ---------------------------
# Entry Point
# ---------------------------
# if __name__ == "__main__":
#     compound_name = "Aspirin"
#     run_extraction(compound_name)