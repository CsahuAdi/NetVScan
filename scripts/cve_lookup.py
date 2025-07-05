import requests

def extract_version(banner: str) -> str:
    """
    Attempt to extract the version string from the banner.
    e.g., 'OpenSSH_7.2p2 Ubuntu' → '7.2'
    """
    import re
    match = re.search(r'(\d+\.\d+(\.\d+)?)', banner)
    if match:
        return match.group(1)
    return ""


def search_cve(service: str, banner: str, max_results=5):
    """
    Search NVD for CVEs matching the service and version (if available).
    """
    version = extract_version(banner)
    query = f"{service} {version}" if version else service
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={query}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        vulns = []
        for item in data.get("vulnerabilities", [])[:max_results]:
            cve_id = item["cve"]["id"]
            desc = item["cve"]["descriptions"][0]["value"]
            vulns.append((cve_id, desc))
        return vulns
    except Exception as e:
        print(f"Error querying NVD: {e}")
        return []
