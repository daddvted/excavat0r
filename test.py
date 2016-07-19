import lxml.html
import requests
from urllib.parse import urlencode


url1 = "http://www.ancc.org.cn/Service/queryTools/Internal.aspx"
url2 = "http://search.anccnet.com/searchResult2.aspx"

data = {
    "__VIEWSTATE": "/wEPDwULLTE5NTYxNDQyMTkPZBYCAgEPZBYCAhMPFgIeB1Zpc2libGVnFgYCAQ8PFgIeBFRleHQFBuWxseS4nGRkAgMPDxYEHwEFQ+adoeeggeS9jeaVsOWkquWwke+8geivt+i+k+WFpeato+ehrueahDEz5L2N5oiWMTTkvY3llYblk4HmnaHnoIHvvIEfAGdkZAIFDxYCHwBoFgICAw8PFgQeC1JlY29yZGNvdW50AugHHhBDdXJyZW50UGFnZUluZGV4AgpkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBQUSUmFkaW9JdGVtT3duZXJzaGlwBQ1SYWRpb0l0ZW1JbmZvBQZSYWRpbzEFBlJhZGlvMgUGUmFkaW8zhOuhmq2e4jNVflP2a/Dev64pnfg=",
    "__EVENTVALIDATION": "/wEWCgKJrOSRDALLnru/BwKB7J3yDAKbg6TuCQLj+szOBgLC79P5DgLC78f5DgLC78v5DgLChPy+DQLjwOP9COj9sw5V3AHWQSX5KcfFX43mYoVr",
    "query-condition": "RadioItemInfo",
    "query-supplier-condition": "Radio2",
    "txtcode": "6924090700135",
    "btn_query": "查询",
}

headers1 = {
    "Content-Type": "application/x-www-form-urlencoded",
}
# resp = requests.post(url1, headers=headers, data=urlencode(data), allow_redirects=False)
# resp1 = requests.post(url1, headers=headers1, data=urlencode(data), allow_redirects=False)

headers2 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "search.anccnet.com",
    "Referer": "http://www.ancc.org.cn/Service/queryTools/Internal.aspx",
    "Upgrade-Insecure-Requests": 1,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
}

params = {
    "keyword": "6924090700135",
}

resp2 = requests.get(url2, headers=headers2, params=params)

print(resp2.status_code)
print(resp2.text)
print(resp2.headers)
print(requests.utils.dict_from_cookiejar(resp2.cookies))
