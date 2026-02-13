import asyncio
from app.ioc.ioc_models import IOC
from app.enrichment.enrichment_orchestrator import enrich_ioc


async def test():
    test_ioc = IOC(type="ipv4", value="8.8.8.8")

    enriched = await enrich_ioc(test_ioc)

    print("\n=== ENRICHMENT RESULT ===")
    print(enriched.enrichment)


if __name__ == "__main__":
    asyncio.run(test())
