import re
from typing import Dict, List


class IOCExtractor:

    IP_REGEX = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    DOMAIN_REGEX = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
    URL_REGEX = r'https?://[^\s]+'
    MD5_REGEX = r'\b[a-fA-F0-9]{32}\b'
    SHA1_REGEX = r'\b[a-fA-F0-9]{40}\b'
    SHA256_REGEX = r'\b[a-fA-F0-9]{64}\b'
    CVE_REGEX = r'\bCVE-\d{4}-\d{4,7}\b'

    @staticmethod
    def extract(text: str) -> Dict[str, List[str]]:
        return {
            "ips": list(set(re.findall(IOCExtractor.IP_REGEX, text))),
            "domains": list(set(re.findall(IOCExtractor.DOMAIN_REGEX, text))),
            "urls": list(set(re.findall(IOCExtractor.URL_REGEX, text))),
            "md5": list(set(re.findall(IOCExtractor.MD5_REGEX, text))),
            "sha1": list(set(re.findall(IOCExtractor.SHA1_REGEX, text))),
            "sha256": list(set(re.findall(IOCExtractor.SHA256_REGEX, text))),
            "cves": list(set(re.findall(IOCExtractor.CVE_REGEX, text))),
        }
