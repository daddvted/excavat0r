import lxml.html
import requests

# url = "http://www.cdmzzj.gov.cn/getRollInfoAjax.do?method=newsDetailInfo&articleId=articleId201508072459623537247232"
# url = "http://www.cdmzzj.gov.cn/getRollInfoAjax.do?method=newsDetailInfo&articleId=articleId201508072459630613300224"
url = "http://www.cdmzzj.gov.cn/getRollInfoAjax.do?method=newsDetailInfo&articleId=articleId201508072459557623383040"


browser = requests.get(url)

if browser.status_code == 200:
    html = lxml.html.fromstring(browser.text)
    font = html.xpath('//*[@id="main_body"]/div[2]/table/tr/td/table/tr[2]/td/table/tr[5]/td')
    print(font[0].text_content())

else:
    print("error")
