from typing import List
from app.ioc.ioc_models import IOC
import app.enrichment.virustotal as virustotal
import app.enrichment.nvd as nvd
import asyncio


async def enrich_ioc(ioc: IOC) -> IOC:

    if ioc.type == "ipv4":
        result = await virustotal.enrich_ip(ioc.value)
        ioc.enrichment["virustotal"] = result

    elif ioc.type == "domain":
        result = await virustotal.enrich_domain(ioc.value)
        ioc.enrichment["virustotal"] = result

    elif ioc.type in ["md5", "sha1", "sha256"]:
        result = await virustotal.enrich_hash(ioc.value)
        ioc.enrichment["virustotal"] = result

    elif ioc.type == "cve":
        result = await nvd.enrich_cve(ioc.value)
        ioc.enrichment["nvd"] = result

    return ioc


async def enrich_all(iocs: List[IOC]) -> List[IOC]:
    tasks = [enrich_ioc(ioc) for ioc in iocs]
    return await asyncio.gather(*tasks)
