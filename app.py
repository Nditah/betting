from flask import Flask, render_template, request, make_response
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

@app.route('/user')
def user():
   return render_template('user.html')


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

@app.route('/match')
def match():
   dict = { 'phy':50, 'che':60, 'maths':70 }
   return render_template('match.html', record = dict)

@app.route('/result', methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html", result = result)

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['nm']
    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('userID', user)
    return resp

@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('userID')
   return '<h1>welcome '+name+'</h1>'


if __name__ == '__main__':
    app.run(debug=True)

# TODO style static pages: today, tomorrow. admin http://tutorialspoint.com/flask/
# TODO connect to MongoDB with dot env https://flask-pymongo.readthedocs.io/en/latest/
# TODO admin user registration, login
# ? READ  