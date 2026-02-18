from app.extraction.ioc_extractor import IOCExtractor

sample_text = """
APT29 used 192.168.10.45 to communicate with malicious-domain.com.
The malware hash was 4d186321c1a7f0f354b297e8914ab240.
It exploited CVE-2021-44228.
The C2 URL was http://evilserver.com/command.
"""

results = IOCExtractor.extract(sample_text)

for key, values in results.items():
    print(f"{key}: {values}")
