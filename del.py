 
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.soccervista.com/"
res = requests.get(url)
soup = BeautifulSoup(res.content,'lxml')
# * table = soup.find_all('table')[0] 
table = soup.find('table', attrs={'class':'main'})
df = pd.read_html(str(table))[0]

print(df)
