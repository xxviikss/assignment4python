from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask , render_template, redirect , url_for
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
import jwt
from functools import wraps
import requests
from bs4 import BeautifulSoup
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Sequence

app = Flask(__name__)
# Bootstrap(app)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kalamkas@localhost/WebScrapping'
db = SQLAlchemy(app)

class Coin(db.Model):
    __tablename__ = 'coins'
    # id = db.Column('id', 
    #              Sequence('coin_id_seq', start=1001, increment=1),   
    #              primary_key=True)
    id = db.Column('id',db.Integer,primary_key=True)
    coin = db.Column('coin', db.Unicode)
    news = db.Column('news', db.Unicode)

    def __init__(self,coin,news):
        self.coin = coin
        self.news = news


class Scrap:
    def __init__(self):
        print('Loading...')
    
    def pars(self,crypto):
            # r = requests.get('https://coinmarketcap.com/currencies/'+crypto)
            r = requests.get('https://cryptonews.com/news/'+crypto+'-news/')
            with open("index.txt", "w", encoding='utf-8') as f:
                f.write(r.text)

            with open("index.txt", encoding='utf-8') as fp:
                soup = BeautifulSoup(fp, 'html.parser')
                

            paragraphs = soup.find_all("div", class_='col-12 col-md-7 column-45__right d-flex flex-column justify-content-center')
            paragraphs = soup.find('div', class_= "article__badge article__badge--md mb-10 pt-10").decompose()
            coin_news=[]

            for item in paragraphs:
                title = item.getText()
                coin_news.append(title
                        # 'title': item.find('a',  class_='article__title article__title--lg article__title--featured  mb-20').get_text(strip=True),
                        # item.find('div', class_='mb-25 d-none d-md-block').get_text(strip=True)
                    )

            # for item in coin_news:
            #     print(item)

            return coin_news        

            

# crypto = input()

# scrapper = Scrap()
# sitepars = scrapper.pars(crypto)


@app.route('/coin',methods=["POST","GET"])
def coin():
    if request.method == "POST":
        user = request.form['coin']
        scrap = Scrap()
        n=scrap.pars(user)
        coin = Coin(coin=user,news=n)
        db.session.add(coin)
        db.session.commit()
        return redirect(url_for('coin',crypto=coin))
    else:
        return render_template("coin.html")

@app.route('/<crypto>')
def crypto():
    return render_template("crypto.html")



if __name__ == '__main__':  
    app.run(debug=True)