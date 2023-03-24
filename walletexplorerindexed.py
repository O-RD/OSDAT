import requests
import numpy as np
from bs4 import BeautifulSoup

source_url = "https://www.walletexplorer.com/"

pages = [1,2]

temp = []
for page in pages:

    services = [
    f'{source_url}wallet/{s["href"].rsplit("/")[-1]}/addresses?page=' + str(page) for s
    in BeautifulSoup(
        requests.get(source_url).text,
        "html.parser",
    ).select("table.serviceslist td ul li a")
]
    for service in services:
        temp.append(service)

for service in services[:5]:
    s = BeautifulSoup(requests.get(service).text, "html.parser")
    print(f"Wallet addresses for {service.rsplit('/')[-2]}")
    print([i.find("a").getText() for i in s.find_all("td") if i.find("a")])

    for i in s.find_all("td"):
        if i.find("a"):
            print(i.find("a").getText())