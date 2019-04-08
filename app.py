from flask import Flask, render_template
import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Response
from flask_pymongo import PyMongo

# !soccervita url
url = "https://www.soccervista.com/"
res = requests.get(url)
soup = BeautifulSoup(res.content,'lxml')
# * table = soup.find_all('table')[0] 
table = soup.find('table', attrs={'class':'main'})
df = pd.read_html(str(table))[0]
data = df.to_json(orient = "records")

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'betting' # name of database on mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/betting"
mongo = PyMongo(app)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/tips")
def get_tips():
    r = Response(response=data, status=200, mimetype="application/json")
    r.headers["Content-Type"] = "tapplication/json; charset=utf-8"
    return r


@app.route('/hello/<game>')
def get_game(game):
   return 'Market for %s!' % game

@app.route("/leagues")
def leagues_page():
    online_users = mongo.db.users.find({"online": True})
    return render_template("index.html", online_users=online_users)

@app.route('/result')
def result():
   dict = { 'phy':50, 'che':60, 'maths':70 }
   return render_template('result.html', result = dict)

if __name__ == '__main__':
    app.run(debug=True)

