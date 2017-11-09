#------------------------------------------------#
# Web Scraping and web rendering  with MongoDB   #
# API code                                       #
# Initial Version:                         2017  #             
# by Fervis lauan                                #
#------------------------------------------------#

from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://flauan:flrumdb2017@ds243285.mlab.com:43285/heroku_h0jj8g9z"
client = pymongo.MongoClient(conn)
db = client.heroku_h0jj8g9z
collection = db.mars_contents

@app.route("/")
def index():
    listings = list(collection.find())
    print(listings) 
    return render_template("index.html", listings=listings)

@app.route("/scrape")
def scrape():    
    collection.remove({})    
    listings_data = scrape_mars.scrape()    
    collection.insert_one(listings_data)      
    # return redirect("http://127.0.0.1:5000/", code=302)
    return redirect("https://fl-ru-webscrape-app.herokuapp.com/", code=302)

if __name__ == "__main__":

    app.run(debug=True)