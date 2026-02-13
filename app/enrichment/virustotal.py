import os
import httpx
from dotenv import load_dotenv

load_dotenv()  # This loads .env file

VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

headers = {
    "x-apikey": VT_API_KEY
}

vt_client = httpx.AsyncClient(
    base_url="https://www.virustotal.com/api/v3/",
    headers=headers
)

async def enrich_ip(ip: str):
    response = await vt_client.get(f"ip_addresses/{ip}")
    return response.json()

async def enrich_domain(domain: str):
    response = await vt_client.get(f"domains/{domain}")
    return response.json()
