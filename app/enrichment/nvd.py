from app.config import NVD_API_KEY
from app.enrichment.base_client import APIClient


NVD_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"

nvd_client = APIClient(
    base_url=NVD_BASE,
    headers={"apiKey": NVD_API_KEY} if NVD_API_KEY else {}
)


async def enrich_cve(cve_id: str):
    return await nvd_client.get("", params={"cveId": cve_id})
