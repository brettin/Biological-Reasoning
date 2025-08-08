import httpx


def chembl_mechanism(compound_name: str, max_results: int = 10) -> str:
    """
    Query ChEMBL API for mechanisms of action related to a compound name.
    Returns a concise list of targets and mechanisms (if any).
    """
    base = "https://www.ebi.ac.uk/chembl/api/data"
    try:
        # Find molecule by name (fuzzy search)
        r = httpx.get(
            f"{base}/molecule.json",
            params={"molecule_synonyms__icontains": compound_name, "limit": max_results},
            timeout=30.0,
        )
        r.raise_for_status()
        mols = r.json().get("molecules", [])
        if not mols:
            return f"ChEMBL: no molecules found for '{compound_name}'."
        chembl_ids = [m.get("molecule_chembl_id") for m in mols if m.get("molecule_chembl_id")]
        if not chembl_ids:
            return f"ChEMBL: no ChEMBL IDs found for '{compound_name}'."

        lines = [f"ChEMBL mechanisms for '{compound_name}':"]
        for mid in chembl_ids:
            mr = httpx.get(
                f"{base}/mechanism.json",
                params={"molecule_chembl_id__exact": mid, "limit": max_results},
                timeout=30.0,
            )
            mr.raise_for_status()
            mechs = mr.json().get("mechanisms", [])
            if not mechs:
                lines.append(f"- {mid}: no mechanisms listed")
                continue
            for mech in mechs[:max_results]:
                target = mech.get("target_chembl_id", "")
                action = mech.get("mechanism_of_action", "")
                refs = mech.get("references", [])
                ref_txt = refs[0].get("ref_url", "") if refs else ""
                lines.append(f"- {mid}: {action} (target {target}) {ref_txt}")

        return "\n".join(lines)
    except Exception as e:
        return f"ChEMBL error: {e}"

