import httpx


def pubchem_summary(compound: str) -> str:
    """
    Fetch a basic summary for a compound from PubChem using the PUG REST API.
    Accepts names or CIDs. Returns selected properties relevant to toxicity context.
    """
    base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    # Try compound name to CID
    try:
        r = httpx.get(f"{base}/compound/name/{compound}/cids/JSON", timeout=20.0)
        r.raise_for_status()
        cids = r.json().get("IdentifierList", {}).get("CID", [])
        if not cids:
            return f"PubChem: no CID found for '{compound}'."
        cid = cids[0]
    except Exception as e:
        return f"PubChem error resolving CID: {e}"

    # Properties
    props = [
        "MolecularFormula",
        "MolecularWeight",
        "IUPACName",
        "XLogP",
        "HBondDonorCount",
        "HBondAcceptorCount",
        "TPSA",
        "RotatableBondCount",
    ]
    try:
        r = httpx.get(
            f"{base}/compound/cid/{cid}/property/{','.join(props)}/JSON",
            timeout=20.0,
        )
        r.raise_for_status()
        rec = r.json().get("PropertyTable", {}).get("Properties", [{}])[0]
    except Exception as e:
        return f"PubChem error fetching properties for CID {cid}: {e}"

    lines = [f"PubChem summary for '{compound}' (CID {cid}):"]
    for p in props:
        if p in rec:
            lines.append(f"- {p}: {rec[p]}")
    return "\n".join(lines)

