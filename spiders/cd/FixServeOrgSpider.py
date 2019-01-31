"""
成都市城乡房产管理局 - 维修服务机构查询
URL: http://www.cdfgj.gov.cn/WXZJ/FixServeOrg.aspx
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
    base_url = "http://www.cdfgj.gov.cn/WXZJ"
    url = "http://www.cdfgj.gov.cn/WXZJ/FixServeOrg.aspx"

    def __init__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

        self.form_data = {
            "__EVENTTARGET": "ID_ucFixServeOrg$UcOrgInfoQuery1$UcPager1$btnPage2",
            "__VIEWSTATE": "zpzNRoGe99s+vqptXdD2eLSIDpqzaPslgRJySakH7WCD89v8ZZO5r7KtK1tD5G5fKc1hFnVc6/l9hY818T3VaoYPdXpHFfJG+DwEioXeyDn8vAvDW8Hyyu+McPEfCuQ5e2wBLF3hAny7vFe4CwKDJKETnWH4dr5dM7pEHv4yahOcicPPLN4ofDNG51532FrAwugOkgqZH9ZQ5Qb1xp9x0ptycc68KBzvPICGl3BQb6O6E+ejcFx7VxTeTMc1Y9dY5nMwOmz6H2iUBZcTHehm13+AicezjZeIB52IgBzkB+aNogRmiTlfOUw1ll9qz7frqtYJ+fMbQRdjGqyqmIdVLCq5bubrRVqTY0CsPqbo0ZHbrSkn2v647uhav2H4ptQ54xniDvKDg2gw9QkzMFmfaxye5mh8OBJrkGL1yl26Xrv8c3wYjpWbDLJCRLJomwMpMWYEDH1OlIKW+RSbg684664xuaOP+1VALNiN22zRFDV7IGOM0GTOeB+AilAPiSYpu3n+QRoO9UfqIyllV5NmQ4pUQ7fVgjl3LW0JvzjYgjEN3xy7eEsL4EXor6dUTK8jGucFiHR4NmoVvS3l5RsCQ8rL7E0mL0m1VEf6SeRNj6C/X302zSLV30O3FPGG00SzT4pRd3GEtaMVGPafByhOdzndxOykWHBIM9Py0kGeN4xs3QMdeVvkxAVMe3aS/CLa3yqSWVhPvgyFdC6areYQl3gGa+f66kHXuEsUlSv6IAtWcbG8OISshecq71SXE8E2in2ihtqNFSs+gmy8BtNyDIPgcrJ9d8ARCgJCxKdnUsCW1/HOZgpOJCFaM0ZZmUU3RMViASagggb1+jKtLdDWwt254KOOhR/K1xobI4Jfv6n7DtP8+xRLLbwvIA4c237Sd4ZtIux79yDMYlTG4eregE5EX6phKLKFPYDv+9VBibjrzCRKZYnuf9oGlw1TaWydDimUc60l9BfRMW9bqVt50rBf9CKfsDzunvrSAZj2kz5HK61KrXwNwGHavIMdTx1Yv18yHI+R5/xtT3YEPCCIqP1Kmrlf8sfECEDn3lYj1zyFmjhuR042VBlxazz7rA3Zd3Ckfag2UCay0aHaxSH8bgFK+iPFQXr7YUmuKkApaoBAOx7+TIGDTcANV4wOd/76lXnvtCxKdkE6IJGZKGbMzrBj3pZ8Bu0bQW61Ec5q0sscqlYA27XInygW77W1RGQ/utNJRTLXaydStoWwTPJOjrkIPaVCyTOc4FdGBZpKUq8250w01eXWoZqL6JBjaA3NdNR9XucsonXsNQAoZaDobsCIJt3v3fLXxZzhQ0imqXnV0hX03hPU0XEkaiqeWti8kHQ8TQ8mpTYeleNpdCmZaDQzd2JycANMhy1TEt/lg+VNEHVOwWVQjSru9fgc0rGSQNt2k9g2L3VJr/LeLhc6TbmzKsrf6kfLJpd8CvsAg4rx2JMPoftSU2KtT7Ks/I1FmzCh8vEEVvnYAAKUCkaulXTkG/nUvVshMuA/e7lLYUTxO1k15IY3+KVpdye53pMZNGQ8IITD2RHAISqtgq7c9jUn4ZKZW5w9fmR2iOp0CTo/wPmbn6nFOWcnfhp4cpRZTN/ho21T61fQjItajOxZnmVzKpcnhBDwtrPntWLJCxYDmMwEg742aYesffeIlQaGGeyeTEu/6lnWp8NlWrtIfQRtNzwpI98wheo+asH7gjynXPkpnOJtZiAP72ShpOlnKXLSxYD8yRjmL/MHbPupi/0DMXjA3EgjQIWnbmHYlMYVd4RT1ThoxxawCIRSnjEGpqWqyJkfWrJH2ODeHldHOoOZZuuRiipn1agXsOxP83RwddCwehH/b3N9dZgqqpiiIfW08KzQw9cMev3gHcU649MHrylrdth81P5s3C39fajUo+xK9Ga3cPRf52RfqI1zvBU7LBRv1yES3Jf2CG7Ai2lVG/E2TjzSOzEO/qr2+b+1+l1yCjOqWPebDQwAf2NtqoBPwMKf6BLEq1R3yr70HJ1qUbRwCSj3syEfFwkN/u/264orDDCtYutLpnvdiG9ZGPVULw6w82aOC4ziAVtLcWvTa9kovxLStqx1nsCFN/FxegHonSff3LEXwqBzzdKTc9sg1EDIFBviNMyLEW098X7uXDcd2LE9ndVDBKjRaMA6W69P5zZJOOM1TKY2ruzaHnVNLesa40c6r2RTSXgbcm900WQeKQK873B3H7Lu/AXRudMsnl8sJbEyNnI5wkOpbxjP6U1BIUd/BrS5BclBcbUIJKnKEoT/62vl2hwEjoe5vApzZ/8KhamSWrfcGvYCOKEzBZKXi6+1V+PcdYResAaWEq7tI5rE+O2yIoC88P/2iqvBGmPZX/J2UKFmrOlO16JbepwdujgxbIDfYOpVY763wtGlt3PhJVT0kuTnzFMFNP2/7zWxq2l66Td1IPx1NKfTfC6slYeh4rYO+Z1LGFssTOv3C8vIZvvSxS2eX+GbnzW1uPGua7f3spcYMVanQHBzuuDsNoSSQbqFb5yCTUo2cbkgwnc5hpojcP1822jA5hQT6ztL+50gEKuqT6+IttmLdG1i++2uMivgqtf+XuthcXidHAPwE7D7NS1ph9D3rlLOAyYGVLHqvQWz+hyXQK+zoa3Z1IO4zvC/itSTCu8IHDAkMjieRDrNcv8YhmL/NdIbbLYv+LsDmWaA8a0PRKZNffbqCbtbiNTNG7W5WFl7l0Vd+kmDTywGYVbWN0z0XskS4nuI2jAmd3LxagDpJd8nN+yFI4Af5ASih4utbYa7gKPu4ePFBqB2PpqdSJ/L9jPIp55zzRL8Tpwn6Lkxug++ThKFVBAhRDgDviP9b69mCbcM1sqFLnQJ5/v8Uj6TkcqpgoemuubR0CybjN7fIv9DB8WswbQbhKpRZtKGu523M+Zr53pzc2dmpgnISeuj7avM1TxFFk+CYBmpmt3DoJA40XiX3KY03qyIGINuYav5BimFup/Ze8YU46OvldSIqo3kA0JBahhNENqydOjgfVJoFxr0yjTRY702DsGoIrKbkz1fG0jSsiPKyxECS6FR6tNT7rElBdfY4RBKskZ0SFZm5KPNZfepXXktxPaEFowq7hZ/11pHpH5PZmEwL4jOEZYU5ThLx+5N9skAwX14ikbtxb2XXLdt5MIJ60R1ekIBq3bAemexE2ZppLvYCHe+ZGAy9Z4635yA8qtAnKF5m7gOgUDHVdUgNniHbi5nx8S1ebV2lKc4GcAijPS77VTZOWa4TiWtTo2BXv36v+WwiLKdyCt6EkkZnGGeYpVVpwVG6u2XMdhqAYJk76TdN3tb0Zpbn5oyThUuKnpOAbQrmkumeJyu4OzrUZz5piLiSByiBVLHgushhA9upsi+fcT2YPNHuVD1lq8WFl2Ko91ynXVuzlayP/Wpe9MHwmCPV/WEeQPzA+Nsy1mdioH65zA5m4P7I0UWTwUhPKgPMubIzbXIwLNumCeJsY4R0iu9tv3Nr9x5zlnNtlE8+QUSYPlkXZAjPfV0Ap/RVt05l5mSEkkuclFVeoLAljyxvR560HYb84PMICHTbcOZzx/vnLKr13477wN1DqpCXx23eyea8xdDpXGLC3IWESfXL/Rfggb+KNmlg3JJ5GIG85kbo7K+jp+gyC5I2UK1Jai9DBRjzuP0htX9EC1mSwt4IbcMDZ/FqqrNUauOPPJBNRSiJw+7P4cYIlAHgvWxLD/eHe5uQQqODD+8PYU3Bo7m5QQPJncrxFjQl+AOjo/Qc27V43l9shpZlK62isffqfXw1VjzZIB5SXabw38CFZfIJ9zF3Lne3ntIVy9iZanzs2qV5BJ/7xiz4FX+3mUSM1wJJk39yvxA6vMPSiKyoBERzx7ql+D17UEnCaUb6TdKLkuhqjpf2eBnk/8TJB4VF4Q6dOwY13ZZ8oaKxs2qkv1nWxYlyRTJBQZ2cVn+AokKc2Z5S9nofHLYFw/CYDTukMG95GdkqaN1UWLOYgjIsYcBaELC4m072F41SWyXfvWe3+G/COlwna1be/Yr/nVfYXLlm8U2rCYsxw+k3LXEUfyHDX036M0r9OF/KHRJT6SzuSWmXqOkjuP4yuuZq0NI5h4mbmjCbO5e4D4cO/kpFMLoWy6DInjprIiChmlhwVpgm7Hh7FTR3iOn5OSkgn7jx5IS9iAqFolZgXRZ8YsMijeXZ0h5v1DygEy4JwoEI/9n+dWEjStrGtTydkqlPxC72apSIBI1RnA5g28OOlWGhIyiyTdlGphwd8BiAzMsY/kX4S4r25KhN5EyNAVV1OEKRO4qS0j2tATo28G/wz69aHGrW7O25EzvXSigbN1wvP49FC5Jc7uc/7RSmwWpSjYOAc5p3NpbDlCDhZSDq1R//UbXZmsbHUlYv5Aa8mVct3NoAStGDEME2Fu+dV9MqWxU2/NFyT9B2mvmPMg7LcmZKVmibuEDitzvR6v6Y/Bx/1NK+OP0ZUzQu4WqK9hJBOnVJG3MIUOvnJE7xy/3mYFwhLPPyR6/UihgBxoQv3CYOchFW0YKcGW7UVvqmMe70G2t56bH2Cc7JAS6CXGxfaXOuYt+CMgiP8S+X5UR8Ba+vT5wcFUiizMSOjccqr1Ukh0k2FFDRh035o4giTJxYxGnvbt55orMqbGDLqsyYNpI/LsCV8WnuFqzAGaHjI44aUezDHmCAS82EVlXwQ==",
            "__VIEWSTATEGENERATOR": "43B811F4",
        }

    def save2db(self, data):
        """
        Change this template, refer to EnvProtectionStdSpider
        Change this template, refer to EnvProtectionStdSpider
        Change this template, refer to EnvProtectionStdSpider
        """
        template = "INSERT INTO fix_serve_org(org_name, service_type, registered_capital, manage_scope, level, address, " \
              "contact, phone) VALUES ('{org_name}', '{service_type}', '{registered_capital}', '{manage_scope}'," \
              " '{level}', '{address}', '{contact}', '{phone}')"
        sql = template.format(**data)
        self.cursor.execute(sql)
        self.conn.commit()

    def crawl(self):
        for m in range(1, 4):
            print("====== Processing page {0} ======".format(m))
            event_target = "ID_ucFixServeOrg$UcOrgInfoQuery1$UcPager1$btnPage{0}".format(m)
            self.form_data["__EVENTTARGET"] = event_target
            browser = requests.post(self.url, data=self.form_data)
            if browser.status_code == 200:
                root = lxml.html.fromstring(browser.text)
                trs = root.xpath('//*[@id="ID_ucFixServeOrg_UcOrgInfoQuery1_gridView"]/tr')
                for n in range(1, len(trs)):
                    td = trs[n].xpath('.//td')[1]
                    a = td.xpath('.//a')[0]
                    link = a.attrib["href"]
                    url = "{0}/{1}".format(self.base_url, link)
                    self.crawl2(url)
            else:
                print("Error when crawling page {0}".format(m))

    def crawl2(self, url):
        browser = requests.get(url)
        if browser.status_code == 200:
            root = lxml.html.fromstring(browser.text)
            data = {
                "org_name": root.xpath('//*[@id="ID_ucOrgInfoShow_txtorgname"]')[0].text_content(),
                "service_type": root.xpath('//*[@id="ID_ucOrgInfoShow_txtservetype"]')[0].text_content(),
                "registered_capital": root.xpath('//*[@id="ID_ucOrgInfoShow_txtRegisteredCapital"]')[0].text_content(),
                "manage_scope": root.xpath('//*[@id="ID_ucOrgInfoShow_txtManageScope"]')[0].text_content(),
                "level": root.xpath('//*[@id="ID_ucOrgInfoShow_txtlevel"]')[0].text_content(),
                "address": root.xpath('//*[@id="ID_ucOrgInfoShow_lbOrgAddress"]')[0].text_content(),
                "contact": root.xpath('//*[@id="ID_ucOrgInfoShow_txtContactPerson"]')[0].text_content(),
                "phone": root.xpath('//*[@id="ID_ucOrgInfoShow_txtContactTel"]')[0].text_content()
            }
            self.save2db(data)

        else:
            print("Error when crawling url: {0}".format(url))


if __name__ == "__main__":
    spider = FixServeOrgSpider()
    spider.crawl()

    spider.cursor.close()
    spider.conn.close()
