from flask import Flask
import pandas as pd
import requests
from bs4 import BeautifulSoup


# !soccervita url
url = "https://www.soccervista.com/"
res = requests.get(url)
soup = BeautifulSoup(res.content,'lxml')
# * table = soup.find_all('table')[0] 
table = soup.find('table', attrs={'class':'main'})
df = pd.read_html(str(table))[0]
# print(df[0].to_json(orient='records'))

print(table)

app = Flask(__name__)

@app.route("/")
def hello():
    return table

@app.route("/hi")
def hi():
    return df

if __name__ == '__main__':
    app.run(debug=True)

