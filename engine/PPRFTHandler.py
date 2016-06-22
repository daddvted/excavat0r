# P(Press)P(Publication)R(Radio)F(Film)T(Television)
import requests
from bs4 import BeautifulSoup



def crawl_info_to_db():
    config = {
        'user': 'root',
        'password': 'hello',
        'host': '192.168.1.91',
        'port': '3306',
        'database': 'excavator',
        'raise_on_warnings': True,
    }

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    pass




