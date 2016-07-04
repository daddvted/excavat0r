import urllib.request
import lxml.html


response = urllib.request.urlopen("http://www.cdfgj.gov.cn/ZBGS/PZPS/Default.aspx?page=0&ClassID=5")
html = response.read().decode("utf-8")

root = lxml.html.fromstring(html)

# tmp = root.xpath(u'//*[@id="interest_sectl"]/div[1]/div[2]/strong')
tables = root.xpath(u'//table')

trs = tables[13].xpath(u'./tr')
tr_num = len(trs)

for n in range(2, tr_num-1):
    tds = trs[n].xpath('.//td')
    print(
        tds[0].text_content().strip(),
        tds[1].text_content().strip(),
        tds[2].text_content().strip(),
        tds[3].text_content().strip(),
        tds[4].text_content().strip(),
        tds[5].text_content().strip(),
        tds[6].text_content().strip()
    )