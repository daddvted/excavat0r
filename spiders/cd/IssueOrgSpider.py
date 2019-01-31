"""
国家新闻出版广电总局 - 发行单位
URL: http://www.gapp.gov.cn/zongshu/serviceList3.shtml
"""

import requests
import lxml.html
import mysql.connector


class FixServeOrgSpider(object):
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.86.86',
        'port': '3306',
        'database': 'service',
        'raise_on_warnings': True,

    }
    url = "http://www.gapp.gov.cn/sitefiles/services/wcm/dynamic/output.aspx?publishmentSystemID=35&"

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

        self.form_data = {
            "pageNodeID": 35,
            "pageContentID": 0,
            "pageTemplateID": 455,
            "isPageRefresh": False,
            "pageUrl": "7e2NgF3U02dai0cwLqW7htXS0slash0u1npuTB5hF8OLkh5Q6uQQJIgOBGmMfX4bkVBHnE",
            "ajaxDivID": "ajaxElement_1_112",
            "templateContent": "749eA6yOssuNCdbHByQHOvlVgc0add0eZTp0add0T0slash0gWI5SfQV3e0add0mTpjfTiC3bQ7y9vqkgAjyzCkSfWi2uuxk0slash0cZH0add0KFi0gEjByIPTJUnSmNnVn5p7XAbdJ0add0nMaqz8EjzMGiQq6e5GSJZFHlivZZhNR2GRBUa9FAyLxAgEKuA9RT7Ov4ybj8lUCeULN0R5DuYrDyrX05I6dfClXaZkBQ00slash0sWCjDLL7BTTZzRYFq0add0vSbvGRqbpBMQ8TEE6f1fggGIbkFI0add0TqmR66RY7KaoiqMviIov7W7Q81QrUkrJO2QVVtf5WLDF0slash0kqOrIQrMPebQ0slash06nQViT71xNe2VOnRgRd2I4m80slash0SKWVcZmfa0add0WMzm31idYgcY30add0taWa8lK6otH9ZsVKCpliRTOGqAS7iAvdl7XchEdHshX6OHHiJ0h0slash0nvNZwnayGPtgJhRUU8WFG0add04p6WHj9e5hNpdRzhWAIl282eb0add0Dwer0slash0XAU2G9hbCdEDdCa0slash0fR7lo3OoZI12U9bLjCzbZ0add0XalWny0slash0C9cUQY4GtegRn5O0slash0cKc0de6Sx1tuGrd0add0VogKQiiixvsbyE0add0SfEQFbQWgdq6FSOOdAzj4MdGY5LY5mY3FuYQvJCv6RZZv0slash0V6oNF4PBwmMjSn87j4Nt99J78lLcnibZoFqkhzAKj6E3y6b5hafUsbYw0slash0XlyiMGkZg3ldR8uewRjMNlt0slash0LYHXkQUGEe1fUmyaEZcbyOc6xCV0slash0QjcJvmspjMNNSdzbpuyvulgqI20WiPSrMV6j4x1sbklHk5kw2mEfiWpJvPCDEcuw5BBUlHZgHhqnZTXOc9vlFf58EICu4nMSDEuKg5mPPU6aCJW5lSUVfbIrhJCD0add0AZClgqLqn75rCqQFNYfRABdfAkPZ96OF30add0s0add0UVYfz9FtFTFXRHS9luXqeEZofHT1oUUl2UQmhbX4f8mG3LG8HuY7OB2xxUdAq8E7G6zRcHSvTh3qeb4DwBBEM0add0B0add0xOChexeLjawzOs0slash0txFPaSvxdsnL0add0kILTvecuxrdBbktxhVfFTdQAQpxPvshGog0slash0I9lNYqDM0zvXHJ33gNbJDbeNqhknTvrKtkl0add02QQG3bq7lhLy9oweolXAZIArSL2p9WZzIlGcrsFBMODemds5ku4tNgxwK9A6eY59UXEucaqWjAFD7e80add0QP0omtaCuE0slash0ZbP1nsOFMOhL0jhPrqflrwetMZOJ0slash0iU90UeV7ZXL19LgtYznIHrp57dTXBOWr3Swh0slash0skzrjpMhKTD90add0djlTrnejA19IW2m0add0iq1x0add0jIZjPehTcs58nWy0slash0dyHNP9yTdQQWGhVEHbXtdFEbaLU6rfqngabX0slash0MekEsk1Cgqt0j5pK1YUCKaGX0slash0PokqXG6mCkAQ7OYL5yyK7UV6wU5yCycA0add07RfKwkPbiRYBQ2i4qnH7zyUhEgbDaerskfenV8PC00cSE2HmgZ5sThIa9o0slash0UUpLAg0slash0nm9cuQUKJDXVcGYDr0slash00umsjGG9p369XDeee3xPRSodIbCdg3Yue0slash0Wy0add0uXZWVYmqC5NRnM09AOTutN5ovP0L12RdhTAnPHEjqUrPqgMxyBCNvJnFeYro4o4ZCEUYibkqy0add0HwL0QTaXnApR9holejcF1lDVtHWScaaMkZMZC3kRLJsjkqXl4L214fR2dvoYeWFwlxooNRlPK0Gm7A5j1PmyL0add0aY418fzkhgcRMWNC31HeWIPTqj984RbybKsM0aJB0add077OucztinVLETB2i7tL63xpTxyTdlUS3wOyYFV7eSGs30e2bSJwP5GdrwwgkmywK7JOhv95HmtjSWoMhVJQ9qXCITeSyFO3vMF0slash0kCMi954PiustwboFBZ0slash03yJBFOoM40xhxeouGvyRsrWDp8zYtadWC0slash0SASx1vAAtLq6gohdmxUg6ASoqluOeJZfrrWe1c6O9hyy04SCJpJeDkyUOwV0slash0p8E0ud0add0jPXGK0CzfaRNxGHuVAl54ChrSFpApDCEAxGvN1blc0slash0gv2vENq43m0add0rTrKtWhXy4M0slash05Mlk6tiBpaFBHjkV4v00add0JTbfkclZoCZP7wmXWZmLgdZFWe28HOi57Xe76cDurZ7tazZ9pxsHLnP05QrB9E7XdYj0slash0wfrsvvgl51NGGC0add0Fi75QN8W6I6SDEjRLAEyhiR0slash0J1hqOu8RXdM4hrXWWVuHqQ0slash0sLIFO2OCkBw7Ndiuw5cfUZfN2AW0add0Dq0add0j2PvmljjOb7B8v1GHhGg7VqnPaP2k0slash0vxL8ADaUSNkX43HikJczI52jrA4aIDRJSQIMxmjvg0USPpzb6LTOxFMQjkzqVHtmSOVoyMA8R0add0PVbEV0slash0X0RP0add00XtITln33vZ9hHhCofY0slash0qxTPH5Tq0hOy5AhFUBLGewDoa85L1Sl4yWj9MqI0slash08BVl3IrWC5Ae0B4zjRwyUL9ZEQTmGyURpWj6uxHZ0add0FT3WzHL55IKGvE7T5rCY4HJJb75TBWkFTiEfF5971vJwop2DiO3Wp7qhNcT0add0sXprz5yrKLvWwyAm7dpgLObK0add0EP8xS9lXBONooLd2mjxL7sYaJnMTrC0add0SlgTtC0NQYjAL7bRXkH00add0lCW7dO8MKF6M70add0jWbD7pcwqFLSFO8fAHoWyUkFeHyDHgrcAz9weGvU6OU9aiib4rvPUv4iCiqjVqsTLhAIGvRzoxaILh5ZO0slash0mmRoGLYMqJZyTHQoLAjenoBxlz4Zd0slash0QTc6UrrsAjJiVOJ3AFb0add0ldIvJZ1YZv4Wd47jVvKLsCusVREngo5vYGkKXu96KtdpYkyuN39xB9g3FpaLqpUESbADuEFWX7xsC6ZlWtH9c3UWPFlXADj1F0add0aylqPcu2N5bVAkVFVg9SUxsCdY4xd63TtKXBfY2QZytGLg0slash0SeHtsiRSo4yxhIDl1ivXxoP0slash0c2f0add0dqTflR51hFPUlKMUXieHKz0add0tNCj8eKoU22h0add04GgNVCXCb35jCSqBOFQX9ACoBo0slash0QPoXmXdALCpvXAPCLCcyCvgjtPTPbr9BftS38VDpUlj0slash01qN00add0I0I0slash0psBkyNsjgv9FLZEV2gGxwEfVhW7RwogibGQk5tdOEIbwIRN0add00add0FjoQxnGG7e0slash00C447mAELbJ9oHaaYEe5KohwZ65ghmnBQ0Ym0add0z6GOBLeTLx0add0jzavqkRamb0slash0HP1PC70slash0GG22tbu3b5jqz41bJ0slash0zBRdXQjiZvAvwiMnQnylSCh0add0e0add01xc2pOywbyAcyAIB5YNHKfDDi1jzBbN8ndFgp7avJsE0slash0lCKY3r1aQdDL2PV5wx20add09iKTQ23fZFqOWbSSkGD0cgJDfVnnz40add0ckih80gBuuBq8hFhFX4eHFvLkLPfR3CVjFrtqW2iy5bG7B7ux0add0gLI1kk0JhQgHVa1RvwvTKBBGzPcrNqPsooCSKqTOnAyr74d495F19pErhutrorr0add0S3efcqCQr0Y0GAQFPu4zs0eQKwXj8KVdk95pha0hZ3ZhwVK4E50slash0n1snMVBBb0slash0MSlJNIaNBeu09GeCJ65e20add0Tr5c0U6meP2RaC3BeSSt8JdEkn8GXbGKKVPwWKzvJL5IGjJoss90add0IB9xmIT9j3H7BYUjqQ5wXOhX7ixYyx0add09K0FbIFGfpsU8gEOHfXcs3w9oqpxenTIVyZ0add0DF0add00fXbpieo5XNPdf2ZsPWRuX0hRQFWnR7WQYdfQmJtcc537T6yosxTl50slash0qxqUMJmjg6GHoePsUWsdUlS1MC1ZO7IvLdw07KD8ypIM6IgEA9V0slash0KZytobF9619Lo8Euveghg3NF9T1JDjlXglEhzAG0CGlLmgx0bJMps80add0muPv4qOHxnfXKmEGD0add0iD4WJYxxg0add0lALpwwVVrpTnQEN342Qb3vFPzxvkzGTtNkZ4mMWCMKRskLKrINv51JCJwwoeLsS76EQIa6bWav0add0muyaYjhihZpqi4XfEBCloa3XKmxWsz0slash0DvkdXr2PI5mwc7TsWuV1SBoqMs0add0zXWpUQRdYmYRC1HPlFq122Zxxr9X0slash0WPFjJDC9sTya2f0yyyxMl0add0bcUHLxWuJPp6aeFGiU7oEV0KCKtON0slash00add0pGN7dpS0usN8DzgJY7UkAuDHtRTAsRxaX6xbrwCamb10slash03eQ9WJvZzo0add0mgr8vAxZD36SYb0kU0slash0cL2Lz0a1M7HlzI1DGopYIHYbktYBpfwhny23k0slash0Kitsrq0slash0WBgHDHfCDqXhlIvtXEhQOSvHl0slash0VWOUyPe0iKfKF8JAAKJETJ6B0YIbQFBw7LnBpkEvBAIfHi6NkhYW40add0rRfqEx9Yj0add0a90slash0kWTz4J0slash0SZJhA0equals00equals0",
        }

    def save2db(self, data):
        """
        Change this template, refer to EnvProtectionStdSpider
        Change this template, refer to EnvProtectionStdSpider
        Change this template, refer to EnvProtectionStdSpider
        """

        template = "INSERT INTO issue_org(org_name, issue_type, province) " \
                   "VALUES ('{org_name}', '{issue_type}', '{province}')"
        sql = template.format(**data)
        self.cursor.execute(sql)
        self.conn.commit()

    def crawl(self):
        for m in range(2, 8):
            print("====== Processing page {0} ======".format(m))
            self.form_data["pageNum"] = m
            browser = requests.post(self.url, data=self.form_data)
            if browser.status_code == 200:
                root = lxml.html.fromstring(browser.text)
                table = root.xpath('//table')
                trs = table[1].xpath('.//tr')
                num = len(trs)
                for n in range(1, num):
                    tds = trs[n].xpath('.//td')
                    data = {
                        "org_name": tds[0].text_content().strip(),
                        "issue_type": tds[1].text_content().strip(),
                        "province": tds[2].text_content().strip()
                    }

                    self.save2db(data)

            else:
                print("Error when crawling page {0}".format(m))


if __name__ == "__main__":
    spider = FixServeOrgSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
