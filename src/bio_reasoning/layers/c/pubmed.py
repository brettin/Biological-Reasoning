from typing import List, Dict
import urllib.parse
import httpx


def pubmed_search_toxicity(query: str, max_results: int = 10, email: str | None = None) -> str:
    """
    Search PubMed for toxicity-related articles for a given query (e.g., molecule name)
    and return a compact JSON-like string of top results (pmid, title, abstract snippet).

    Args:
        query: Free-text query, typically a chemical name or identifier.
        max_results: Maximum number of records to return.
        email: Optional email to include for NCBI E-utilities policies.

    Returns:
        str: A human-readable string summarizing top hits.
    """
    term = f"({query}) AND (toxicity[Title/Abstract] OR toxic[Title/Abstract])"
    params = {
        "db": "pubmed",
        "retmode": "json",
        "retmax": str(max_results),
        "term": term,
    }
    if email:
        params["email"] = email

    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esummary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    with httpx.Client(timeout=30.0) as client:
        # ESearch to get PMIDs
        r = client.get(esearch_url, params=params)
        r.raise_for_status()
        data = r.json()
        idlist: List[str] = data.get("esearchresult", {}).get("idlist", [])
        if not idlist:
            return "PubMed: no toxicity-related results found."

        ids = ",".join(idlist)

        # ESummary to get titles
        s_params = {"db": "pubmed", "retmode": "json", "id": ids}
        if email:
            s_params["email"] = email
        s = client.get(esummary_url, params=s_params)
        s.raise_for_status()
        summaries = s.json().get("result", {})

        # EFetch to get abstracts (XML returned; request text to simplify)
        f_params = {"db": "pubmed", "id": ids, "retmode": "text", "rettype": "abstract"}
        if email:
            f_params["email"] = email
        f = client.get(efetch_url, params=f_params)
        f.raise_for_status()
        abstracts_text = f.text

    lines: List[str] = ["PubMed toxicity search results:"]
    for pmid in idlist:
        rec = summaries.get(pmid, {})
        title = rec.get("title", "")
        journal = rec.get("fulljournalname", rec.get("source", ""))
        pubdate = rec.get("pubdate", "")
        lines.append(f"- PMID {pmid}: {title} ({journal}, {pubdate})")
    lines.append("\nAbstracts (truncated):")
    # Truncate combined abstracts for brevity
    snippet = abstracts_text.strip()
    if len(snippet) > 2000:
        snippet = snippet[:2000] + "..."
    lines.append(snippet)
    return "\n".join(lines)

