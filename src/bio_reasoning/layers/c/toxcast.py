import httpx


def toxcast_endpoints(compound: str, max_results: int = 20) -> str:
    """
    Query EPA CompTox Chemicals Dashboard (CTS) for assay endpoints (approximation).
    Note: Public APIs are limited; this function tries the CTS search and reports identifiers
    and links for manual follow-up. In production, integrate official ToxCast/Tox21 APIs/dumps.
    """
    try:
        # Search CTS for the chemical to get DTXSID or DTXCID
        r = httpx.get(
            "https://comptox.epa.gov/dashboard/api/search",
            params={"search": compound},
            timeout=30.0,
        )
        r.raise_for_status()
        results = r.json()
        if not results:
            return f"CompTox: no results for '{compound}'."
        lines = [f"CompTox identifiers for '{compound}':"]
        for rec in results[:max_results]:
            name = rec.get("preferredName") or rec.get("chemicalName") or ""
            dtxsid = rec.get("dtxsid", "")
            dtxcid = rec.get("dtxcid", "")
            url = f"https://comptox.epa.gov/dashboard/chemical/properties/{dtxsid or dtxcid}"
            lines.append(f"- {name} DTXSID={dtxsid} DTXCID={dtxcid} {url}")
        lines.append(
            "Note: For detailed ToxCast/Tox21 assay data, download data tables or use EPA APIs where available."
        )
        return "\n".join(lines)
    except Exception as e:
        return f"CompTox error: {e}"

